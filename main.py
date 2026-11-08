import os
# No início do main.py:
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY não encontrada no .env")

# O cliente OpenAI consegue ligar-se diretamente ao endpoint do Groq
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Dentro da função chat_endpoint():
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # Modelo gratuito e muito competente em física/matemática
    messages=formatted_messages,
    temperature=0.3,
)
