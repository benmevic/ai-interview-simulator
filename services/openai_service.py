from openai import OpenAI
from typing import List, Dict, Optional
from config import Config

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"
    
    def generate_completion(self, prompt: str, 
                          max_tokens: int = 1000,
                          temperature: float = 0.7) -> str:
        """Generate a completion using OpenAI's API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant specialized in conducting job interviews and providing professional feedback."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_interview_questions(self, 
                                    num_questions: int = 5,
                                    difficulty: str = 'medium',
                                    topic: Optional[str] = None) -> List[str]:
        """Generate interview questions."""
        topic_text = f" about {topic}" if topic else ""
        prompt = f"""Generate {num_questions} technical interview questions{topic_text}
at {difficulty} difficulty level.

Provide exactly {num_questions} questions, numbered 1-{num_questions}.
Make them clear, specific, and appropriate for a {difficulty} difficulty interview."""
        
        response = self.generate_completion(prompt)
        
        # Parse questions from response
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and formatting
                question = line.lstrip('0123456789.-) ').strip()
                if question:
                    questions.append(question)
        
        return questions[:num_questions]
    
    def evaluate_answer(self, question: str, answer: str) -> Dict[str, any]:
        """Evaluate an interview answer."""
        prompt = f"""Evaluate the following interview answer on a scale of 0-10.

Question: {question}

Answer: {answer}

Provide:
1. A score (0-10)
2. Strengths of the answer
3. Areas for improvement
4. Overall feedback

Format your response as:
Score: [number]
Strengths: [text]
Areas for Improvement: [text]
Overall Feedback: [text]"""
        
        try:
            response = self.generate_completion(prompt, max_tokens=500)
            
            # Parse the response
            score = 0
            strengths = ""
            improvements = ""
            feedback = ""
            
            for line in response.split('\n'):
                if line.startswith('Score:'):
                    try:
                        score = float(line.split(':')[1].strip())
                    except:
                        score = 5.0
                elif line.startswith('Strengths:'):
                    strengths = line.split(':', 1)[1].strip()
                elif line.startswith('Areas for Improvement:'):
                    improvements = line.split(':', 1)[1].strip()
                elif line.startswith('Overall Feedback:'):
                    feedback = line.split(':', 1)[1].strip()
            
            return {
                'score': score,
                'strengths': strengths,
                'improvements': improvements,
                'feedback': feedback,
                'raw_evaluation': response
            }
        except Exception as e:
            return {
                'score': 0,
                'strengths': '',
                'improvements': '',
                'feedback': f'Error evaluating answer: {str(e)}',
                'raw_evaluation': ''
            }
    
    def evaluate_interview(self, questions_and_answers: List[Dict[str, str]]) -> Dict[str, any]:
        """Evaluate an entire interview session."""
        qa_text = "\n\n".join([
            f"Q{i+1}: {qa['question']}\nA{i+1}: {qa['answer']}"
            for i, qa in enumerate(questions_and_answers)
        ])
        
        prompt = f"""Evaluate the following interview session. Provide an overall assessment.

{qa_text}

Provide:
1. Overall Score (0-100)
2. Strengths demonstrated across the interview
3. Areas needing improvement
4. Specific recommendations for the candidate
5. Summary feedback

Format your response clearly with these sections."""
        
        try:
            response = self.generate_completion(prompt, max_tokens=1500)
            
            # Try to extract overall score
            score = 50.0  # default
            for line in response.split('\n'):
                if 'score' in line.lower() and ':' in line:
                    try:
                        score_text = line.split(':')[1].strip()
                        score = float(''.join(filter(str.isdigit, score_text)))
                        break
                    except:
                        pass
            
            return {
                'overall_score': score,
                'evaluation_text': response,
                'success': True
            }
        except Exception as e:
            return {
                'overall_score': 0,
                'evaluation_text': f'Error during evaluation: {str(e)}',
                'success': False
            }