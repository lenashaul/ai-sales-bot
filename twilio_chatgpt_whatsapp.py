import openai
import requests
import os
from flask import Flask, request

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
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("products", [])
    return []

def search_product(query):
    products = get_shopify_products()
    for product in products:
        if query.lower() in product["title"].lower():
            return f"{product['title']} - {product['body_html']} במחיר של {product['variants'][0]['price']} ש\"ח."
    return "לא נמצא מוצר תואם, אולי תרצי לבדוק מוצרים דומים?"

def get_chatgpt_response(user_input):
    product_info = search_product(user_input)
    prompt = f"אתה בוט מכירות של חנות הקוסמטיקה E-L-BEAUTY. לקוח שואל: {user_input}. המידע על המוצר: {product_info}. הצע לו הצעה מעניינת!"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "אתה בוט מכירות ידידותי של חנות הקוסמטיקה E-L-BEAUTY. דבר עם הלקוח בגישה חיובית, ספק מידע רלוונטי על המוצרים, והצע הצעות משכנעות לרכישה."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body", "").strip()
    if not incoming_msg:
        return "", 200
    response_text = get_chatgpt_response(incoming_msg)
    return response_text, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
