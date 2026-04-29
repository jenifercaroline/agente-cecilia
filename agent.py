import json
import requests
from prompts import SYSTEM_PROMPT
from memory import get_recent_memories


def format_memories():
    memories = get_recent_memories()

    if not memories:
        return "Nenhuma memória registrada ainda."

    formatted = []

    for raw_text, category, event_type, event_time, notes, created_at in memories:
        formatted.append(
            f"- categoria={category}; evento={event_type}; horário={event_time}; notas={notes}; texto_original={raw_text}; criado_em={created_at}"
        )

    return "\n".join(formatted)


def extract_memory_event(user_message: str) -> dict:
    prompt = f"""
Você é um extrator de eventos da rotina de uma criança.

Leia a mensagem e retorne APENAS um JSON válido.

Categorias possíveis:
- sono
- alimentacao
- saude
- rotina
- vacina
- outro

Tipos de evento possíveis:
- inicio_soneca
- fim_soneca
- acordou
- mamou
- comeu
- almocou
- jantou
- remedio
- sintoma
- vacina_aplicada
- vacina_reacao
- outro

Regras importantes:
- "foi fazer soneca", "dormiu", "tirou soneca" = inicio_soneca
- "acordou da soneca", "acordou das sonecas" = fim_soneca
- "acordou às 7h" sem mencionar soneca = acordou
- não confunda fim_soneca com inicio_soneca
- erros de digitação podem acontecer, como "soncea" significando "soneca"
- frases com "teve febre após vacina", "reação da vacina" → vacina_reacao
- frases com "tomou vacina", "foi vacinada" → vacina_aplicada


Se a mensagem NÃO for um evento relevante da rotina, retorne:
{{"should_save": false}}

Se for relevante, retorne:
{{
  "should_save": true,
  "category": "...",
  "event_type": "...",
  "event_time": "...",
  "notes": "..."
}}

Mensagem:
{user_message}
"""

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

    text = response.json().get("response", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"should_save": False, "notes": f"Erro ao interpretar JSON: {text}"}


def ask_agent(user_message: str) -> str:
    memories = format_memories()

    prompt = f"""
{SYSTEM_PROMPT}

Memórias estruturadas recentes:
{memories}

Mensagem da usuária:
{user_message}

Responda considerando as memórias quando for útil.
Se a pergunta envolver contagem, use os tipos de evento estruturados.
Exemplo:
- Para contar sonecas, conte eventos inicio_soneca.
- Não conte fim_soneca como uma nova soneca.

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