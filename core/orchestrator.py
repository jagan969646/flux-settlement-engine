import logging
from typing import Dict, Optional
from datetime import datetime
from .engine import AutomationEngine
from .processors import DataSanitizer

# Professional Logging setup - Essential for BA Audit Trails
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [SENTINEL-ORCHESTRATOR] - %(message)s'
)

class WorkflowOrchestrator:
    def __init__(self):
        self.engine = AutomationEngine()
        self.sanitizer = DataSanitizer()
        self.max_auto_value = 500.00  # Business Rule: Cap auto-resolutions at £500
        
    def process_transaction(self, raw_payload: Dict) -> Dict:
        """
        Main entry point for the automation lifecycle.
        Steps: Sanitize -> Rule Validation -> AI Analysis -> Execution -> Audit
        """
        txn_id = raw_payload.get('id', 'UNKNOWN')
        logging.info(f"Initiating lifecycle for Transaction: {txn_id}")

        try:
            # 1. DATA SANITIZATION (Cleaning inputs for the LLM)
            clean_data = self.sanitizer.clean_text(raw_payload['description'])
            amount = raw_payload.get('value', 0.0)

            # 2. HARD BUSINESS RULES (The "BA" Guardrails)
            # This shows you don't blindly trust AI
            if amount > self.max_auto_value:
                return self._finalize_step(txn_id, "ESCALATED", "Value exceeds auto-limit threshold.")

            # 3. INTELLIGENT ANALYSIS
            analysis = self.engine.analyze_dispute(clean_data)
            
            # 4. DECISION MATRIX
            if analysis['confidence_score'] >= 0.90 and analysis['category'] != "Technical":
                # AUTO-EXECUTION PATH
                status = "AUTO_COMPLETED"
                action = f"Executed {analysis['recommended_action']}"
            else:
                # HUMAN-IN-THE-LOOP PATH
                status = "PENDING_REVIEW"
                action = "Queued for Manual SME Oversight"

            return self._finalize_step(txn_id, status, action, analysis['confidence_score'])

        except Exception as e:
            logging.error(f"Critical workflow failure on {txn_id}: {str(e)}")
            return self._finalize_step(txn_id, "FAILED", f"System Error: {str(e)}")

    def _finalize_step(self, txn_id: str, status: str, remark: str, confidence: float = 0.0) -> Dict:
        """
        Standardized output for downstream RPA bots or Dashboards.
        """
        result = {
            "transaction_id": txn_id,
            "status": status,
            "remark": remark,
            "confidence_score": confidence,
            "processed_at": datetime.now().isoformat(),
            "version": "v2.1.0-production"
        }
        logging.info(f"Finalized {txn_id} with status: {status}")
        return result

# --- QUICK TEST SIMULATION ---
if __name__ == "__main__":
    orchestrator = WorkflowOrchestrator()
    
    # Scenario: Low-value clear dispute
    test_ticket = {
        "id": "FLTR-9921",
        "description": "I placed a bet on the 3:30 at Leopardstown but the payout is wrong.",
        "value": 45.00
    }
    
    print(orchestrator.process_transaction(test_ticket))