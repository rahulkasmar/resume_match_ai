import io
import fitz  # PyMuPDF
from docx import Document
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np
from groq import Groq
from groq import Groq, RateLimitError, APIError
import json
from config import GROQ_API_KEY # Use the key from your config

# --- LangChain Imports ---
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

# --- LangChain LLM Initialization ---
# Initialize the LLM client once
try:
    llm = ChatOpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model_name="llama3-70b-8192", # Corrected model name
    )
    print("✅ LangChain client initialized successfully with Groq.")
except Exception as e:
    print(f"❌ Failed to initialize LangChain client: {e}")
    llm = None

# Initialize models and clients once to save resources and startup time
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text(file_bytes: bytes, filename: str) -> str:
    """Extracts text from PDF or DOCX bytes."""
    if filename.lower().endswith(".pdf"):
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc)
    elif filename.lower().endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX.")

def get_embedding(text: str) -> np.ndarray:
    """Generates a vector embedding for the given text."""
    return embedding_model.encode(text)

# analysis/services.py

def calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculates cosine similarity and returns a percentage."""
    similarity = 1 - cosine(vec1, vec2)
    return float(round(similarity * 100, 2))


def get_llm_analysis(resume_text: str, jd_text: str) -> dict:
    """Gets missing skills and resume improvements using LangChain."""
    if not llm:
        raise ConnectionError("LangChain client is not initialized.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", 'Analyze the resume against the job description. Respond with a valid JSON object with two keys: "missing_skills" (an array of strings) and "resume_improvements" (an array of strings with 3 actionable suggestions).'),
        ("human", "JOB DESCRIPTION:\n---\n{jd}\n---\n\nRESUME:\n---\n{resume}\n---")
    ])
    
    # A chain combines the prompt, the model, and an output parser
    chain = prompt | llm | JsonOutputParser()
    
    return chain.invoke({"jd": jd_text, "resume": resume_text})

def generate_cover_letter(resume_text: str, jd_text: str) -> str:
    """Generates a tailored cover letter using LangChain."""
    if not llm:
        raise ConnectionError("LangChain client is not initialized.")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional career coach. Write an engaging and tailored cover letter based on the provided resume and job description."),
        ("human", "JOB DESCRIPTION:\n---\n{jd}\n---\n\nRESUME:\n---\n{resume}\n---")
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"jd": jd_text, "resume": resume_text})