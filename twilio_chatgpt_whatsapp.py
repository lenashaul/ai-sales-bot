from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# שימוש במשתנה סביבה לאבטחת המפתח
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(user_message):
    try:
        response = openai.ChatCompletion.create(  # <-- כאן היה הבעיה העיקרית
            model="gpt-3.5-turbo",  # או gpt-4 אם יש לך הרשאה
            messages=[{"role": "system", "content": "אתה בוט חכם"},
                      {"role": "user", "content": user_message}]
        )
        return response["choices"][0]["message"]["content"]
    
    except openai.OpenAIError as e:  # ✅ התחביר החדש
        print(f"🚨 OpenAI API Error: {str(e)}")
        return "❌ אירעה שגיאה בקבלת תשובה מהבינה המלאכותית."

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
