import os
import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# הגדרת מפתח ה-API של OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_chatgpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה עוזר וירטואלי שמתמחה בהמלצות על מוצרים ופתרונות מותאמים אישית."},
                {"role": "user", "content": message}
            ]
        )
        response_text = response["choices"][0]["message"]["content"].strip()
        print(f"🔹 תגובת OpenAI: {response_text}")  # הדפסת התגובה לצורך בדיקה
        return response_text
    except Exception as e:
        print(f"🚨 שגיאה בקבלת תגובה מ-OpenAI: {str(e)}")
        return "מצטער, כרגע אני לא זמין. נסה שוב מאוחר יותר."

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    response_text = get_chatgpt_response(incoming_msg)
    
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
