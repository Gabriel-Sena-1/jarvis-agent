from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import chatbot
from app.services.chatbot_service import ChatbotService

# Carregar variáveis de ambiente do .env
load_dotenv()

# Instância global do ChatbotService para compartilhar RAG
chatbot_service = ChatbotService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Iniciando Jarvis Chatbot API...")
    print("📚 Carregando documentos para o RAG...")
    await chatbot_service.warmup()
    stats = chatbot_service.get_rag_stats()
    print(f"✅ RAG pronto! {stats['total_chunks']} chunks carregados")
    print(f"📁 Documentos: {', '.join(stats['documentos']) if stats['documentos'] else 'Nenhum'}")
    
    yield
    
    # Shutdown
    print("🛑 Encerrando Jarvis Chatbot API...")


app = FastAPI(
    title="Jarvis Chatbot API",
    description="API REST para um chatbot inteligente com RAG",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chatbot.router)


@app.get("/", tags=["health"])
async def root():
    """Health check da API"""
    return {"message": "Jarvis Chatbot API is running"}


@app.get("/health", tags=["health"])
async def health():
    """Endpoint de health check"""
    return {"status": "healthy"}


@app.get("/stats", tags=["info"])
async def stats():
    """Retorna estatísticas do RAG"""
    return chatbot_service.get_rag_stats()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
