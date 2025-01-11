import os
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import json
from ai.shared.story_analyzer import StoryAnalyzer, Story, AnalysisStatus

def print_analysis_result(result):
    """Pretty print the analysis result"""
    print("\n" + "="*80)
    print("ANALYSIS RESULT")
    print("="*80)
    
    # Handle both AnalysisResult objects and dictionaries
    if hasattr(result, 'status'):
        # It's an AnalysisResult object
        print(f"\nStatus: {result.status.value}")
        print(f"\nAnalysis:\n{result.analysis}")
        if result.improved_story:
            print(f"\nImproved Story:\n{result.improved_story.text}")
            print("\nEnhanced Acceptance Criteria:")
            for ac in result.improved_story.acceptance_criteria:
                print(f"- {ac}")
    else:
        # It's a dictionary
        print(f"\nStatus: {result['status']}")
        print(f"\nAnalysis:\n{result['analysis']}")
        if result.get('improved_story'):
            print(f"\nImproved Story:\n{result['improved_story']['text']}")
            print("\nEnhanced Acceptance Criteria:")
            for ac in result['improved_story']['acceptance_criteria']:
                print(f"- {ac}")
    
    print("\n" + "="*80 + "\n")

def get_user_input(prompt):
    """Get user input with validation"""
    while True:
        response = input(prompt).lower().strip()
        if response in ['y', 'n']:
            return response == 'y'
        print("Please enter 'y' for yes or 'n' for no")

def run_workflow():
    """Run the story analysis workflow with CLI interaction"""
    analyzer = StoryAnalyzer()
    
    # Get initial story input
    print("\nEnter your user story details:")
    story_text = input("\nStory: ")
    
    print("\nEnter acceptance criteria (one per line, empty line to finish):")
    acceptance_criteria = []
    while True:
        criterion = input()
        if not criterion:
            break
        acceptance_criteria.append(criterion)
    
    print("\nEnter context (optional, press enter to skip):")
    context = input("Context: ").strip()
    
    # Create initial story
    story = Story(
        text=story_text,
        acceptance_criteria=acceptance_criteria,
        context=context
    )
    
    # Start with Agile Coach analysis
    print("\nStarting Agile Coach analysis...")
    result = analyzer.start_analysis(story)
    print_analysis_result(result)
    
    # Handle both object and dictionary status
    status = result.status if hasattr(result, 'status') else result['status']
    if status != AnalysisStatus.ERROR:
        approved = get_user_input("\nDo you approve these changes? (y/n): ")
        
        if approved:
            # Move to technical review
            result = analyzer.process_user_feedback(result, True)
            print("\nStarting Technical review...")
            print_analysis_result(result)
            
            # Get user feedback on Technical review
            status = result.status if hasattr(result, 'status') else result['status']
            if status != AnalysisStatus.ERROR:
                approved = get_user_input("\nDo you approve the technical analysis? (y/n): ")
                if approved:
                    print("\nAnalysis complete!")
                    print_analysis_result(result)  # Just show final result
                else:
                    print("\nWould you like to edit the story?")
                    if get_user_input("Edit story? (y/n): "):
                        # Get edited story
                        print("\nEnter your edited story:")
                        edited_text = input("\nStory: ")
                        print("\nEnter edited acceptance criteria (one per line, empty line to finish):")
                        edited_ac = []
                        while True:
                            criterion = input()
                            if not criterion:
                                break
                            edited_ac.append(criterion)
                        
                        edited_story = Story(
                            text=edited_text,
                            acceptance_criteria=edited_ac,
                            context=context,
                            version=story.version + 1
                        )
                        result = analyzer.process_user_feedback(result, False, edited_story)
                    else:
                        print("\nCancelling analysis...")
                        return

if __name__ == "__main__":
    run_workflow() 