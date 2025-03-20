import openai
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# קבלת המפתח הסודי של OpenAI מסביבת העבודה
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("🚨 API Key לא נטען כראוי. בדקו את משתני הסביבה ב-Render!")

openai.api_key = OPENAI_API_KEY

def get_chatgpt_response(user_message, conversation_history=[]):
    """שליחת הודעה ל-GPT וקבלת תשובה"""
    try:
        conversation_history.append({"role": "user", "content": user_message})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ניתן לשדרג ל-GPT-4 בהמשך
            messages=conversation_history
        )
        
        reply = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"❌ שגיאה בקבלת תשובה מהבינה המלאכותית: {str(e)}"

@app.route('/bot', methods=['POST'])
def bot():
    """קבלת הודעות מהמשתמש והחזרת תשובות"""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"response": "אנא הקלד הודעה."})
        
        response_text = get_chatgpt_response(user_message)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"❌ שגיאה פנימית: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
