from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# שימוש במשתני סביבה לאבטחה
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "💡 השרת פועל! נסה /bot לשליחת הודעה."

@app.route("/bot", methods=["POST"])
def bot():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        print(f"📥 הודעה שהתקבלה: {incoming_msg}")  # Debugging log
        
        # בדיקה לוודא שהבקשה מכילה מידע
        if not incoming_msg:
            print("❌ שגיאה: לא התקבלה הודעה בתוכן הבקשה.")
            return "❌ No message received", 400
        
        # שליחת ההודעה ל-OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "אתה עוזר וירטואלי שמתמחה במכירות ושירות לקוחות."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            response_text = response["choices"][0]["message"]["content"]
            print(f"🤖 תשובת OpenAI: {response_text}")  # Debugging log
        except Exception as e:
            print(f"🚨 שגיאה בקבלת תשובה מ-OpenAI: {str(e)}")
            response_text = "❌ שגיאה בעת עיבוד הבקשה."
        
        # שליחת התגובה ללקוח
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(response_text)
        return str(resp)
    
    except Exception as e:
        print(f"🚨 שגיאה כללית בבוט: {str(e)}")
        return f"🚨 Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
