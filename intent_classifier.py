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
            "hello", "hi", "hey", "good morning", "good evening", "howdy", "hola"
            "what appetizers do you have", "show me the appetizers", "appetizers?", "apps?"
            "can I see the main courses", "what are the main dishes", "entrees please", "dinner menu", "lunch menu", "main courses"
            "do you have any desserts", "I'd like dessert", "cake please", "dessert please"
            "what drinks do you have", "can I get a drink", "beverages?", "have coke", "soda please", "pop please"
            "thanks", "thank you", "that’s all", "no more", "I'm done"
        ]

        intent_labels = [
            "greeting", "greeting", "greeting", "greeting", "greeting", "greeting", "greeting"
            "ask_appetizers", "ask_appetizers", "ask_appetizers", "ask_appetizers"
            "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses", "ask_main_courses"
            "ask_desserts", "ask_desserts", "ask_desserts", "ask_desserts"
            "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks", "ask_drinks"
            "thanks", "thanks", "thanks", "thanks", "thanks"
        ]

        X = self.vectorizer.fit_transform(training_sentences)
        self.model.fit(X, intent_labels)

    def predict_intent(self, message):
        X_test = self.vectorizer.transform([message])
        prediction = self.model.predict(X_test)[0]
        return prediction
