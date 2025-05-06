import os
import argparse
import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("groq_api_key"))

def fetch_website_content(url):
  
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        text_content = ' '.join([element.get_text().strip() for element in paragraphs])
        
        return text_content if text_content else None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website content: {e}")
        return None

def process_content(text, max_length=28000):
    
    cleaned_text = ' '.join(text.split())
    return cleaned_text[:max_length] if len(cleaned_text) > max_length else cleaned_text

def generate_chat_response(user_input, context):
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"Answer questions using only this context: {context}. If unsure, say you don't know."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            model="llama3-70b-8192",
            temperature=0.4,
            max_tokens=150
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Chatbot using Groq')
    parser.add_argument('url', type=str, help='URL of the website to analyze')
    args = parser.parse_args()

    raw_text = fetch_website_content(args.url)
    if not raw_text:
        print("Failed to retrieve website content. Please check the URL.")
        return

    processed_text = process_content(raw_text)
    print(f"\nGroq Chatbot initialized with content from {args.url}")
    print("Type 'exit' to end the conversation.\n")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            bot_response = generate_chat_response(user_input, processed_text)
            print("\nBot:", bot_response, "\n")
            
        except KeyboardInterrupt:
            print("\nConversation ended.")
            break

if __name__ == "__main__":
    main()
    