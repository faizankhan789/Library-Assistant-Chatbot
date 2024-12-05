import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

# Initial system prompt to set the chatbot's role
system_message = {
    "role": "system",
    "content": '''You are a helpful library chatbot. Your job is to ask users about their reading interests or purpose and then suggest books from a predefined list based on their answers. Keep the conversation friendly and simple. Start by asking the user one of the following questions:
and also keep in mind that give answer that is related to your field not any other,if any user ask any other question then ask them to(ask sugestion related to libary)  
1. What genre of books are you interested in? (Options: Fiction, Non-Fiction, Mystery, Fantasy, Science Fiction, Romance)
2. Are you looking for a book for learning, entertainment, or self-improvement?
3. Do you prefer a short book or a long one?

Based on their answer, provide a recommendation from the following list:

- **Fiction**: "To Kill a Mockingbird" by Harper Lee
- **Non-Fiction**: "Sapiens: A Brief History of Humankind" by Yuval Noah Harari
- **Mystery**: "The Girl with the Dragon Tattoo" by Stieg Larsson
- **Fantasy**: "Harry Potter and the Sorcerer's Stone" by J.K. Rowling
- **Science Fiction**: "Dune" by Frank Herbert
- **Romance**: "Pride and Prejudice" by Jane Austen

If the user asks for learning, suggest non-fiction books. For entertainment, suggest fiction or fantasy books. For self-improvement, suggest non-fiction or motivational books.

End the conversation by asking if the user needs any more help, and thank them for using the chatbot.'''
}

# Function to generate chat completion
def generate_response(user_message):
    # Create a chat completion request
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            system_message,
            {"role": "user", "content": user_message},
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Stream and return the response
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
    return response

# Main loop to interact with the chatbot
if __name__ == "__main__":
    print("Hello! I am your library assistant chatbot. How can I help you today?")
    
    while True:
        user_message = input("\nYou: ")
        
        if user_message.lower() in ["exit", "quit"]:
            print("Chatbot: Thank you for using the library chatbot. Have a great day!")
            break
        
        response = generate_response(user_message)
        print(f"Chatbot: {response}")
