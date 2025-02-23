# ~/VOTSai/core/classifier.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import logging

logger = logging.getLogger(__name__)

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()
        self.train_data = {
            "web_search": ["weather today", "news update", "crawl f1.com", "recent events"],
            "technical": ["code python", "debug script", "build algorithm"],
            "conceptual": ["explain quantum", "what is agi", "how does ai work"],
            "comparative": ["compare deepmind vs openai", "verstappen vs hamilton"]
        }
        self._train_model()

    def _train_model(self):
        try:
            X = []
            y = []
            for intent, examples in self.train_data.items():
                X.extend(examples)
                y.extend([intent] * len(examples))
            X_vec = self.vectorizer.fit_transform(X)
            self.classifier.fit(X_vec, y)
        except Exception as e:
            logger.error(f"Classifier training failed: {e}")

    def predict(self, query: str) -> str:
        try:
            query_vec = self.vectorizer.transform([query])
            return self.classifier.predict(query_vec)[0]
        except Exception as e:
            logger.error(f"Intent prediction failed: {e}")
            return "conceptual"