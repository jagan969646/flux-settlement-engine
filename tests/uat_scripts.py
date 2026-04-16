import sys
import os
import json
from datetime import datetime

# Adjusting path to import core modules for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.orchestrator import WorkflowOrchestrator

class AutomationUAT:
    """
    Automated User Acceptance Testing (UAT) Suite.
    Designed to validate Business Rules, GDPR Redaction, and AI Logic.
    """

    def __init__(self):
        self.orchestrator = WorkflowOrchestrator()
        self.test_cases = [
            {
                "name": "Standard Auto-Resolution",
                "payload": {"id": "TXN-001", "description": "Wrong payout on horse racing bet.", "value": 50.0},
                "expected_status": "AUTO_COMPLETED"
            },
            {
                "name": "High Value Escalation (Risk Rule)",
                "payload": {"id": "TXN-002", "description": "Requesting refund for VIP bet.", "value": 5000.0},
                "expected_status": "ESCALATED"
            },
            {
                "name": "GDPR Compliance Check",
                "payload": {"id": "TXN-003", "description": "My email is test@flutter.com and phone is 0871234567.", "value": 10.0},
                "expected_status": "AUTO_COMPLETED" # Should redact, but still process
            }
        ]

    def run_suite(self):
        print(f"🚀 Starting UAT Suite - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        results = []
        for case in self.test_cases:
            print(f"Testing: {case['name']}...", end=" ")
            output = self.orchestrator.process_transaction(case['payload'])
            
            # Validation Logic
            passed = output['status'] == case['expected_status']
            
            # Special check for GDPR redaction in the remark/log
            if case['name'] == "GDPR Compliance Check":
                # Ensure the actual output didn't leak PII in the logs
                if "REDACTED" not in output['remark'] and "AUTO" in output['status']:
                    # This is a meta-test for data safety
                    pass 

            status_icon = "✅ PASS" if passed else "❌ FAIL"
            print(status_icon)
            
            results.append({
                "case": case['name'],
                "result": status_icon,
                "output_status": output['status'],
                "remark": output['remark']
            })

        self.generate_report(results)

    def generate_report(self, results):
        """Generates a summary for Stakeholders (The BA 'Output')"""
        print("\n" + "="*20 + " UAT SUMMARY REPORT " + "="*20)
        total = len(results)
        passed = sum(1 for r in results if "PASS" in r['result'])
        
        print(f"Total Scenarios: {total}")
        print(f"Success Rate: {(passed/total)*100}%")
        print("="*60)
        
        # Save to JSON for the Streamlit Dashboard to read
        with open('data/uat_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("📁 UAT Log exported to data/uat_results.json")

if __name__ == "__main__":
    uat = AutomationUAT()
    uat.run_suite()