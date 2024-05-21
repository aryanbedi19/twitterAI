import re
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
import openai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Twitter API
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

openai.api_key = os.getenv('OPENAI_API_KEY')

# Setup OAuth1 session
def get_oauth_session():
    return OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET
    )

@app.route('/')
def home():
    return "placeholder for a home page (this runs in terminal currently though)"

@app.route('/profile')
def profile():
    oauth = get_oauth_session()
    response = oauth.get('https://api.twitter.com/2/users/me')
    return jsonify(response.json())

@app.route('/post_tweet', methods=['POST'])
def post_tweet():
    tweet_content = request.json.get('tweet', 'Hello World!')
    return post_tweet_internal(tweet_content)

def post_tweet_internal(tweet_content):
    print(f"Posting tweet: {tweet_content}")
    oauth = get_oauth_session()
    url = 'https://api.twitter.com/2/tweets'
    payload = {'text': tweet_content}
    response = oauth.post(url, json=payload)
    print(f"Tweet post response: {response.status_code} {response.text}")
    return jsonify(response.json())

@app.route('/delete_tweet/<tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id):
    return delete_tweet_internal(tweet_id)

def delete_tweet_internal(tweet_id):
    print(f"Deleting tweet: {tweet_id}")
    oauth = get_oauth_session()
    url = f'https://api.twitter.com/2/tweets/{tweet_id}'
    response = oauth.delete(url)
    print(f"Tweet delete response: {response.status_code} {response.text}")
    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Tweet deleted successfully."})
    else:
        return jsonify({"status": "error", "message": response.json()}), response.status_code

@app.route('/get_user_info')
def get_user_info():
    oauth = get_oauth_session()
    url = 'https://api.twitter.com/2/users/me'
    response = oauth.get(url)
    return jsonify(response.json())

@app.route('/command', methods=['POST'])
def handle_command():
    user_command = request.json.get('command')
    print(f"Received command: {user_command}")

    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very helpful assistant. Respond only in the format: {action: <command>, content: '<content>'}."},
            {"role": "user", "content": user_command}
        ]
    )

    print("Full OpenAI response:")
    print(openai_response)

    action_response = openai_response.choices[0]['message']['content'].strip()
    print(f"OpenAI response: {action_response}")

    match = re.match(r"\{action:\s*(\w+),\s*content:\s*'(.+?)'\}", action_response)
    if match:
        action = match.group(1).lower() 
        content = match.group(2)

        if action in ["tweet", "post_tweet"]:
            return post_tweet_internal(content)
        elif action in ["delete_tweet"]:
            return delete_tweet_internal(content)
        else:
            return jsonify({"error": "invalid command"}), 400
    else:
        return jsonify({"error": "invalid format from openai api"}), 400

if __name__ == '__main__':
    app.run(debug=True)
