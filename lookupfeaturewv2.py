#lookup feature needs v2 authnetication which wont work because of callback url approval
@app.route('/lookup_user/<username>')
def lookup_user(username):
    return lookup_user_internal(username)

def lookup_user_internal(username):
    oauth = get_oauth_session()
    url = f'https://api.twitter.com/2/users/by/username/{username}'
    response = oauth.get(url)
    user_data = response.json()
    print(f"User data: {user_data}")

    openai_summary_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize the following user data: {user_data}"}
        ]
    )

    summary = openai_summary_response.choices[0]['message']['content'].strip()
    print(f"OpenAI summary: {summary}")
    return jsonify({"user_data": user_data, "summary": summary})