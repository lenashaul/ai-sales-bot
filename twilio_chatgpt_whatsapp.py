import openai
import requests
import os
import logging
from flask import Flask, request, jsonify

# הגדרת קובץ לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# הגדרות מפתחות API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SHOPIFY_STORE_URL = "https://62c2a3-d7.myshopify.com"
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

openai.api_key = OPENAI_API_KEY

def get_shopify_products():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2023-04/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("products", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Shopify API Error: {e}")
        return []

def search_product(query):
    products = get_shopify_products()
    for product in products:
        if query.lower() in product["title"].lower():
            return f"{product['title']} - {product['body_html']} במחיר של {product['variants'][0]['price']} ש"ח."
    return "לא נמצא מוצר תואם, אולי תרצי לבדוק מוצרים דומים?"

def get_chatgpt_response(user_input):
    product_info = search_product(user_input)
    prompt = f"אתה בוט מכירות של חנות הקוסמטיקה E-L-BEAUTY. לקוח שואל: {user_input}. המידע על המוצר: {product_info}. הצע לו הצעה מעניינת!"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה בוט מכירות ידידותי של חנות הקוסמטיקה E-L-BEAUTY. ספק מידע רלוונטי על המוצרים והצע הצעות משכנעות לרכישה."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"OpenAI API Error: {e}")
        return "מצטער, יש כרגע בעיה במערכת. נסה שוב מאוחר יותר."

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body", "").strip()
    if not incoming_msg:
        return "", 200
    response_text = get_chatgpt_response(incoming_msg)
    return jsonify({"response": response_text}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
