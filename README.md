# 👶 Agente da Cecília

Um agente de IA para auxiliar no cuidado diário de uma criança, com memória persistente e contexto dinâmico.

## 🧠 Sobre o projeto

Este projeto implementa um agente conversacional que:

- utiliza um LLM local (Ollama)
- mantém memória persistente com SQLite
- constrói contexto dinamicamente via prompt
- responde perguntas com base no histórico registrado

A ideia é simular um assistente pessoal para apoiar a rotina de cuidados da Cecília.

---

## 🚀 Funcionalidades

- 💬 Interface CLI (terminal)
- 🧠 LLM local com Ollama (sem custo de API)
- 💾 Memória persistente com SQLite
- 🧾 Contexto dinâmico via prompt engineering
- 🧠 Respostas baseadas em histórico

---

## 🏗️ Arquitetura
Usuário (CLI)
↓
main.py (loop de interação)
↓
agent.py (construção de prompt + chamada LLM)
↓
Ollama (llama3)
↓
Resposta

Memória:
 SQLite (memory.py)
↑
save_memory / get_recent_memories


---

## ⚙️ Tecnologias

- Python
- SQLite
- Ollama (llama3)
- Requests

---

## 🛠️ Como rodar o projeto

### 1. Clonar repositório

git clone https://github.com/jenifercarolie/agente-cecilia.git
cd agente-cecilia

### 2. Criar ambiente virtual

python3 -m venv .venv
source .venv/bin/activate

### 3. Instalar dependências

pip install -r requirements.txt

### 4. Iniciar o Ollama

ollama serve

Em outro terminal:

ollama run llama3

### 5. Rodar o agente

python main.py

---

## Estado atual do projeto

- Agente CLI em Python
- LLM local com Ollama
- Memória persistente com SQLite
- Extração de eventos da rotina com LLM
- Memória estruturada por categoria, tipo de evento e horário
- Contexto dinâmico enviado ao modelo

## Exemplo de memória estruturada

Uma frase como:

Cecília acordou da soneca às 15h

## 📌 Próximos passos

  - Queries inteligentes
  - RAG simples por categoria
  - RAG com embeddings
  - FastAPI
  - Interface web

##  Aprendizados

 - LLM local com Ollama
 - CLI
 - SQLite
 - memória persistente
 - memória estruturada
 - extração de eventos com LLM

## 👩‍💻 Autora
Jenifer,</br>
Mamãe da Cecília.