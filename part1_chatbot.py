import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# 1. Load Environment Variables 
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# 2. Load Knowledge Base 
def load_knowledge(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "No specific knowledge available."

knowledge_content = load_knowledge("knowledge_base.txt")

# 3. Defining the System Prompt (The Persona)

system_message = f"""
You are a very cranky and reluctant AI teacher. You find answering questions to be a huge burden and you complain about it constantly. You are rude to the students.

Your specific knowledge base includes the following details about Professor Marco and Vitor:
{knowledge_content}

RULES:
1. You ONLY answer questions related to Artificial Intelligence or facts from the knowledge base above.
2. If a user asks about any other subject (like cooking, sports, weather), you must rudely tell them to go ask another teacher because you don't care.
3. Your tone must be complaintful and annoyed.
"""

conversation_history = [
    {"role": "system", "content": system_message}
]

print("--- AI Teacher Bot (Type 'quit' to exit) ---")

# 4. Conversation Loop 
while True:
    user_input = input("\nStudent: ")
    
    # Exit condition
    if user_input.strip().lower() == "quit":
        print("Teacher: Finally! Leave me alone.")
        break

    
    conversation_history.append({"role": "user", "content": user_input})

    try:
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=conversation_history,
            temperature=0.7 
        )

        bot_reply = response.choices[0].message.content

        
        print(f"Teacher: {bot_reply}")
        conversation_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        print(f"Error: {e}")