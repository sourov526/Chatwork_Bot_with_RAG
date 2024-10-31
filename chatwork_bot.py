import requests
import openai
import time
import os
from dotenv import load_dotenv
# API tokens
# CHATWORK_API_TOKEN = '70662106d5c56d0369e26ac78e11d710'
CHATWORK_API_TOKEN = os.getenv('CHATWORK_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') # github do not permit to push secret key
CHATWORK_ROOM_ID = os.getenv('CHATWORK_ROOM_ID') # Replace with the ID of your chat room
# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY
def get_chatwork_messages():
    """Get the latest messages from a specific Chatwork room."""
    url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages'
    # url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages?force=1'
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages: {response.status_code}")
        return []
def send_chatwork_message(text):
    """Send a message to the Chatwork room."""
    url = f'https://api.chatwork.com/v2/rooms/{CHATWORK_ROOM_ID}/messages'
    headers = {'X-ChatWorkToken': CHATWORK_API_TOKEN}
    payload = {'body': text}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.status_code}")
    else:
        print("Message sent to Chatwork.")
        print("Response Message: ", text)
def generate_openai_response(message):
    """Generate a response using OpenAI's GPT model."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message['content']
def main():
    processed_message_ids = set()
    print("Show the processed message ids top: ", processed_message_ids)
    # while True:
    messages = get_chatwork_messages()
    print("Show the response messages: ", len(messages))
    for message in messages:
        message_id = message['message_id']
        message_text = message['body']
        print("show the text body : ", message_text)
        # Only respond to new messages
        if message_id not in processed_message_ids:
            print(f"New message: {message_text}")
            # Send message to OpenAI for a response
            response_text = generate_openai_response(message_text)
            # Send the response back to Chatwork
            send_chatwork_message(response_text)
            # Mark this message as processed
            processed_message_ids.add(message_id)
    # Wait a bit before checking for new messages again

        time.sleep(5)

    # print("Show the processed message ids bellow: ", processed_message_ids)

if __name__ == "__main__":
    main()