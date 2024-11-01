import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()

CHATWORK_API_TOKEN = os.getenv('CHATWORK_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHATWORK_ROOM_ID = os.getenv('CHATWORK_ROOM_ID')

openai.api_key = OPENAI_API_KEY

def get_chatwork_messages():
    url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages'
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages: {response.status_code}")
        return []

def send_chatwork_message(text):
    url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages'
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN}
    payload = {'body': text}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}")
    else:
        print("Message sent to Chatwork.")

def generate_openai_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message['content']

def main():
    processed_message_ids = set()
    messages = get_chatwork_messages()
    print("Received messages:", len(messages))
    for message in messages:
        message_id = message['message_id']
        message_text = message['body']

        # Only respond to new messages
        if message_id not in processed_message_ids:
            print(f"New message: {message_text}")
            # Generate a response using OpenAI
            response_text = generate_openai_response(message_text)
            # Send the response back to Chatwork
            send_chatwork_message(response_text)
            # Mark this message as processed
            processed_message_ids.add(message_id)

        # Optional delay to avoid rapid requests (adjust as needed)
        time.sleep(3)

if __name__ == "__main__":
    main()
