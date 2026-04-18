class KBManager:
    """Manages structured knowledge base operations"""

    def __init__(self, storage_file: str = None):
        self.articles = {}  # filename -> article data
        self.suggestions = []  # list of suggestions
        self.storage_file = storage_file

    def add_article(self, article_data: dict):
        """Add an article to the knowledge base"""
        filename = article_data.get("filename", "unknown.md")
        self.articles[filename] = article_data

    def get_article(self, filename: str) -> dict:
        """Retrieve an article from the knowledge base"""
        return self.articles.get(filename)

    def list_articles(self) -> list:
        """List all articles in the knowledge base"""
        return list(self.articles.values())

    def add_suggestion(self, suggestion):
        """Add a suggestion to the review queue"""
        self.suggestions.append(suggestion)

    def get_suggestions(self) -> list:
        """Get all suggestions pending review"""
        return self.suggestions.copy()

    def update_suggestion_status(self, filename: str, status: str):
        """Update the review status of a suggestion"""
        for suggestion in self.suggestions:
            if suggestion.suggested_filename == filename:
                suggestion.review_status = status
                break

    def save_to_file(self):
        """Save KB articles and suggestions to file"""
        if not self.storage_file:
            return

        data = {
            "articles": self.articles,
            "suggestions": [self._suggestion_to_dict(s) for s in self.suggestions]
        }

        import json
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self):
        """Load KB articles and suggestions from file"""
        if not self.storage_file:
            return

        try:
            import json
            with open(self.storage_file, 'r') as f:
                data = json.load(f)

            self.articles = data.get("articles", {})
            suggestion_dicts = data.get("suggestions", [])
            self.suggestions = [self._dict_to_suggestion(s) for s in suggestion_dicts]
        except FileNotFoundError:
            pass  # Start with empty KB if file doesn't exist

    def _suggestion_to_dict(self, suggestion) -> dict:
        """Convert KBUpdate to dictionary for serialization"""
        return {
            "question": suggestion.question,
            "answer": suggestion.answer,
            "category": suggestion.category,
            "confidence": suggestion.confidence,
            "source_ticket": suggestion.source_ticket,
            "suggested_filename": suggestion.suggested_filename,
            "review_status": suggestion.review_status
        }

    def _dict_to_suggestion(self, data: dict):
        """Convert dictionary to KBUpdate"""
        from src.agents.learning_agent import KBUpdate
        return KBUpdate(
            question=data["question"],
            answer=data["answer"],
            category=data["category"],
            confidence=data["confidence"],
            source_ticket=data["source_ticket"],
            suggested_filename=data["suggested_filename"],
            review_status=data["review_status"]
        )