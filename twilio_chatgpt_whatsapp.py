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

def get_chatgpt_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "אתה עוזר וירטואלי."},
                {"role": "user", "content": user_message}
            ]
        )
        return response['choices'][0]['message']['content']
    
    except openai.error.OpenAIError as e:
        return f"⚠ שגיאת OpenAI: {str(e)}"

@app.route("/bot", methods=["POST"])
def bot():
    try:
        incoming_msg = request.values.get("Body", "").strip()
        
        if not incoming_msg:
            return "❌ No message received", 400
        
        response_text = get_chatgpt_response(incoming_msg)

        resp = MessagingResponse()
        msg = resp.message()
        msg.body(response_text)

        return str(resp)
    
    except Exception as e:
        return f"🚨 שגיאה בשרת: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
