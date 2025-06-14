from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents import qa_agent_respond

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Airline API server is running."}

@app.get("/chat")
def chat_get():
    return {"detail": "Use POST /chat with a JSON body { 'query': 'your question' }."}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    response = qa_agent_respond(user_query)
    return {"response": response}
