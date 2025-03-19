from flask import Flask, request
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# שימוש במשתני סביבה לאבטחה
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/bot", methods=["POST"])
def bot():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        
        # הוספת בדיקה לוודא שהבקשה מכילה מידע
        if not incoming_msg:
            return "No message received", 400
        
        # שליחת הודעת בדיקה חזרה ל-Twilio
        response_text = f"הודעה התקבלה: {incoming_msg}"

        resp = MessagingResponse()
        msg = resp.message()
        msg.body(response_text)

        return str(resp)
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
