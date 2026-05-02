from memory import search_memories, get_recent_memories, get_today_memories


def infer_search_terms(user_message):
    message = user_message.lower()
    terms = []

    if any(word in message for word in ["soneca", "dormiu", "sono", "acordou"]):
        terms.append("sono")

    if any(word in message for word in ["mamou", "comeu", "almoço", "almocou", "jantar", "jantou", "comida"]):
        terms.append("alimentacao")

    if any(word in message for word in ["febre", "vômito", "vomito", "diarreia", "remédio", "remedio", "dor"]):
        terms.append("saude")

    if any(word in message for word in ["vacina", "vacinada", "reação", "reacao"]):
        terms.append("vacina")

    return terms


def retrieve_relevant_memories(user_message):
    message = user_message.lower()

    if "hoje" in message:
        return get_today_memories()

    terms = infer_search_terms(user_message)

    memories = []

    for term in terms:
        memories.extend(search_memories(term))

    if not memories:
        memories = get_today_memories()

    return memories


def format_retrieved_memories(memories):
    if not memories:
        return "Nenhuma memória relevante encontrada."

    formatted = []

    for raw_text, category, event_type, event_time, notes, created_at in memories:
        formatted.append(
            f"- categoria={category}; evento={event_type}; horário={event_time}; notas={notes}; texto_original={raw_text}; criado_em={created_at}"
        )

    return "\n".join(formatted)