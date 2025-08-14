from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from typing import List
import traceback

from auth.utils import get_current_user
from database import get_analysis_collection
from . import services
from .schemas import AnalysisResponse, AnalysisHistoryItem

router = APIRouter(prefix="/analysis", tags=["AI Analysis"])

@router.post("/", response_model=AnalysisResponse)
async def analyze_resume_and_jd(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    collection: Collection = Depends(get_analysis_collection)
):
    """
    Accepts a resume file and job description to perform a full analysis
    and saves the result to the user's history.
    """
    try:
        # 1. Extract text
        resume_bytes = await resume_file.read()
        resume_text = services.extract_text(resume_bytes, resume_file.filename)
        if not resume_text or not resume_text.strip():
            raise ValueError("Failed to extract any text from the uploaded document.")

        # 2. Vectorize and calculate similarity
        resume_vec = services.get_embedding(resume_text)
        jd_vec = services.get_embedding(job_description)
        match_score = services.calculate_similarity(resume_vec, jd_vec)
        
        # 3. Get LLM analysis and generate cover letter
        llm_analysis = services.get_llm_analysis(resume_text, job_description)
        cover_letter = services.generate_cover_letter(resume_text, job_description)

        # 4. Prepare the document to be saved in the database
        analysis_document = {
            "user_id": ObjectId(current_user["user_id"]),
            "analyzed_at": datetime.utcnow(),
            "match_score": match_score,
            "missing_skills": llm_analysis.get("missing_skills", []),
            "resume_suggestions": llm_analysis.get("resume_improvements", []),
            "generated_cover_letter": cover_letter,
        }
        
        # 5. Insert the document into the MongoDB collection
        collection.insert_one(analysis_document)

        # 6. Return the final response
        return AnalysisResponse(**analysis_document)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An internal error occurred during analysis.")

@router.get("/history", response_model=List[AnalysisHistoryItem])
def get_analysis_history(
    current_user: dict = Depends(get_current_user),
    collection: Collection = Depends(get_analysis_collection)
):
    user_id_obj = ObjectId(current_user["user_id"])
    results = collection.find({"user_id": user_id_obj}).sort("analyzed_at", -1)
    
    history = []
    for result in results:
        history.append(AnalysisHistoryItem(id=str(result["_id"]), **result))
    return history