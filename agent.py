import requests
from prompts import SYSTEM_PROMPT
from memory import get_recent_memories


def format_memories():
    memories = get_recent_memories()

    if not memories:
        return "Nenhuma memória registrada ainda."

    formatted = []

    for content, created_at in memories:
        formatted.append(f"- {created_at}: {content}")

    return "\n".join(formatted)


def ask_agent(user_message: str) -> str:
    memories = format_memories()

    prompt = f"""
{SYSTEM_PROMPT}

Memórias recentes:
{memories}

Mensagem da usuária:
{user_message}

Responda considerando as memórias quando for útil.

Agente:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "Não consegui gerar uma resposta.")

    except Exception as e:
        return f"Erro ao chamar o modelo: {str(e)}"