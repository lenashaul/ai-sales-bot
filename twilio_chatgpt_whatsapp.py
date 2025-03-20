from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# שימוש במפתח API מהסביבה
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(user_message):
    try:
        client = openai.OpenAI()  # 🔹 התחברות ל-API לפי התחביר החדש
        response = client.chat.completions.create(  
            model="gpt-3.5-turbo",  # או gpt-4 אם יש לך הרשאה
            messages=[
                {"role": "system", "content": "אתה עוזר וירטואלי חכם."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    
    except openai.OpenAIError as e:  # ✅ שימוש בתחביר חדש לטיפול בשגיאות
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
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # שולף את ה-API Key מהסביבה

if openai.api_key is None:
    raise ValueError("🚨 API Key לא נטען כראוי. בדקו את משתני הסביבה ב-Render!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
