from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self._train()

    def _train(self):
        # Messages and matching intent labels
        # TODO: use sqlite for large dataset
        training_sentences = [
            "hello", "hi", "hey", "good morning", "good evening", "howdy", "hola",
            "what appetizers do you have", "show me the appetizers", "appetizers?", "apps?", "add Spring Rolls", "give me an order of Garlic Bread", "Bruschetta please", "I'll take an order of Mozzarella Sticks",
            "can I see the main courses", "what are the main dishes", "entrees please", "dinner menu", "lunch menu", "main courses", "Pizza Margherita", "Spaghetti Bolognese", "Grilled Chicken", "Veg Burger",
            "do you have any desserts", "I'd like dessert", "cake please", "dessert please", "I want Cheesecake", "I'll take a slice of Tiramisu", "Ice Cream please", "Give me a Brownie",
            "what drinks do you have", "can I get a drink", "beverages?", "have coke", "soda please", "pop please", "Give me a Lemonade", "Water please", "I'll tak an Iced Tea", "Coffee",
            "show order", "order status", "items ordered", "items status", "current order",
            "yes", "yeah", "sure", "absolutely", "of course", "ya", "yep",
            "take off", "remove item", "remove from order", "take out the salad", "remove the pizza", "cancel the coke",
            "restart", "start over", "clear order", "clear my order", "cancel everything",
            "Show me everything", "What do you have?", "Full menu", "I have no idea", "entire menu",
            "thanks", "thank you", "that’s all", "no more", "I'm done", "that's good", "that will do me"
        ]

        intent_labels = [
            "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting",
            "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers",
            "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses",
            "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts",
            "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks",
            "show_order", "show_order", "show_order", "show_order", "show_order",
            "confirm_order", "confirm_order", "confirm_order", "confirm_order", "confirm_order", "confirm_order", "confirm_order",
            "remove_order", "remove_order", "remove_order", "remove_order", "remove_order", "remove_order",
            "clear_order", "clear_order", "clear_order", "clear_order", "clear_order",
            "full_menu", "full_menu", "full_menu", "full_menu", "full_menu",
            "thanks", "thanks", "thanks", "thanks", "thanks", "thanks", "thanks"
        ]


        X = self.vectorizer.fit_transform(training_sentences)
        self.model.fit(X, intent_labels)

    def predict_intent(self, message):
        X_test = self.vectorizer.transform([message])
        prediction = self.model.predict(X_test)[0]
        return prediction
