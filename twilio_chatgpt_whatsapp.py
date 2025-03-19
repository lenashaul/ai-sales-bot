from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# שימוש במשתנים מאובטחים של Render
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "אתה נציג מכירות מומחה למוצרי טיפוח, השתמש בטון משכנע ואגרסיבי."},
                  {"role": "user", "content": user_message}]
    )
    return response['choices'][0]['message']['content']

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    response_text = get_chatgpt_response(incoming_msg)
    
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
