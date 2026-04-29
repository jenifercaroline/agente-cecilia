from agent import ask_agent
from memory import create_memory_table, save_memory


def main():
    print("Agente da Cecília iniciado 👶")
    print("Digite 'sair' para encerrar.\n")
    create_memory_table()
    while True:
        user_message = input("Você: ")

        if user_message.lower() in ["sair", "exit", "quit"]:
            print("Agente: Até mais 💛")
            break

        if user_message.lower().startswith("registrar:"):
            content = user_message.replace("registrar:", "").strip()
            save_memory(content)
            print("\nAgente: Memória salva 💛\n")
            continue

        answer = ask_agent(user_message)
        print(f"\nAgente: {answer}\n")



if __name__ == "__main__":
    main()