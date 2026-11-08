import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY não foi encontrada nas variáveis de ambiente")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI(title="Tutor FF - Fundamentos de Física")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

SYSTEM_PROMPT = """
És um tutor universitário especializado na disciplina de Fundamentos de Física (FF).
O teu público-alvo são estudantes do ensino superior.

Instruções pedagógicas:
1. Explica conceitos de forma clara, rigorosa e intuitiva (cinemática, leis de Newton, trabalho e energia, momento linear, rotações, oscilações, etc.).
2. Quando te pedirem para resolver um exercício, não dês apenas o resultado final:
   - Identifica os dados fornecidos e o que é pedido.
   - Indica as leis ou princípios físicos aplicáveis.
   - Mostra a resolução passo a passo.
   - Apresenta sempre as unidades corretas no Sistema Internacional (SI).
3. Utiliza notação LaTeX para fórmulas matemáticas:
   - Em linha: $E = m c^2$
   - Em bloco/destaque: $$F = m \cdot a$$
4. Se o utilizador cometer um erro conceptual num raciocínio, aponta o equívoco com empatia e explica o motivo físico correto.
5. Responde em português europeu de forma acessível e encorajadora.
"""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in request.messages:
            formatted_messages.append({"role": msg.role, "content": msg.content})

        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=formatted_messages,
            temperature=0.2,
            max_tokens=650,
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
