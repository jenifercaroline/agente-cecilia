# 👶 Agente da Cecília

Um agente de IA para auxiliar no cuidado diário de uma criança, com memória persistente e contexto dinâmico.

## 🧠 Sobre o projeto

Este projeto implementa um agente conversacional que simula um assistente pessoal para apoiar a rotina de cuidados da Cecília.

A partir de mensagens em linguagem natural, o agente é capaz de:

- interpretar eventos da rotina (sono, alimentação, saúde, etc.)
- armazenar essas informações de forma estruturada
- recuperar memórias relevantes
- responder perguntas com base no histórico

---

## 🚀 Funcionalidades

- 💬 Interface via CLI (terminal)
- 🧠 LLM local com Ollama (sem custo de API)
- 💾 Memória persistente com SQLite
- 🧾 Extração estruturada de eventos com LLM
- 🔎 Recuperação de contexto (RAG simples)
- 🧠 Respostas baseadas em histórico

---


## 🏗️ Arquitetura

Usuário (CLI)<br/>
↓<br/>
main.py (loop de interação)<br/>
↓<br/>
agent.py (extração + resposta)<br/>
↓<br/>
Ollama (llama3)<br/>
↓<br/>
Resposta<br/>

Memória:<br/>
 SQLite (memory.py)<br/>
↑<br/>
save_memory / search_memories<br/>

RAG:<br/>
 rag.py (recuperação de contexto)<br/>

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

## 💡Exemplo de uso

Você: a Cecília dormiu às 13h
Agente: Registrei 😊

Você: a Cecília acordou da soneca às 15h
Agente: Anotado 💛

Você: foram quantas sonecas?
Agente: Foi 1 soneca.

Você: como foi a rotina hoje?
Agente:
Hoje a Cecília:
- Dormiu às 13h e acordou às 15h
- Mamou às 16h

No geral, teve uma rotina tranquila 😊

## 🧠 Como funciona

O agente combina três conceitos principais:

1. Memória estruturada

Eventos são armazenados com:

categoria (sono, alimentação, saúde…)
tipo de evento (inicio_soneca, mamou…)
horário
texto original

2. Extração com LLM

O modelo interpreta mensagens como:

"a Cecília acordou da soneca às 15h"

E transforma em dados estruturados.

3. RAG (Retrieval-Augmented Generation)

O agente recupera memórias relevantes antes de responder.

Exemplo:

pergunta sobre sono → busca apenas eventos de sono
pergunta sobre "hoje" → filtra por data atual

## 📌 Próximos passos

### 🧠 Evolução do agente
- Melhorar filtros temporais (ontem, últimos dias)
- RAG com embeddings (busca semântica)
- Refinamento da classificação de eventos

### 🌐 API e integração
- Criar API com FastAPI
- Expor endpoints para interação com o agente
- Separar camada de serviço (agent) da interface

### 📱 Integração com WhatsApp
- Integrar com WhatsApp Business API
- Receber mensagens via webhook
- Permitir registrar eventos da rotina via WhatsApp
- Responder automaticamente perguntas sobre a rotina
- Evoluir para experiência de "assistente familiar"

### 🖥️ Interface
- Interface web simples
- Dashboard da rotina da criança
- Visualização de padrões (sono, alimentação, etc.)

### 🚀 Escalabilidade
- Evoluir de SQLite para banco mais robusto
- Estruturar logs e monitoramento
- Modularizar o agente para múltiplos usuários

##  📚 Aprendizados
- Uso de LLM local com Ollama
- Construção de agentes conversacionais
- Modelagem de memória estruturada
- RAG simples com SQLite
- Prompt engineering para controle de comportamento

## 👩‍💻 Autora
Jenifer,</br>
Mamãe da Cecília.