import requests
import openai
import os
from dotenv import load_dotenv

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

def handler(request):
    messages = get_chatwork_messages()
    processed_message_ids = set()  # For example, store this in a database in production
    responses = []
    for message in messages:
        message_id = message['message_id']
        message_text = message['body']
        if message_id not in processed_message_ids:
            response_text = generate_openai_response(message_text)
            send_chatwork_message(response_text)
            processed_message_ids.add(message_id)
            responses.append({"id": message_id, "response": response_text})
    return {"status": "success", "responses": responses}
