import pytest
import tempfile
import os
from src.knowledge_base.kb_manager import KBManager
from src.agents.learning_agent import KBUpdate


def test_kb_manager_can_be_imported():
    """Test that KBManager class exists and can be instantiated"""
    manager = KBManager()
    assert manager is not None


def test_kb_manager_can_add_and_get_article():
    """Test that KBManager can store and retrieve KB articles"""
    manager = KBManager()
    article_data = {
        "question": "How do I reset my password?",
        "answer": "Go to login page and click Forgot Password",
        "category": "password_reset",
        "confidence": 0.95,
        "filename": "password_reset_guide.md"
    }

    manager.add_article(article_data)
    retrieved = manager.get_article("password_reset_guide.md")

    assert retrieved is not None
    assert retrieved["question"] == "How do I reset my password?"
    assert retrieved["answer"] == "Go to login page and click Forgot Password"


def test_kb_manager_can_list_articles():
    """Test that KBManager can list all articles"""
    manager = KBManager()
    article1 = {
        "question": "How do I reset my password?",
        "answer": "Go to login page and click Forgot Password",
        "category": "password_reset",
        "filename": "password_reset_guide.md"
    }
    article2 = {
        "question": "How do I update billing?",
        "answer": "Visit Account > Billing > Payment Methods",
        "category": "billing_inquiry",
        "filename": "billing_inquiry_guide.md"
    }

    manager.add_article(article1)
    manager.add_article(article2)

    articles = manager.list_articles()
    assert len(articles) == 2
    filenames = [article["filename"] for article in articles]
    assert "password_reset_guide.md" in filenames
    assert "billing_inquiry_guide.md" in filenames


def test_kb_manager_can_add_and_get_suggestions():
    """Test that KBManager can store and retrieve KB suggestions"""
    manager = KBManager()
    suggestion = KBUpdate(
        question="How do I reset my password?",
        answer="Go to login page and click Forgot Password",
        category="password_reset",
        confidence=0.9,
        source_ticket="How do I reset my password?",
        suggested_filename="password_reset_guide.md",
        review_status="pending"
    )

    manager.add_suggestion(suggestion)
    suggestions = manager.get_suggestions()

    assert len(suggestions) == 1
    assert suggestions[0].question == "How do I reset my password?"
    assert suggestions[0].review_status == "pending"


def test_kb_manager_can_update_suggestion_status():
    """Test that KBManager can update suggestion status"""
    manager = KBManager()
    suggestion = KBUpdate(
        question="How do I reset my password?",
        answer="Go to login page and click Forgot Password",
        category="password_reset",
        confidence=0.9,
        source_ticket="How do I reset my password?",
        suggested_filename="password_reset_guide.md",
        review_status="pending"
    )

    manager.add_suggestion(suggestion)
    manager.update_suggestion_status("password_reset_guide.md", "approved")

    suggestions = manager.get_suggestions()
    assert len(suggestions) == 1
    assert suggestions[0].review_status == "approved"


def test_kb_manager_can_save_and_load_articles():
    """Test that KBManager can persist articles to file and load them"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        storage_file = f.name

    try:
        manager = KBManager(storage_file=storage_file)
        article_data = {
            "question": "How do I reset my password?",
            "answer": "Go to login page and click Forgot Password",
            "category": "password_reset",
            "confidence": 0.95,
            "filename": "password_reset_guide.md"
        }

        manager.add_article(article_data)
        manager.save_to_file()

        # Create new manager and load from file
        new_manager = KBManager(storage_file=storage_file)
        new_manager.load_from_file()

        retrieved = new_manager.get_article("password_reset_guide.md")
        assert retrieved is not None
        assert retrieved["question"] == "How do I reset my password?"
        assert retrieved["answer"] == "Go to login page and click Forgot Password"
    finally:
        if os.path.exists(storage_file):
            os.unlink(storage_file)


def test_kb_manager_handles_missing_file_gracefully():
    """Test that KBManager handles missing storage file gracefully"""
    manager = KBManager(storage_file="/non/existent/file.json")
    # Should not raise exception
    manager.load_from_file()
    assert manager.articles == {}
    assert manager.suggestions == []


if __name__ == "__main__":
    pytest.main([__file__])