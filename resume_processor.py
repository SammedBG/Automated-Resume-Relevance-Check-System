import fitz  # PyMuPDF
import pdfplumber
from docx import Document
import spacy
import nltk
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Semantic matching will be disabled.")
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None
import numpy as np
import re
from typing import Dict, List, Tuple
import io

class ResumeProcessor:
    def __init__(self):
        self.setup_nlp()
        self.setup_models()
        
    def setup_nlp(self):
        """Initialize NLP components"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Please install spacy English model: python -m spacy download en_core_web_sm")
            self.nlp = None
            
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def setup_models(self):
        """Initialize ML models"""
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ SentenceTransformer model loaded successfully")
            except Exception as e:
                print(f"⚠️ Failed to load SentenceTransformer: {e}")
                self.sentence_model = None
        else:
            self.sentence_model = None
        
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    
    def extract_text_from_file(self, file) -> str:
        """Extract text from uploaded file"""
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self.extract_from_pdf(file)
        elif file_extension == 'docx':
            return self.extract_from_docx(file)
        elif file_extension == 'txt':
            return str(file.read(), "utf-8")
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def extract_from_pdf(self, file) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""
        
        # Try PyMuPDF first
        try:
            pdf_bytes = file.read()
            file.seek(0)  # Reset file pointer
            
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
            doc.close()
            
            if text.strip():
                return self.clean_text(text)
        except Exception as e:
            print(f"PyMuPDF failed: {e}")
        
        # Fallback to pdfplumber
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        return self.clean_text(text)
    
    def extract_from_docx(self, file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return self.clean_text(text)
        except Exception as e:
            print(f"DOCX extraction failed: {e}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\-\(\)]', ' ', text)
        
        # Remove headers/footers patterns
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'Confidential|Private|Internal', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using comprehensive pattern matching"""
        skills = set()
        
        # Comprehensive skill patterns - much more extensive
        skill_patterns = [
            # Programming Languages
            r'\b(?:Python|Java|JavaScript|TypeScript|C\+\+|C#|PHP|Ruby|Go|Rust|Swift|Kotlin|Scala|R|MATLAB|Perl|Shell|Bash)\b',
            
            # Web Technologies
            r'\b(?:React|Angular|Vue\.?js|Node\.?js|Express|Django|Flask|Spring|Laravel|Rails|ASP\.NET|jQuery|Bootstrap|HTML5?|CSS3?|SASS|LESS)\b',
            
            # Cloud & DevOps
            r'\b(?:AWS|Azure|GCP|Google Cloud|Docker|Kubernetes|Jenkins|Git|GitHub|GitLab|Linux|Ubuntu|CentOS|CI/CD|DevOps|Terraform|Ansible)\b',
            
            # Databases
            r'\b(?:SQL|MySQL|PostgreSQL|MongoDB|Redis|Elasticsearch|Oracle|SQLite|Cassandra|DynamoDB|Neo4j)\b',
            
            # Data Science & AI
            r'\b(?:Machine Learning|Deep Learning|AI|Artificial Intelligence|Data Science|Analytics|Statistics|Pandas|NumPy|TensorFlow|PyTorch|Scikit-learn|Jupyter|Tableau|Power BI)\b',
            
            # Methodologies & Frameworks
            r'\b(?:Agile|Scrum|Kanban|DevOps|CI/CD|Testing|QA|Unit Testing|Integration Testing|TDD|BDD|Microservices|REST|API|GraphQL)\b',
            
            # Business & Soft Skills
            r'\b(?:Project Management|Leadership|Communication|Problem Solving|Team Work|Collaboration|Presentation|Documentation|Requirements Analysis)\b',
            
            # Tools & Software
            r'\b(?:JIRA|Confluence|Slack|Microsoft Office|Excel|PowerPoint|Photoshop|Figma|Sketch|InDesign|AutoCAD)\b',
            
            # Certifications & Standards
            r'\b(?:PMP|Certified|Certification|ISO|ITIL|Six Sigma|Lean|MBA|PhD|Masters|Bachelor)\b'
        ]
        
        # Extract using patterns
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update([match.strip().lower() for match in matches])
        
        # Additional keyword extraction - look for common skill indicators
        skill_keywords = [
            'experience with', 'proficient in', 'skilled in', 'expertise in', 
            'knowledge of', 'familiar with', 'worked with', 'used', 'implemented',
            'developed', 'created', 'built', 'designed', 'managed'
        ]
        
        for keyword in skill_keywords:
            # Find text after skill indicators
            pattern = rf'{keyword}\s+([^.,:;]+)'
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # Extract potential skills from the match
                words = re.findall(r'\b[A-Za-z][A-Za-z0-9+#.]*\b', match)
                for word in words[:3]:  # Take first 3 words as potential skills
                    if len(word) > 2:  # Skip very short words
                        skills.add(word.lower())
        
        # Use spaCy for entity extraction if available
        if self.nlp:
            try:
                doc = self.nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ['ORG', 'PRODUCT', 'PERSON']:
                        # Filter out common non-skill entities
                        entity_text = ent.text.lower().strip()
                        if len(entity_text) > 2 and not any(stop in entity_text for stop in ['inc', 'ltd', 'corp', 'company']):
                            skills.add(entity_text)
            except Exception as e:
                print(f"SpaCy processing failed: {e}")
        
        # Clean and filter skills
        cleaned_skills = []
        for skill in skills:
            skill = skill.strip().lower()
            # Filter out very common words and short skills
            if len(skill) > 2 and skill not in ['the', 'and', 'for', 'with', 'from', 'this', 'that', 'have', 'been', 'will', 'can', 'may']:
                cleaned_skills.append(skill)
        
        return list(set(cleaned_skills))  # Remove duplicates
    
    def hard_match_analysis(self, resume_text: str, jd_text: str) -> Dict:
        """Perform enhanced hard matching using keyword and fuzzy matching"""
        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(jd_text)
        
        print(f"Debug: Found {len(resume_skills)} resume skills: {resume_skills[:10]}")
        print(f"Debug: Found {len(jd_skills)} JD skills: {jd_skills[:10]}")
        
        if not jd_skills:
            # If no skills found in JD, try basic keyword matching
            jd_words = re.findall(r'\b[A-Za-z][A-Za-z0-9+#.]{2,}\b', jd_text.lower())
            jd_skills = list(set(jd_words))[:20]  # Take top 20 unique words
            print(f"Debug: Fallback JD keywords: {jd_skills[:10]}")
        
        if not jd_skills:
            return {'score': 0.0, 'matched_skills': [], 'missing_skills': []}
        
        matched_skills = []
        missing_skills = []
        
        for jd_skill in jd_skills:
            best_match_score = 0
            best_match = None
            
            # Check exact match first
            if jd_skill in resume_skills:
                best_match_score = 100
                best_match = jd_skill
            else:
                # Check fuzzy matches
                for resume_skill in resume_skills:
                    # Fuzzy match with lower threshold
                    fuzzy_score = fuzz.ratio(jd_skill, resume_skill)
                    if fuzzy_score > best_match_score and fuzzy_score >= 70:  # Lowered threshold
                        best_match_score = fuzzy_score
                        best_match = resume_skill
                    
                    # Also check partial matches
                    if jd_skill in resume_skill or resume_skill in jd_skill:
                        partial_score = 85
                        if partial_score > best_match_score:
                            best_match_score = partial_score
                            best_match = resume_skill
            
            if best_match_score >= 70:  # Lowered threshold
                matched_skills.append(best_match)
            else:
                missing_skills.append(jd_skill)
        
        # Calculate score with bonus for high match count
        base_score = len(matched_skills) / len(jd_skills) if jd_skills else 0
        
        # Add bonus for having many matches (up to 20% bonus)
        match_bonus = min(0.2, len(matched_skills) * 0.02)
        final_score = min(1.0, base_score + match_bonus)
        
        print(f"Debug: Matched {len(matched_skills)} skills, missing {len(missing_skills)}, score: {final_score:.3f}")
        
        return {
            'score': final_score,
            'matched_skills': matched_skills[:10],  # Limit to top 10 for display
            'missing_skills': missing_skills[:10]   # Limit to top 10 for display
        }
    
    def semantic_match_analysis(self, resume_text: str, jd_text: str) -> float:
        """Perform enhanced semantic matching"""
        if not self.sentence_model:
            print("⚠️ Semantic matching unavailable - using enhanced TF-IDF fallback")
            return self._enhanced_tfidf_similarity(resume_text, jd_text)
        
        try:
            # Truncate texts if too long (sentence transformers have limits)
            max_length = 500
            resume_text_short = resume_text[:max_length] if len(resume_text) > max_length else resume_text
            jd_text_short = jd_text[:max_length] if len(jd_text) > max_length else jd_text
            
            # Create embeddings
            resume_embedding = self.sentence_model.encode([resume_text_short])
            jd_embedding = self.sentence_model.encode([jd_text_short])
            
            # Calculate cosine similarity
            similarity = np.dot(resume_embedding[0], jd_embedding[0]) / (
                np.linalg.norm(resume_embedding[0]) * np.linalg.norm(jd_embedding[0])
            )
            
            # Boost similarity score slightly (semantic scores tend to be low)
            boosted_similarity = min(1.0, float(similarity) * 1.2)
            
            print(f"Debug: Semantic similarity: {similarity:.3f} -> {boosted_similarity:.3f}")
            return boosted_similarity
            
        except Exception as e:
            print(f"Semantic analysis failed: {e}")
            return self._enhanced_tfidf_similarity(resume_text, jd_text)
    
    def _enhanced_tfidf_similarity(self, text1: str, text2: str) -> float:
        """Enhanced TF-IDF similarity with better preprocessing"""
        try:
            # Preprocess texts
            text1_clean = self.clean_text(text1.lower())
            text2_clean = self.clean_text(text2.lower())
            
            # Create TF-IDF with better parameters
            tfidf = TfidfVectorizer(
                stop_words='english', 
                max_features=1000,
                ngram_range=(1, 2),  # Include bigrams
                min_df=1,
                max_df=0.95
            )
            
            # Fit TF-IDF on both texts
            tfidf_matrix = tfidf.fit_transform([text1_clean, text2_clean])
            
            # Calculate cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Boost TF-IDF scores as they tend to be lower than semantic scores
            boosted_similarity = min(1.0, float(similarity) * 1.5)
            
            print(f"Debug: TF-IDF similarity: {similarity:.3f} -> {boosted_similarity:.3f}")
            return boosted_similarity
            
        except Exception as e:
            print(f"Enhanced TF-IDF similarity failed: {e}")
            return 0.2  # Return a small positive value instead of 0
    
    def _tfidf_similarity(self, text1: str, text2: str) -> float:
        """Legacy TF-IDF similarity method"""
        return self._enhanced_tfidf_similarity(text1, text2)
    
    def generate_verdict(self, final_score: float) -> str:
        """Generate verdict based on final score with more balanced thresholds"""
        if final_score >= 0.6:  # Lowered from 0.7
            return "High"
        elif final_score >= 0.35:  # Lowered from 0.4
            return "Medium"
        else:
            return "Low"
    
    def generate_suggestions(self, missing_skills: List[str], verdict: str) -> str:
        """Generate improvement suggestions"""
        if not missing_skills:
            return "Great match! No major gaps identified."
        
        suggestions = []
        
        if verdict == "Low":
            suggestions.append("Consider gaining experience in the following key areas:")
        else:
            suggestions.append("To strengthen your profile, consider developing skills in:")
        
        # Group skills by category
        tech_skills = [skill for skill in missing_skills if any(
            tech in skill.lower() for tech in ['python', 'java', 'javascript', 'react', 'sql']
        )]
        
        soft_skills = [skill for skill in missing_skills if any(
            skill_word in skill.lower() for skill_word in ['communication', 'leadership', 'management']
        )]
        
        if tech_skills:
            suggestions.append(f"• Technical skills: {', '.join(tech_skills[:5])}")
        
        if soft_skills:
            suggestions.append(f"• Soft skills: {', '.join(soft_skills[:3])}")
        
        # Add general advice based on verdict
        if verdict == "Low":
            suggestions.append("• Consider taking relevant courses or certifications")
            suggestions.append("• Build projects that demonstrate these skills")
        elif verdict == "Medium":
            suggestions.append("• Highlight relevant experience more prominently")
            suggestions.append("• Consider adding specific examples or metrics")
        
        return "\n".join(suggestions)
    
    def analyze_relevance(self, resume_text: str, jd_text: str, 
                         hard_weight: float = 0.6, semantic_weight: float = 0.4) -> Dict:
        """Main analysis function combining hard and semantic matching"""
        
        print(f"\n=== ANALYSIS DEBUG ===")
        print(f"Resume text length: {len(resume_text)}")
        print(f"JD text length: {len(jd_text)}")
        print(f"Weights: Hard={hard_weight:.2f}, Semantic={semantic_weight:.2f}")
        
        # Hard match analysis
        hard_match = self.hard_match_analysis(resume_text, jd_text)
        hard_score = hard_match['score']
        
        # Semantic match analysis
        semantic_score = self.semantic_match_analysis(resume_text, jd_text)
        
        # Calculate final score
        final_score = (hard_weight * hard_score) + (semantic_weight * semantic_score)
        
        print(f"Scores: Hard={hard_score:.3f}, Semantic={semantic_score:.3f}, Final={final_score:.3f}")
        
        # Generate verdict
        verdict = self.generate_verdict(final_score)
        print(f"Verdict: {verdict}")
        
        # Generate suggestions
        suggestions = self.generate_suggestions(hard_match['missing_skills'], verdict)
        
        print(f"=== END DEBUG ===\n")
        
        return {
            'final_score': round(final_score, 3),
            'hard_match_score': round(hard_score, 3),
            'semantic_score': round(semantic_score, 3),
            'verdict': verdict,
            'matched_skills': hard_match['matched_skills'],
            'missing_skills': hard_match['missing_skills'],
            'suggestions': suggestions
        }