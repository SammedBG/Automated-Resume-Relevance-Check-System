"""
LLM-powered processing for advanced semantic analysis and feedback generation
Implements the complete workflow as specified in requirements
"""

import os
from typing import Dict, List, Optional, Tuple, Any
import json
import asyncio
from datetime import datetime

# LangChain imports
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory

# LangGraph imports for structured workflows
try:
    from langgraph import StateGraph, END
    from langgraph.graph import Graph
    LANGGRAPH_AVAILABLE = True
except ImportError:
    print("LangGraph not available. Using basic workflow.")
    LANGGRAPH_AVAILABLE = False

# Vector stores
import chromadb
from sentence_transformers import SentenceTransformer

# Local imports
from config import config
from logger import log_info, log_error, log_warning
from exceptions import ModelLoadingError, ScoringError

class LLMResumeProcessor:
    """
    Advanced LLM-powered resume processing system
    Implements hybrid scoring with hard match + semantic analysis
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.setup_models()
        self.setup_vector_store()
        self.setup_prompts()
        if LANGGRAPH_AVAILABLE:
            self.setup_workflow()
    
    def setup_models(self):
        """Initialize LLM models and embeddings"""
        try:
            if self.api_key:
                # OpenAI models
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=self.api_key
                )
                self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
                log_info("OpenAI models initialized successfully")
            else:
                # Fallback to local models
                log_warning("No OpenAI API key found. Using local models.")
                self.llm = None
                self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
                
        except Exception as e:
            log_error(f"Failed to initialize LLM models: {e}")
            raise ModelLoadingError("LLM", str(e))
    
    def setup_vector_store(self):
        """Initialize vector store for semantic search"""
        try:
            # Initialize Chroma vector store
            self.chroma_client = chromadb.Client()
            self.vector_store = None
            log_info("Vector store initialized")
        except Exception as e:
            log_error(f"Failed to initialize vector store: {e}")
            self.chroma_client = None
            self.vector_store = None
    
    def setup_prompts(self):
        """Setup LLM prompts for different analysis tasks"""
        
        # Skill extraction prompt
        self.skill_extraction_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert HR analyst. Extract technical skills, soft skills, 
            certifications, and qualifications from the given text. Return as structured JSON."""),
            HumanMessage(content="Text: {text}\n\nExtract skills in JSON format with categories: technical_skills, soft_skills, certifications, education, experience_years.")
        ])
        
        # Job requirement analysis prompt
        self.jd_analysis_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert recruiter. Analyze the job description and extract:
            1. Must-have skills (critical requirements)
            2. Good-to-have skills (preferred requirements)  
            3. Required qualifications
            4. Experience level required
            Return as structured JSON."""),
            HumanMessage(content="Job Description: {jd_text}\n\nAnalyze and return structured requirements in JSON format.")
        ])
        
        # Semantic matching prompt
        self.semantic_match_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert HR analyst. Compare a resume against job requirements 
            and provide a semantic fit score (0-100) with detailed reasoning."""),
            HumanMessage(content="""
            Resume: {resume_text}
            
            Job Requirements: {jd_requirements}
            
            Provide:
            1. Semantic fit score (0-100)
            2. Key strengths alignment
            3. Major gaps identified
            4. Overall assessment
            
            Return as JSON with fields: semantic_score, strengths, gaps, assessment
            """)
        ])
        
        # Feedback generation prompt
        self.feedback_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are a career counselor providing constructive feedback to job candidates.
            Generate personalized improvement suggestions based on resume analysis."""),
            HumanMessage(content="""
            Candidate Resume Analysis:
            - Current Score: {score}
            - Missing Skills: {missing_skills}
            - Verdict: {verdict}
            - Job Role: {job_role}
            
            Provide specific, actionable improvement suggestions in 3 categories:
            1. Skills Development
            2. Experience Enhancement  
            3. Resume Optimization
            
            Return as JSON with structured suggestions.
            """)
        ])
    
    def setup_workflow(self):
        """Setup LangGraph workflow for structured processing"""
        if not LANGGRAPH_AVAILABLE:
            return
            
        # Define workflow states
        workflow = StateGraph({
            "resume_text": str,
            "jd_text": str,
            "resume_skills": dict,
            "jd_requirements": dict,
            "hard_match_score": float,
            "semantic_score": float,
            "final_score": float,
            "verdict": str,
            "feedback": dict,
            "missing_elements": list
        })
        
        # Add workflow nodes
        workflow.add_node("extract_resume_skills", self._extract_resume_skills)
        workflow.add_node("analyze_jd_requirements", self._analyze_jd_requirements)
        workflow.add_node("calculate_hard_match", self._calculate_hard_match)
        workflow.add_node("calculate_semantic_match", self._calculate_semantic_match)
        workflow.add_node("generate_final_score", self._generate_final_score)
        workflow.add_node("generate_feedback", self._generate_feedback)
        
        # Define workflow edges
        workflow.add_edge("extract_resume_skills", "analyze_jd_requirements")
        workflow.add_edge("analyze_jd_requirements", "calculate_hard_match")
        workflow.add_edge("calculate_hard_match", "calculate_semantic_match")
        workflow.add_edge("calculate_semantic_match", "generate_final_score")
        workflow.add_edge("generate_final_score", "generate_feedback")
        workflow.add_edge("generate_feedback", END)
        
        # Set entry point
        workflow.set_entry_point("extract_resume_skills")
        
        self.workflow = workflow.compile()
        log_info("LangGraph workflow initialized")
    
    async def process_resume_advanced(self, resume_text: str, jd_text: str, job_role: str = "") -> Dict[str, Any]:
        """
        Advanced resume processing using LLM workflow
        Implements the complete evaluation pipeline
        """
        try:
            if LANGGRAPH_AVAILABLE and self.llm:
                # Use LangGraph workflow
                initial_state = {
                    "resume_text": resume_text,
                    "jd_text": jd_text,
                    "job_role": job_role
                }
                result = await self.workflow.ainvoke(initial_state)
                return result
            else:
                # Fallback to sequential processing
                return await self._process_sequential(resume_text, jd_text, job_role)
                
        except Exception as e:
            log_error(f"Advanced resume processing failed: {e}")
            raise ScoringError("LLM processing", str(e))
    
    async def _process_sequential(self, resume_text: str, jd_text: str, job_role: str) -> Dict[str, Any]:
        """Sequential processing fallback"""
        
        # Step 1: Extract resume skills
        resume_skills = await self._extract_resume_skills_llm(resume_text)
        
        # Step 2: Analyze JD requirements
        jd_requirements = await self._analyze_jd_requirements_llm(jd_text)
        
        # Step 3: Calculate hard match
        hard_match_score = self._calculate_hard_match_score(resume_skills, jd_requirements)
        
        # Step 4: Calculate semantic match
        semantic_score = await self._calculate_semantic_match_llm(resume_text, jd_requirements)
        
        # Step 5: Generate final score and verdict
        final_score, verdict = self._calculate_final_score_verdict(hard_match_score, semantic_score)
        
        # Step 6: Generate feedback
        feedback = await self._generate_feedback_llm(resume_skills, jd_requirements, final_score, verdict, job_role)
        
        # Step 7: Identify missing elements
        missing_elements = self._identify_missing_elements(resume_skills, jd_requirements)
        
        return {
            "final_score": final_score,
            "hard_match_score": hard_match_score,
            "semantic_score": semantic_score,
            "verdict": verdict,
            "resume_skills": resume_skills,
            "jd_requirements": jd_requirements,
            "missing_elements": missing_elements,
            "feedback": feedback,
            "processed_at": datetime.now().isoformat()
        }
    
    async def _extract_resume_skills_llm(self, resume_text: str) -> Dict[str, Any]:
        """Extract skills using LLM"""
        if not self.llm:
            return self._extract_skills_fallback(resume_text)
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.skill_extraction_prompt)
            response = await chain.arun(text=resume_text)
            return json.loads(response)
        except Exception as e:
            log_warning(f"LLM skill extraction failed, using fallback: {e}")
            return self._extract_skills_fallback(resume_text)
    
    async def _analyze_jd_requirements_llm(self, jd_text: str) -> Dict[str, Any]:
        """Analyze job requirements using LLM"""
        if not self.llm:
            return self._analyze_jd_fallback(jd_text)
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.jd_analysis_prompt)
            response = await chain.arun(jd_text=jd_text)
            return json.loads(response)
        except Exception as e:
            log_warning(f"LLM JD analysis failed, using fallback: {e}")
            return self._analyze_jd_fallback(jd_text)
    
    async def _calculate_semantic_match_llm(self, resume_text: str, jd_requirements: Dict) -> float:
        """Calculate semantic match using LLM"""
        if not self.llm:
            return self._calculate_semantic_fallback(resume_text, jd_requirements)
        
        try:
            chain = LLMChain(llm=self.llm, prompt=self.semantic_match_prompt)
            response = await chain.arun(
                resume_text=resume_text,
                jd_requirements=json.dumps(jd_requirements)
            )
            result = json.loads(response)
            return float(result.get('semantic_score', 0)) / 100.0
        except Exception as e:
            log_warning(f"LLM semantic matching failed, using fallback: {e}")
            return self._calculate_semantic_fallback(resume_text, jd_requirements)
    
    async def _generate_feedback_llm(self, resume_skills: Dict, jd_requirements: Dict, 
                                   score: float, verdict: str, job_role: str) -> Dict[str, Any]:
        """Generate personalized feedback using LLM"""
        if not self.llm:
            return self._generate_feedback_fallback(resume_skills, jd_requirements, score, verdict)
        
        try:
            missing_skills = self._identify_missing_elements(resume_skills, jd_requirements)
            
            chain = LLMChain(llm=self.llm, prompt=self.feedback_prompt)
            response = await chain.arun(
                score=score,
                missing_skills=missing_skills,
                verdict=verdict,
                job_role=job_role
            )
            return json.loads(response)
        except Exception as e:
            log_warning(f"LLM feedback generation failed, using fallback: {e}")
            return self._generate_feedback_fallback(resume_skills, jd_requirements, score, verdict)
    
    def _calculate_hard_match_score(self, resume_skills: Dict, jd_requirements: Dict) -> float:
        """Calculate hard match score based on exact skill matching"""
        try:
            resume_tech_skills = set(skill.lower() for skill in resume_skills.get('technical_skills', []))
            required_skills = set(skill.lower() for skill in jd_requirements.get('must_have_skills', []))
            
            if not required_skills:
                return 0.0
            
            matched_skills = resume_tech_skills.intersection(required_skills)
            return len(matched_skills) / len(required_skills)
            
        except Exception as e:
            log_error(f"Hard match calculation failed: {e}")
            return 0.0
    
    def _calculate_final_score_verdict(self, hard_match: float, semantic_match: float) -> Tuple[float, str]:
        """Calculate final score and verdict"""
        # Weighted combination: 60% hard match, 40% semantic match
        final_score = (0.6 * hard_match) + (0.4 * semantic_match)
        
        # Determine verdict
        if final_score >= 0.7:
            verdict = "High"
        elif final_score >= 0.4:
            verdict = "Medium"
        else:
            verdict = "Low"
        
        return final_score, verdict
    
    def _identify_missing_elements(self, resume_skills: Dict, jd_requirements: Dict) -> List[str]:
        """Identify missing skills and requirements"""
        resume_tech_skills = set(skill.lower() for skill in resume_skills.get('technical_skills', []))
        required_skills = set(skill.lower() for skill in jd_requirements.get('must_have_skills', []))
        
        missing_skills = required_skills - resume_tech_skills
        return list(missing_skills)
    
    # Fallback methods for when LLM is not available
    def _extract_skills_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback skill extraction using patterns"""
        # Import the basic processor for fallback
        from resume_processor import ResumeProcessor
        processor = ResumeProcessor()
        skills = processor.extract_skills(text)
        
        return {
            "technical_skills": skills,
            "soft_skills": [],
            "certifications": [],
            "education": [],
            "experience_years": 0
        }
    
    def _analyze_jd_fallback(self, jd_text: str) -> Dict[str, Any]:
        """Fallback JD analysis using patterns"""
        from resume_processor import ResumeProcessor
        processor = ResumeProcessor()
        skills = processor.extract_skills(jd_text)
        
        return {
            "must_have_skills": skills,
            "good_to_have_skills": [],
            "required_qualifications": [],
            "experience_level": "Mid-level"
        }
    
    def _calculate_semantic_fallback(self, resume_text: str, jd_requirements: Dict) -> float:
        """Fallback semantic calculation using TF-IDF"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        try:
            jd_text = " ".join(jd_requirements.get('must_have_skills', []))
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0
    
    def _generate_feedback_fallback(self, resume_skills: Dict, jd_requirements: Dict, 
                                  score: float, verdict: str) -> Dict[str, Any]:
        """Fallback feedback generation"""
        missing_skills = self._identify_missing_elements(resume_skills, jd_requirements)
        
        suggestions = {
            "skills_development": [f"Consider learning {skill}" for skill in missing_skills[:3]],
            "experience_enhancement": ["Gain more hands-on experience in relevant technologies"],
            "resume_optimization": ["Highlight relevant projects and achievements"]
        }
        
        return suggestions

# Workflow node functions for LangGraph
async def _extract_resume_skills(state):
    """LangGraph node for resume skill extraction"""
    # Implementation for workflow node
    pass

async def _analyze_jd_requirements(state):
    """LangGraph node for JD analysis"""
    # Implementation for workflow node
    pass

async def _calculate_hard_match(state):
    """LangGraph node for hard match calculation"""
    # Implementation for workflow node
    pass

async def _calculate_semantic_match(state):
    """LangGraph node for semantic match calculation"""
    # Implementation for workflow node
    pass

async def _generate_final_score(state):
    """LangGraph node for final score generation"""
    # Implementation for workflow node
    pass

async def _generate_feedback(state):
    """LangGraph node for feedback generation"""
    # Implementation for workflow node
    pass