from flask import Flask, render_template, request, jsonify
#import json
from intent_classifier import IntentClassifier
from menu_data import menu_data

app = Flask(__name__)
classifier = IntentClassifier()

# Load menu data from JSON
#def load_menu_data():
#    with open("menu.json", "r") as file:
#        return json.load(file)

#menu_data = load_menu_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    intent = classifier.predict_intent(user_message)

    if intent == "greeting":
        response = "Hello! What would you like to eat or drink today?"
    elif intent == "ask_appetizers":
        response = f"Our appetizers include: {', '.join(menu_data['appetizers'])}."
    elif intent == "ask_main_courses":
        response = f"Our main courses include: {', '.join(menu_data['main_courses'])}."
    elif intent == "ask_desserts":
        response = f"Our desserts include: {', '.join(menu_data['desserts'])}."
    elif intent == "ask_drinks":
        response = f"We offer these drinks: {', '.join(menu_data['drinks'])}."
    elif intent == "thanks":
        response = "You're welcome! Let me know if you'd like anything else."
    else:
        response = "Sorry, I didn’t quite understand that. Try asking about appetizers, drinks, or desserts!"

    return jsonify({"response": response})
