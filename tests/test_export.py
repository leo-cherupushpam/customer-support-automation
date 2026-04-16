# Tests for export functionality

import pytest
import csv
import tempfile
import os
from utils.export import export_to_csv


class TestExportToCSV:
    """Test CSV export functionality"""

    def setup_method(self):
        """Create temporary file for each test"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv')
        self.temp_file.close()

    def teardown_method(self):
        """Clean up temp file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_export_single_ticket(self):
        """Test exporting a single ticket"""
        tickets = [
            {
                "ticket_id": "1",
                "ticket_text": "I forgot my password",
                "category": "password_reset",
                "response": "Thank you for contacting us...",
                "auto_responded": True,
                "confidence": 0.9,
                "priority": "low"
            }
        ]
        
        export_to_csv(tickets, self.temp_file.name)
        
        # Read back and verify
        with open(self.temp_file.name, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 1
        assert rows[0]["ticket_id"] == "1"
        assert rows[0]["category"] == "password_reset"

    def test_export_multiple_tickets(self):
        """Test exporting multiple tickets"""
        tickets = [
            {
                "ticket_id": "1",
                "ticket_text": "I forgot my password",
                "category": "password_reset",
                "response": "Response 1",
                "auto_responded": True,
                "confidence": 0.9,
                "priority": "low"
            },
            {
                "ticket_id": "2",
                "ticket_text": "I was charged twice",
                "category": "billing_inquiry",
                "response": "Response 2",
                "auto_responded": False,
                "confidence": 0.7,
                "priority": "high"
            }
        ]
        
        export_to_csv(tickets, self.temp_file.name)
        
        # Read back and verify
        with open(self.temp_file.name, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]["ticket_id"] == "1"
        assert rows[1]["ticket_id"] == "2"

    def test_export_preserves_special_characters(self):
        """Test that special characters are preserved"""
        tickets = [
            {
                "ticket_id": "1",
                "ticket_text": "I was charged $99.99! @#$%",
                "category": "billing_inquiry",
                "response": "Thank you! We'll help.",
                "auto_responded": False,
                "confidence": 0.8,
                "priority": "high"
            }
        ]
        
        export_to_csv(tickets, self.temp_file.name)
        
        # Read back and verify
        with open(self.temp_file.name, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert "$99.99" in rows[0]["ticket_text"]
        assert "@" in rows[0]["ticket_text"]

    def test_export_headers(self):
        """Test that export includes correct headers"""
        tickets = [
            {
                "ticket_id": "1",
                "ticket_text": "Test",
                "category": "general",
                "response": "Test response",
                "auto_responded": True,
                "confidence": 0.8,
                "priority": "medium"
            }
        ]
        
        export_to_csv(tickets, self.temp_file.name)
        
        # Read headers
        with open(self.temp_file.name, 'r') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
        
        expected_headers = ["ticket_id", "ticket_text", "category", "response", 
                          "auto_responded", "confidence", "priority"]
        
        for header in expected_headers:
            assert header in headers

    def test_export_empty_list(self):
        """Test exporting empty ticket list"""
        export_to_csv([], self.temp_file.name)
        
        # File should exist but be empty or have headers only
        with open(self.temp_file.name, 'r') as f:
            content = f.read()
        
        assert len(content) > 0  # Should have at least headers
