import openai
import datetime

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
    
def chatbot():
    conversation = []
    knowledge = load_knowledge()
    print("Hello! I am your chatbot. What's your name?")
    conversation.append("Chatbot: Hello! I am your chatbot. What's your name?")

    name = input("You: ")
    conversation.append(f"You: {name}")
    print(f"Chatbot: Nice to meet you, {name}!")
    conversation.append(f"Chatbot: Nice to meet you, {name}!")

    while True:
        print("\nYou can ask me about my features or type 'quit' to exit.")
        user_input = input("You: ")
        conversation.append(f"You: {user_input}")

        if user_input.lower() == "quit":
            print("Chatbot: Goodbye! Have a great day!")
            conversation.append("Chatbot: Goodbye! Have a great day!")
            break
        elif user_input.lower() in knowledge:
            answer = knowledge[user_input.lower()]
            print(f"Chatbot: {answer}")
            conversation.append(f"Chatbot: {answer}")
        elif user_input.lower().startswith("calculate"):
            try:
                _, operation, num1, num2 = user_input.split()
                num1, num2 = float(num1), float(num2)
                result = math(operation.lower(), num1, num2)
                print(f"Chatbot: The result is {result}")
                conversation.append(f"Chatbot: The result is {result}")
            except ValueError:
                print("Chatbot: Please use the format 'calculate add/subtract/multiply/divide num1 num2'")
                conversation.append("Chatbot: Please use the format 'calculate add/subtract/multiply/divide num1 num2'")
        else:
            print("Chatbot: Sorry, I didn't understand that. Can you teach me the correct answer?")
            conversation.append("Chatbot: Sorry, I didn't understand that. Can you teach me the correct answer?")
            correct_answer = input("You: ")
            conversation.append(f"You: {correct_answer}")
            save_knowledge(user_input, correct_answer)
            knowledge[user_input.lower()] = correct_answer
            print("Chatbot: Thank you! I'll remember that for the future.")
            conversation.append("Chatbot: Thank you! I'll remember that for the future.")


    save_conversation(conversation)

# Start the chatbot
if __name__ == "__main__":
    chatbot()