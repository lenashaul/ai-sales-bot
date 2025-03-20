import os
import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Shopify API Credentials
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")
SHOPIFY_ADMIN_API_KEY = os.getenv("SHOPIFY_ADMIN_API_KEY")
SHOPIFY_ADMIN_API_SECRET = os.getenv("SHOPIFY_ADMIN_API_SECRET")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_shopify_products():
    url = f"{SHOPIFY_STORE_URL}/admin/api/2024-01/products.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        products = response.json()["products"]
        return products
    return []

def get_product_by_name(product_name):
    products = get_shopify_products()
    for product in products:
        if product_name.lower() in product["title"].lower():
            return product
    return None

def get_chatgpt_response(message):
    try:
        # Check if user is asking about a product
        product = get_product_by_name(message)
        if product:
            product_info = f"{product['title']} - {product['body_html']} במחיר של {product['variants'][0]['price']} ש"ח."
            return f"מצאתי את המוצר שמתאים לך! {product_info}"
        
        # If no product was found, default to OpenAI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "אתה בוט מכירות שעוזר ללקוחות לרכוש מוצרים מחנות Shopify"},
                      {"role": "user", "content": message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"מצטער, יש תקלה זמנית: {str(e)}"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.json.get("message", "")
    response_text = get_chatgpt_response(incoming_msg)
    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
