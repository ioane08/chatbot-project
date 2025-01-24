import openai
import datetime
from numpy import dot
from numpy.linalg import norm
import json

# Set up the OpenAI API key
openai.api_key = ""



def get_text_embedding(user_input):
    # Get the embedding for the user's input using text-embedding-ada-002 model
    response = openai.Embedding.create(
        model="text-embedding-ada-002",  # This is the model for text embeddings
        input=user_input
    )

    # Extract the embeddings from the response
    embeddings = response['data'][0]['embedding']
    return embeddings

def get_chat_response(user_input):
    # Get a response from OpenAI's chat model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with "gpt-4" if desired
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response["choices"][0]["message"]["content"]

def chat_with_openai():
    print("Hello! I am your chatbot. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        # Get the embedding for the user's input
        embeddings = get_text_embedding(user_input)

        # You can now do something with the embeddings, like storing or comparing them
        print(f"Embedding: {embeddings}")  # This prints out the embedding (a list of numbers)


def save_conversation(conversation):
    with open("chat_log.txt", "a") as file:
        for line in conversation:
            file.write(line + "\n")


def save_knowledge(question, answer):
    with open("knowledge_base.txt", "a") as file:
        file.write(f"{question}|{answer}\n")


def load_knowledge():
    knowledge = {}
    try:
        with open("knowledge_base.txt", "r") as file:
            for line in file:
                question, answer = line.strip().split("|")
                knowledge[question.lower()] = answer
    except FileNotFoundError:
        pass
    return knowledge


def math(operation, num1, num2):
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        return num1 / num2 if num2 != 0 else "Error: Division by zero"
    else:
        return "Unknown operation"

def cosine_similarity(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def load_knowledge_with_embeddings():
    knowledge = {}
    try:
        with open("knowledge_base.json", "r") as file:
            knowledge = json.load(file)
    except FileNotFoundError:
        pass
    return knowledge

def save_knowledge_with_embeddings(question, embedding, answer):
    knowledge = load_knowledge_with_embeddings()
    knowledge[question] = {"embedding": embedding, "answer": answer}
    with open("knowledge_base.json", "w") as file:
        json.dump(knowledge, file)

def find_best_match(embedding, knowledge):
    max_similarity = -1
    best_match = None
    for question, data in knowledge.items():
        stored_embedding = data["embedding"]
        similarity = cosine_similarity(embedding, stored_embedding)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = (question, data["answer"])
    return best_match, max_similarity

    
def chatbot():
    conversation = []
    knowledge = load_knowledge_with_embeddings()
    conversation_history = [{"role": "system", "content": "You are a helpful assistant."}]
    
    print("Hello! I am your chatbot. What's your name?")
    name = input("You: ")
    print(f"Chatbot: Nice to meet you, {name}!")

    while True:
        print("\nYou can ask me anything or type 'quit' to exit.")
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chatbot: Goodbye! Have a great day!")
            break

        # Get embedding for the input
        embedding = get_text_embedding(user_input)

        # Find best match from the knowledge base
        best_match, similarity = find_best_match(embedding, knowledge)

        if similarity > 0.8:
            print(f"Chatbot: {best_match}")
        else:
            # Use GPT for a response
            chatbot_reply = get_chat_response(user_input)
            print(f"Chatbot: {chatbot_reply}")

            # Ask the user if GPT's response was helpful
            print("Chatbot: Was my response helpful? (yes/no)")
            feedback = input("You: ").lower()
            if feedback == "no":
                print("Chatbot: What is the correct answer?")
                correct_answer = input("You: ")
                save_knowledge_with_embeddings(user_input, embedding, correct_answer)
                print("Chatbot: Thank you! I'll remember that for the future.")
            else:
                save_knowledge_with_embeddings(user_input, embedding, chatbot_reply)

            


    save_conversation(conversation)

# Start the chatbot
if __name__ == "__main__":
    chatbot()
