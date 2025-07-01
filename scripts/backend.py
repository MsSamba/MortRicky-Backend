from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import random
from typing import List, Dict, Any

app = FastAPI(title="Mort and Ricky Quiz API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store questions
quiz_questions = []

def load_questions():
    """Load questions from JSON file"""
    global quiz_questions
    try:
        with open('quiz_questions.json', 'r') as f:
            quiz_questions = json.load(f)
        print(f"Loaded {len(quiz_questions)} questions")
    except FileNotFoundError:
        print("quiz_questions.json not found. Please run question_generator.py first.")
        quiz_questions = []

# Load questions on startup
load_questions()

@app.on_event("startup")
async def startup_event():
    load_questions()

@app.get("/")
async def root():
    return {"message": "Mort and Ricky Quiz API", "total_questions": len(quiz_questions)}

@app.get("/api/questions")
async def get_all_questions():
    """Get all available questions"""
    if not quiz_questions:
        raise HTTPException(status_code=404, detail="No questions available")
    return {"questions": quiz_questions, "total": len(quiz_questions)}

@app.get("/api/quiz/{num_questions}")
async def get_quiz(num_questions: int):
    """Get a random set of questions for a quiz"""
    if not quiz_questions:
        raise HTTPException(status_code=404, detail="No questions available")
    
    if num_questions > len(quiz_questions):
        num_questions = len(quiz_questions)
    
    selected_questions = random.sample(quiz_questions, num_questions)
    
    # Remove correct answers from the response (frontend shouldn't know)
    quiz_data = []
    for q in selected_questions:
        quiz_question = {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "type": q["type"]
        }
        quiz_data.append(quiz_question)
    
    return {"questions": quiz_data, "total": len(quiz_data)}

@app.post("/api/submit-quiz")
async def submit_quiz(submission: Dict[str, Any]):
    """Submit quiz answers and get results"""
    user_answers = submission.get("answers", {})
    
    if not user_answers:
        raise HTTPException(status_code=400, detail="No answers provided")
    
    results = []
    correct_count = 0
    
    for question_id, user_answer in user_answers.items():
        # Find the original question
        original_question = next((q for q in quiz_questions if str(q["id"]) == str(question_id)), None)
        
        if original_question:
            is_correct = user_answer == original_question["correct_index"]
            if is_correct:
                correct_count += 1
            
            results.append({
                "question_id": question_id,
                "question": original_question["question"],
                "user_answer": user_answer,
                "correct_answer": original_question["correct_index"],
                "correct_answer_text": original_question["options"][original_question["correct_index"]],
                "is_correct": is_correct
            })
    
    total_questions = len(results)
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    return {
        "results": results,
        "score": {
            "correct": correct_count,
            "total": total_questions,
            "percentage": round(score_percentage, 2)
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get quiz statistics"""
    if not quiz_questions:
        return {"total_questions": 0, "question_types": {}}
    
    question_types = {}
    for q in quiz_questions:
        q_type = q.get("type", "unknown")
        question_types[q_type] = question_types.get(q_type, 0) + 1
    
    return {
        "total_questions": len(quiz_questions),
        "question_types": question_types
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
