import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import story
import json
from dotenv import load_dotenv
import openai

# Add project root to Python path
project_root = str(Path(__file__).parents[2].absolute())  # Go up from backend/app/main.py to project root
print(f"Project root: {project_root}")
sys.path.append(project_root)

# Load environment variables
try:
    # First try env.json
    env_json_path = os.path.join(project_root, 'env.json')
    print(f"Looking for env.json at: {env_json_path}")
    
    with open(env_json_path, 'r') as f:
        env_vars = json.load(f)
        openai.api_key = env_vars['SeniorDevFunction']['OPENAI_API_KEY']
        openai.organization = env_vars['SeniorDevFunction']['OPENAI_ORG_ID']
        print("Loaded credentials from env.json")
except Exception as e:
    print(f"Could not load from env.json: {e}")
    
    # Try .env as fallback
    env_path = os.path.join(project_root, '.env')
    print(f"Looking for .env at: {env_path}")
    
    load_dotenv(env_path)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    openai.organization = os.getenv('OPENAI_ORG_ID')
    if openai.api_key and openai.organization:
        print("Loaded credentials from .env")
    else:
        print("Failed to load OpenAI credentials")
        sys.exit(1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(story.router, prefix="/api") 