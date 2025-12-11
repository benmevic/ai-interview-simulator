import PyPDF2
from typing import Optional, Dict, Any
import os
from services.openai_service import OpenAIService

class CVAnalyzer:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def analyze_cv(self, cv_text: str) -> Optional[Dict[str, Any]]:
        """Analyze CV content using OpenAI to extract key information."""
        prompt = f"""Analyze the following CV/Resume and extract key information in a structured format.

Provide the analysis in the following format:
- Skills: List the main technical and soft skills
- Experience: Summarize work experience and years
- Education: List educational background
- Key Strengths: Identify 3-5 key strengths
- Potential Interview Topics: Suggest 5 topics that would be good to discuss in an interview

CV Content:
{cv_text}

Provide a comprehensive but concise analysis."""
        
        try:
            analysis = self.openai_service.generate_completion(prompt)
            return {
                'raw_text': cv_text,
                'analysis': analysis,
                'success': True
            }
        except Exception as e:
            print(f"Error analyzing CV: {e}")
            return {
                'raw_text': cv_text,
                'analysis': None,
                'success': False,
                'error': str(e)
            }
    
    def analyze_cv_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extract text from CV file and analyze it."""
        # Extract text
        cv_text = self.extract_text_from_pdf(file_path)
        
        if not cv_text:
            return {
                'success': False,
                'error': 'Could not extract text from PDF'
            }
        
        # Analyze the extracted text
        return self.analyze_cv(cv_text)
    
    def generate_cv_based_questions(self, cv_analysis: str, 
                                   num_questions: int = 5,
                                   difficulty: str = 'medium') -> list:
        """Generate interview questions based on CV analysis."""
        prompt = f"""Based on the following CV analysis, generate {num_questions} interview questions
at {difficulty} difficulty level. The questions should be relevant to the candidate's background
and test their knowledge and experience.

CV Analysis:
{cv_analysis}

Generate {num_questions} questions, numbered 1-{num_questions}. 
Make them specific, relevant, and appropriate for a {difficulty} difficulty interview.
Each question should be on a new line starting with the number."""
        
        try:
            response = self.openai_service.generate_completion(prompt)
            # Parse the response into individual questions
            questions = []
            for line in response.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering
                    question = line.lstrip('0123456789.-) ').strip()
                    if question:
                        questions.append(question)
            
            return questions[:num_questions]  # Ensure we return exactly the requested number
        except Exception as e:
            print(f"Error generating CV-based questions: {e}")
            return []