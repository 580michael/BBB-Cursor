#!/usr/bin/env python3
"""
Test script for FAQ parser
"""

import random

def load_faqs():
    """
    Load FAQs from the FAQ.md file
    """
    try:
        faq_file = "FAQ.md"
        
        with open(faq_file, "r") as f:
            content = f.read()
        
        # Parse questions and answers
        faqs = []
        lines = content.strip().split("\n")
        
        # Skip the title line
        current_question = None
        current_answer = ""
        
        for line in lines[1:]:
            line = line.strip()
            if not line:
                # Empty line separates Q&A
                if current_question and current_answer:
                    faqs.append({
                        "question": current_question,
                        "answer": current_answer.strip()
                    })
                    current_question = None
                    current_answer = ""
            elif not current_question:
                # This is a question
                current_question = line
            else:
                # This is part of the answer
                current_answer += line + " "
        
        # Add the last FAQ if it exists
        if current_question and current_answer:
            faqs.append({
                "question": current_question,
                "answer": current_answer.strip()
            })
        
        return faqs
    except Exception as e:
        print(f"Error loading FAQs: {str(e)}")
        return []

def select_random_faqs(faqs, state_name, count=5):
    """
    Select random FAQs and customize them for the state
    """
    if len(faqs) <= count:
        selected_faqs = faqs
    else:
        selected_faqs = random.sample(faqs, count)
    
    # Customize FAQs with state information
    customized_faqs = []
    for faq in selected_faqs:
        question = faq["question"]
        answer = faq["answer"]
        
        # Replace state name
        question = question.replace("[state_name]", state_name)
        answer = answer.replace("[state_name]", state_name)
        
        # Replace premium rate (10% for TX, FL, CA; 15% for others)
        premium_rate = "10" if state_name in ["Texas", "Florida", "California"] else "15"
        question = question.replace("[premium_rate]", premium_rate)
        answer = answer.replace("[premium_rate]", premium_rate)
        
        # Calculate premium example (e.g., $1,000 for 10%)
        premium_example = str(int(premium_rate) * 100)
        answer = answer.replace("[premium_example]", premium_example)
        
        # State specific replacements
        state_specifics = {
            "Oklahoma": {
                "recent_state_change": "recent reforms in bail procedures",
                "state_specific_factor": "county-specific bail schedules"
            },
            "Texas": {
                "recent_state_change": "the 2021 bail reform legislation",
                "state_specific_factor": "different county bail practices"
            },
            "Florida": {
                "recent_state_change": "updated pretrial release guidelines",
                "state_specific_factor": "varying bail schedules by judicial circuit"
            }
        }
        
        # Apply state-specific replacements if available
        if state_name in state_specifics:
            for key, value in state_specifics[state_name].items():
                placeholder = f"[{key}]"
                answer = answer.replace(placeholder, value)
        
        customized_faqs.append({
            "question": question,
            "answer": answer
        })
    
    return customized_faqs

def main():
    # Load all FAQs
    faqs = load_faqs()
    print(f"Loaded {len(faqs)} FAQs from FAQ.md")
    
    # Print first FAQ as a sample
    if faqs:
        print("\nSample FAQ:")
        print(f"Question: {faqs[0]['question']}")
        print(f"Answer: {faqs[0]['answer']}")
    
    # Test with different states
    for state in ["Oklahoma", "Texas", "Florida"]:
        selected_faqs = select_random_faqs(faqs, state)
        print(f"\n--- 5 Random FAQs for {state} ---")
        for i, faq in enumerate(selected_faqs):
            print(f"\n{i+1}. {faq['question']}")
            print(f"   {faq['answer'][:100]}...")  # Print first 100 chars of answer

if __name__ == "__main__":
    main() 