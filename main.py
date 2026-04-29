from agent import ask_agent, extract_memory_event
from memory import create_memory_table, save_memory


def main():
    create_memory_table()

    print("Agente da Cecília iniciado 👶")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_message = input("Você: ")

        if user_message.lower() in ["sair", "exit", "quit"]:
            print("Agente: Até mais 💛")
            break

        event = extract_memory_event(user_message)

        if event.get("should_save"):
            save_memory(
                raw_text=user_message,
                category=event.get("category"),
                event_type=event.get("event_type"),
                event_time=event.get("event_time"),
                notes=event.get("notes"),
            )

            print(
                f"💾 Memória salva: {event.get('category')} / {event.get('event_type')} / {event.get('event_time')}"
            )

        answer = ask_agent(user_message)
        print(f"\nAgente: {answer}\n")


if __name__ == "__main__":
    main()