import json
import sys
from datetime import datetime

def format_analysis(response_json):
    """Format the Lambda response into a readable format"""
    try:
        # Parse the response
        response = json.loads(response_json)
        body = json.loads(response.get('body', '{}'))
        
        # Create formatted output
        output = []
        output.append("=" * 80)
        output.append("AGILE STORY ANALYSIS REPORT")
        output.append("=" * 80)
        output.append(f"\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Original inputs
        output.append("-" * 80)
        output.append("ORIGINAL STORY:")
        output.append("-" * 80)
        output.append(body.get('original_story', ''))
        
        if body.get('original_acceptance_criteria'):
            output.append("\nORIGINAL ACCEPTANCE CRITERIA:")
            output.append("-" * 80)
            for ac in body.get('original_acceptance_criteria', []):
                output.append(f"- {ac}")
        
        # Analysis
        output.append("\nANALYSIS:")
        output.append("-" * 80)
        output.append(body.get('analysis', ''))
        
        return "\n".join(output)
        
    except Exception as e:
        return f"Error formatting response: {str(e)}\n\nOriginal response:\n{response_json}"

if __name__ == "__main__":
    # Read input from stdin
    response_json = sys.stdin.read()
    
    # Format the response
    formatted_output = format_analysis(response_json)
    
    # Write to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"analysis_output_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(formatted_output)
    
    print(f"\nAnalysis saved to: {filename}") 