import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parents[1].absolute()
sys.path.append(str(project_root))

from ai.shared.story_analyzer import StoryAnalyzer

# Test data from actual output
test_analysis_result = {
    "original_story": {
        "text": "passwords reset every 90 days",
        "acceptance_criteria": [
            "notice must be given"
        ],
        "context": "security audits",
        "version": 1
    },
    "improved_story": None,
    "analysis": "INVEST Analysis:\n- Independent: The user story seems to be independent...",
    "suggestions": {},
    "status": "agile_review",
    "timestamp": "2025-01-11T05:28:33.275504"
}

def test_feedback():
    """Test the feedback processing"""
    analyzer = StoryAnalyzer()
    
    print("\n=== Testing Approve Feedback ===")
    result = analyzer.process_user_feedback(test_analysis_result, approved=True)
    print("\nApprove Result:", result)
    
    print("\n=== Testing Reject Feedback ===")
    result = analyzer.process_user_feedback(test_analysis_result, approved=False)
    print("\nReject Result:", result)

if __name__ == "__main__":
    test_feedback() 