from fastapi import FastAPI
from src.API.routes import router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="RAG Document Intelligence")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_headers=["*"],allow_methods=["*"])
app.include_router(router)
