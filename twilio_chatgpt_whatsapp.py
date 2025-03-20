import openai
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# הגדרת Flask
app = Flask(__name__)

# יצירת חיבור ל-OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# פונקציה לקבלת תגובה מבוססת OpenAI
def get_chatgpt_response(incoming_msg):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה עוזר וירטואלי חכם למכירות ושירות לקוחות"},
                {"role": "user", "content": incoming_msg}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"🚨 שגיאה בקבלת תגובה מ-OpenAI: {e}")
        return "מצטער, כרגע אני לא זמין. נסה שוב מאוחר יותר."

# נתיב ל-WhatsApp Webhook
@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"🔹 הודעה נכנסת: {incoming_msg}")
    
    response_text = get_chatgpt_response(incoming_msg)
    print(f"🔹 תגובת OpenAI: {response_text}")
    
    # שליחת תגובה ל-Twilio
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

# הפעלת האפליקציה
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
