# Azure OpenAI Implementations: Smart Agents & RAG Chatbots

This repository features two distinct AI projects built using **Azure OpenAI**. It demonstrates the transition from a specialized knowledge-retrieval chatbot to an advanced AI agent capable of controlling hardware through function calling.

---

## Project Modules

### 1. The Cranky Teacher (RAG Chatbot)
A persona-driven chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer questions based on a specific local knowledge base.
* **The Persona:** A reluctant, annoyed teacher who finds answering questions a burden.
* **Knowledge Source:** Uses `knowledge_base.txt` to provide accurate facts about:
    * **Professor Vitor Santos:** His academic background at NOVA IMS, his 15+ years of software development, and his current pursuit of a second PhD[cite: 1, 2, 4].
    * **Professor Marco Silva:** His role at Microsoft, his expertise in .Net/C#, and his leadership at "DICE Cultural"[cite: 6, 7, 9, 11].
* **Constraint:** The bot is strictly limited to AI topics and the provided faculty data; it will rudely refuse all other subjects.

### 2. Smart TV Assistant (Function Calling)
An "Agentic" AI that controls a virtual TV system using **OpenAI Tool/Function Calling**.
* **Core Logic:** The assistant translates natural language (e.g., "Turn the volume up a bit") into structured JSON commands to execute Python functions.
* **Context Awareness:** The bot understands dependencies. If the TV is **OFF**, it will automatically turn it **ON** before attempting to change channels or volume.
* **Features:** Manages power state, volume levels (0-100), brightness, and channel selection from a metadata-rich list.

---

## 🛠️ Tech Stack
* **Language:** Python 
* **AI Engine:** Azure OpenAI (GPT-4 / GPT-3.5 Models)
* **Key Libraries:** `openai`, `python-dotenv`

---

## ⚙️ Setup & Configuration

1. **Clone the Repo**
2. **Install Dependencies:**
     pip install openai python-dotenv
3. **Copy the contents of sample.env into a new file named .env and add your actual Azure credentials**
