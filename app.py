from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from intent_classifier import IntentClassifier
from menu_data import menu_data

import spacy
nlp = spacy.load("en_core_web_sm")

def extract_order_entities(text):
    doc = nlp(text)
    items = []
    quantity = 1
    description = []

    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }

    for token in doc:
        if token.pos_ == "NOUN":
            items.append(token.lemma_.lower())  # e.g., "breads" → "bread"
        elif token.pos_ == "ADJ":
            description.append(token.text.lower())
        elif token.like_num:
            try:
                quantity = int(token.text)
            except ValueError:
                pass
        elif token.text.lower() in number_words:
            quantity = number_words[token.text.lower()]

    return {
        "items": items,
        "description": description,
        "quantity": quantity
    }

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

"""
import sqlite3

def load_training_data(db_path="training_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sentence, label FROM training_data")
    rows = cursor.fetchall()
    conn.close()
    sentences = [row[0] for row in rows]
    labels = [row[1] for row in rows]
    return sentences, labels
"""

#app = Flask(__name__)
classifier = IntentClassifier()

COMMON_PHRASES = [
    "i want", "i would like", "i'd like", "give me", "can i have", "may i have", "i'll take"
]

def normalize_input(message):
    message = message.lower()
    for phrase in COMMON_PHRASES:
        if message.startswith(phrase):
            return message.replace(phrase, "").strip()
    return message


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    normalized_message = normalize_input(user_message)
    intent = classifier.predict_intent(normalized_message)

    print(intent)

    entities = extract_order_entities(user_message)
    response = ""

    if intent == "greeting":
        response = "Hello and welcome to Little Italy! What would you like to eat or drink today?"

    elif intent == "full_menu":
        
        response = (
            f"Our appetizers include: {', '.join(menu_data['appetizers'])}.<br>"
            f"Our main courses include: {', '.join(menu_data['main_courses'])}.<br>"
            f"Our desserts include: {', '.join(menu_data['desserts'])}.<br>"
            f"We offer these drinks: {', '.join(menu_data['drinks'])}."
        )
        
    elif intent == "ask_appetizers":
        matched_item = next((item for item in menu_data['appetizers'] if any(noun in item.lower() for noun in entities['items'])), None)
        if matched_item:
            session['pending_order'] = matched_item
            session['pending_quantity'] = entities['quantity']
            response = f"Order {entities['quantity']} {matched_item}(s)?"
        else:
            response = f"Our appetizers include: {', '.join(menu_data['appetizers'])}."

    elif intent == "ask_main_courses":
        matched_item = next((item for item in menu_data['main_courses'] if any(noun in item.lower() for noun in entities['items'])), None)
        if matched_item:
            session['pending_order'] = matched_item
            session['pending_quantity'] = entities['quantity']
            response = f"Order {entities['quantity']} {matched_item}(s)?"
        else:
            response = f"Our main courses include: {', '.join(menu_data['main_courses'])}."

    elif intent == "ask_desserts":
        matched_item = next((item for item in menu_data['desserts'] if any(noun in item.lower() for noun in entities['items'])), None)
        if matched_item:
            session['pending_order'] = matched_item
            session['pending_quantity'] = entities['quantity']
            response = f"Order {entities['quantity']} {matched_item}(s)?"
        else:
            response = f"Our desserts include: {', '.join(menu_data['desserts'])}."

    elif intent == "ask_drinks":
        matched_item = next((item for item in menu_data['drinks'] if any(noun in item.lower() for noun in entities['items'])), None)
        if matched_item:
            session['pending_order'] = matched_item
            session['pending_quantity'] = entities['quantity']
            response = f"Order {entities['quantity']} {matched_item}(s)?"
        else:
            response = f"We offer these drinks: {', '.join(menu_data['drinks'])}."

    elif intent == "confirm_order":
        item = session.get("pending_order")
        quantity = session.get("pending_quantity", 1)

        if item:
            # Get or initialize order list
            raw_order_list = session.get("order_list", [])
        
            # Upgrade any old string-based items to dict format
            order_list = []
            for entry in raw_order_list:
                if isinstance(entry, str):
                    order_list.append({"item": entry, "quantity": 1})
                else:
                    order_list.append(entry)

            # Try to update existing item
            found = False
            for entry in order_list:
                if entry["item"].lower() == item.lower():
                    entry["quantity"] += quantity
                    found = True
                    break

            # If not found, add new item
            if not found:
                order_list.append({"item": item, "quantity": quantity})

            # Update session
            session["order_list"] = order_list
            session.pop("pending_order", None)
            session.pop("pending_quantity", None)

            response = f"{quantity} {item}(s) added to your order. Anything else?"

        else:
            response = "I'm not sure what you're confirming. Can you say it again?"

    elif intent == "show_order":
        order_list = session.get("order_list", [])
        if order_list:
            lines = [f"{entry['quantity']} × {entry['item']}" for entry in order_list]
            response = "Here’s your order so far:\n" + ", ".join(lines)
        else:
            response = "You haven’t ordered anything yet."
    elif intent == "clear_order":
        session.pop("order_list", None)
        session.pop("pending_order", None)
        session.pop("pending_quantity", None)
        response = "Your order has been cleared. Would you like to start a new one?"

    elif intent == "remove_order":
        order_list = session.get("order_list", [])
        entities = extract_order_entities(user_message)
        quantity_to_remove = entities.get("quantity", 1)
        item_found = False
        updated_list = []

        for entry in order_list:
            entry_item = entry["item"].lower()

            if any(noun in entry_item for noun in entities["items"]):
                item_found = True
                if entry["quantity"] > quantity_to_remove:
                    entry["quantity"] -= quantity_to_remove
                    updated_list.append(entry)
                    response = f"Removed {quantity_to_remove} {entry['item']}(s). {entry['quantity']} left in your order."
                else:
                    response = f"Removed all {entry['item']} from your order."
                # Skip appending if quantity was removed entirely
            else:
                updated_list.append(entry)

        if not item_found:
            response = "I couldn't find that item in your order. Can you try again?"

        session["order_list"] = updated_list




    elif intent == "thanks":
        response = "You're welcome! Let me know if you'd like anything else."
    else:
        response = "Sorry, I didn’t quite understand that. Try asking about appetizers, drinks, or desserts!"

    return jsonify({"response": response})
