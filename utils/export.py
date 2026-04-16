# Export utilities for customer support automation

import csv
from typing import List, Dict, Any


def export_to_csv(tickets: List[Dict[str, Any]], file_path: str):
    """
    Export tickets to CSV file.
    
    Args:
        tickets: List of ticket dictionaries
        file_path: Path to output CSV file
    """
    if not tickets:
        # Write empty file with headers
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "ticket_id", "ticket_text", "category", "response",
                "auto_responded", "confidence", "priority"
            ])
        return
    
    # Define fieldnames
    fieldnames = ["ticket_id", "ticket_text", "category", "response", 
                  "auto_responded", "confidence", "priority"]
    
    # Write to CSV
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tickets)
