import re
import logging
from typing import List

# Setup specialized logger for data processing
logger = logging.getLogger("DataProcessor")

class DataSanitizer:
    """
    Advanced text processor to prepare raw business data for AI/RPA consumption.
    Includes logic for PII Redaction and SQL Injection prevention.
    """

    def __init__(self):
        # Patterns for PII (Names, Emails, Phone numbers, Credit Cards)
        self.pii_patterns = {
            "email": r'[\w\.-]+@[\w\.-]+\.\w+',
            "phone": r'\+?\d{10,12}',
            "credit_card": r'\b(?:\d[ -]*?){13,16}\b',
            "uk_postcode": r'([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0AA)'
        }

    def clean_text(self, text: str) -> str:
        """
        Primary cleaning pipeline for unstructured customer input.
        """
        if not text:
            return ""

        # 1. Basic Sanitization (Remove extra whitespace/newlines)
        text = " ".join(text.split())

        # 2. PII Redaction (Crucial for GDPR compliance at Flutter UKI)
        text = self.redact_sensitive_info(text)

        # 3. SQL Injection Prevention
        # Escaping characters that could break downstream SQL transformations
        text = text.replace("'", "''").replace(";", "")

        return text

    def redact_sensitive_info(self, text: str) -> str:
        """
        Replaces sensitive data with placeholder tags to protect user privacy
        while maintaining context for the AI model.
        """
        redacted_text = text
        
        for label, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, redacted_text)
            if matches:
                logger.info(f"Redacting {len(matches)} instance(s) of {label}")
                redacted_text = re.sub(pattern, f"[{label.upper()}_REDACTED]", redacted_text)
        
        return redacted_text

    def extract_entities(self, text: str) -> List[str]:
        """
        Helper method for Business Analysts to identify keywords 
        for automated tagging in the CRM.
        """
        keywords = ["refund", "dispute", "login", "bonus", "withdrawal"]
        return [word for word in keywords if word in text.lower()]

# --- UNIT TEST SIMULATION ---
if __name__ == "__main__":
    processor = DataSanitizer()
    
    dirty_input = """
    User John Doe (john.doe@gmail.com) is complaining about a withdrawal to 
    his card 4111-2222-3333-4444. He is located in Dublin, D04 X2K7. 
    Drop table users; -- just kidding.
    """
    
    print("--- ORIGINAL INPUT ---")
    print(dirty_input)
    
    print("\n--- PROCESSED FOR AI ENGINE ---")
    clean_output = processor.clean_text(dirty_input)
    print(clean_output)