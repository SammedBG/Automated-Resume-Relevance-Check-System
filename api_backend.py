"""
Clean and Simple FastAPI Backend for Resume Relevance Check System
Reliable version that matches app_clean.py approach
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import json
import os
from datetime import datetime
from pathlib import Path

# Import system components with error handling
try:
    from resume_processor import ResumeProcessor
    from database import DatabaseManager
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run: python setup.py")
    COMPONENTS_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="Resume Relevance Check API",
    description="Simple and reliable resume evaluation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
if COMPONENTS_AVAILABLE:
    processor = ResumeProcessor()
    db = DatabaseManager()
else:
    processor = None
    db = None

# In-memory job tracking
job_status = {}

# Pydantic models
class ProcessingRequest(BaseModel):
    job_role: Optional[str] = None
    hard_weight: float = 0.6
    semantic_weight: float = 0.4

class ProcessingResponse(BaseModel):
    job_id: str
    status: str
    message: str
    total_resumes: int

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    total_resumes: int
    completed_resumes: int
    results: List[Dict[str, Any]]
    started_at: str
    completed_at: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Resume Relevance Check API",
        "version": "1.0.0",
        "status": "operational" if COMPONENTS_AVAILABLE else "components_missing",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if not COMPONENTS_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "message": "System components not available",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    try:
        # Test database connection
        stats = db.get_statistics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "operational",
                "processor": "operational"
            },
            "statistics": stats
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/api/v1/process-batch", response_model=ProcessingResponse)
async def process_batch(
    background_tasks: BackgroundTasks,
    resumes: List[UploadFile] = File(...),
    job_description: UploadFile = File(...),
    job_role: Optional[str] = None,
    hard_weight: float = 0.6,
    semantic_weight: float = 0.4
):
    """Process multiple resumes against a job description"""
    
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="System components not available")
    
    if not resumes:
        raise HTTPException(status_code=400, detail="No resume files provided")
    
    if len(resumes) > 50:  # Max batch size
        raise HTTPException(status_code=400, detail="Too many files (max 50)")
    
    try:
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        job_status[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "progress": 0.0,
            "total_resumes": len(resumes),
            "completed_resumes": 0,
            "results": [],
            "started_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        # Start background processing
        background_tasks.add_task(
            process_resumes_background,
            job_id,
            resumes,
            job_description,
            job_role,
            hard_weight,
            semantic_weight
        )
        
        return ProcessingResponse(
            job_id=job_id,
            status="queued",
            message="Processing started",
            total_resumes=len(resumes)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get job status and results"""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatusResponse(**job_status[job_id])

@app.get("/api/v1/results")
async def get_all_results(
    limit: int = 100,
    offset: int = 0,
    verdict: Optional[str] = None,
    min_score: Optional[float] = None
):
    """Get all results with filtering"""
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="System components not available")
    
    try:
        all_results = db.get_all_results()
        
        # Apply filters
        filtered_results = all_results
        
        if verdict:
            filtered_results = [r for r in filtered_results if r.get('verdict') == verdict]
        
        if min_score is not None:
            filtered_results = [r for r in filtered_results if r.get('score', 0) >= min_score]
        
        # Apply pagination
        total_count = len(filtered_results)
        paginated_results = filtered_results[offset:offset + limit]
        
        return {
            "results": paginated_results,
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/statistics")
async def get_statistics():
    """Get system statistics"""
    if not COMPONENTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="System components not available")
    
    try:
        db_stats = db.get_statistics()
        
        # Add job statistics
        active_jobs = len([j for j in job_status.values() if j["status"] in ["queued", "processing"]])
        completed_jobs = len([j for j in job_status.values() if j["status"] == "completed"])
        
        return {
            "database_statistics": db_stats,
            "job_statistics": {
                "active_jobs": active_jobs,
                "completed_jobs": completed_jobs,
                "total_jobs": len(job_status)
            },
            "system_info": {
                "components_available": COMPONENTS_AVAILABLE,
                "max_batch_size": 50,
                "supported_formats": [".pdf", ".docx", ".txt"]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/export/{job_id}")
async def export_results(job_id: str, format: str = "csv"):
    """Export job results"""
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = job_status[job_id]
    
    if job_data["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    
    try:
        results = job_data["results"]
        
        if format.lower() == "csv":
            import pandas as pd
            df = pd.DataFrame(results)
            csv_content = df.to_csv(index=False)
            
            # Save to temporary file
            temp_file = f"temp_export_{job_id}.csv"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(csv_content)
            
            return FileResponse(
                temp_file,
                media_type="text/csv",
                filename=f"resume_analysis_{job_id}.csv"
            )
        
        elif format.lower() == "json":
            json_content = json.dumps(results, indent=2, default=str)
            
            temp_file = f"temp_export_{job_id}.json"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(json_content)
            
            return FileResponse(
                temp_file,
                media_type="application/json",
                filename=f"resume_analysis_{job_id}.json"
            )
        
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_resumes_background(
    job_id: str,
    resumes: List[UploadFile],
    job_description: UploadFile,
    job_role: Optional[str],
    hard_weight: float,
    semantic_weight: float
):
    """Background processing function"""
    try:
        # Update job status
        job_status[job_id]["status"] = "processing"
        
        # Extract job description text
        jd_text = processor.extract_text_from_file(job_description)
        
        if not jd_text:
            job_status[job_id]["status"] = "failed"
            job_status[job_id]["error"] = "Failed to extract job description text"
            return
        
        results = []
        total_resumes = len(resumes)
        
        # Normalize weights
        total_weight = hard_weight + semantic_weight
        if total_weight > 0:
            hard_weight = hard_weight / total_weight
            semantic_weight = semantic_weight / total_weight
        
        for i, resume_file in enumerate(resumes):
            try:
                # Update progress
                progress = (i / total_resumes) * 100
                job_status[job_id]["progress"] = progress
                
                # Extract resume text
                resume_text = processor.extract_text_from_file(resume_file)
                
                if not resume_text:
                    continue
                
                # Analyze resume
                analysis = processor.analyze_relevance(
                    resume_text, jd_text, hard_weight, semantic_weight
                )
                
                # Format result
                result = {
                    'filename': resume_file.filename,
                    'job_role': job_role or '',
                    'final_score': analysis.get('final_score', 0),
                    'hard_match_score': analysis.get('hard_match_score', 0),
                    'semantic_score': analysis.get('semantic_score', 0),
                    'verdict': analysis.get('verdict', 'Low'),
                    'matched_skills': analysis.get('matched_skills', []),
                    'missing_skills': analysis.get('missing_skills', []),
                    'suggestions': analysis.get('suggestions', ''),
                    'processed_at': datetime.now().isoformat()
                }
                
                results.append(result)
                
                # Save to database
                db.save_result(result)
                
                # Update job status
                job_status[job_id]["completed_resumes"] = i + 1
                job_status[job_id]["results"] = results
                
            except Exception as e:
                print(f"Error processing {resume_file.filename}: {e}")
                continue
        
        # Mark job as completed
        job_status[job_id]["status"] = "completed"
        job_status[job_id]["progress"] = 100.0
        job_status[job_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        job_status[job_id]["status"] = "failed"
        job_status[job_id]["error"] = str(e)

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    print("🚀 Resume Relevance Check API starting...")
    
    if not COMPONENTS_AVAILABLE:
        print("❌ System components not available")
        print("Please run: python setup.py")
    else:
        print("✅ System components loaded successfully")
    
    # Create directories
    os.makedirs("temp", exist_ok=True)
    os.makedirs("exports", exist_ok=True)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 API shutting down...")
    
    # Clean up temporary files
    import glob
    temp_files = glob.glob("temp_export_*.csv") + glob.glob("temp_export_*.json")
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    
    print("🎯 Starting Resume Relevance Check API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "api_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )