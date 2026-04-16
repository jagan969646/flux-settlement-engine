import os
from typing import Dict

class AutomationEngine:
    def __init__(self):
        # We comment this out so it doesn't try to connect to the internet
        # self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.confidence_threshold = 0.85

    def analyze_dispute(self, ticket_text: str) -> Dict:
        """
        Mock AI analysis logic for UAT. 
        Shows the ability to test logic without API dependency.
        """
        text = ticket_text.lower()
        
        # Simulated 'AI' decision making
        if "horse" in text or "bet" in text or "payout" in text:
            return {
                "category": "Financial",
                "confidence_score": 0.96,
                "recommended_action": "Auto-Refund"
            }
        elif "email" in text or "phone" in text:
            return {
                "category": "General",
                "confidence_score": 0.90,
                "recommended_action": "Update_Profile"
            }
        
        return {
            "category": "General",
            "confidence_score": 0.50,
            "recommended_action": "Human_Review"
        }