import json
import requests
from prompts import SYSTEM_PROMPT
from rag import retrieve_relevant_memories, format_retrieved_memories


def extract_memory_event(user_message: str) -> dict:
    prompt = f"""
Você é um extrator de eventos da rotina de uma criança.

Leia a mensagem e retorne APENAS um JSON válido.
Não escreva explicações fora do JSON.

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
- acordou_dia
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
- "acordou da soneca", "acordou das sonecas", "acordou da soncea" = fim_soneca
- "acordou às 7h" sem mencionar soneca = acordou_dia
- não confunda fim_soneca com inicio_soneca
- erros de digitação podem acontecer, como "soncea" significando "soneca"
- frases com "teve febre após vacina", "reação da vacina" = vacina_reacao
- frases com "tomou vacina", "foi vacinada" = vacina_aplicada

Se a mensagem NÃO for um evento relevante da rotina, retorne:
{{"should_save": false}}

Se for relevante, retorne:
{{
  "should_save": true,
  "raw_text": "{user_message}",
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


def ask_agent(user_message: str, saved_event: dict | None = None) -> str:
    relevant_memories = retrieve_relevant_memories(user_message)
    memories = format_retrieved_memories(relevant_memories)

    event_context = "Nenhum evento foi salvo agora."

    if saved_event:
        event_context = f"""
Um evento acabou de ser salvo:
- categoria={saved_event.get("category")}
- evento={saved_event.get("event_type")}
- horário={saved_event.get("event_time")}
- notas={saved_event.get("notes")}
"""

    prompt = f"""
{SYSTEM_PROMPT}

Contexto do evento atual:
{event_context}

Memórias relevantes recuperadas:
{memories}

Mensagem da usuária:
{user_message}

Regras de resposta:

TIPO 1 — Registro de evento:
- Se a mensagem for apenas um registro de rotina, responda curto.
- Exemplos de registro: "dormiu às 13h", "mamou às 10h", "passeou no shopping", "tomou vacina".
- Para registro, NÃO liste histórico.
- Para registro, NÃO faça resumo.
- Para registro, NÃO explique o sistema.
- Para registro, responda algo como: "Registrei 😊" ou "Anotado 💛".

TIPO 2 — Pergunta específica:
- Se for pergunta direta, responda direto.
- Exemplos: "quantas sonecas?", "ela mamou hoje?", "teve febre?"
- Use as memórias recuperadas.
- Não enrole.

TIPO 3 — Pergunta aberta:
- Se for algo como "como foi o dia?", "como foi a rotina?", "como foi hoje?", faça um resumo organizado.
- Agrupe por tipo quando fizer sentido: sono, alimentação, saúde, vacina, rotina.
- Use apenas memórias relevantes.

Regras gerais:
- Nunca invente eventos.
- Nunca traga memória irrelevante.
- Se a pergunta envolver "hoje", use apenas memórias de hoje.
- Se a pergunta envolver contagem, use os tipos de evento estruturados.
- Para contar sonecas, conte apenas eventos inicio_soneca.
- Não conte fim_soneca como uma nova soneca.
- Se a usuária perguntar sobre sono, priorize memórias da categoria sono.
- Se perguntar sobre vacina, priorize memórias da categoria vacina.
- Se perguntar sobre saúde, priorize memórias da categoria saude.
- Responda como uma pessoa ajudando, não como um sistema técnico.
- Seja natural, simples e breve quando possível.

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