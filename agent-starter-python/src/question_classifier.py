"""
Question Classifier - Determines if a customer question is about services or just technical/conversational
"""

class QuestionClassifier:
    """Classifies customer questions to avoid unnecessary escalations"""
    
    # Questions that are NOT about services - don't escalate these
    TECHNICAL_PHRASES = [
        "can you hear me",
        "hello",
        "hi",
        "are you there",
        "testing",
        "test test",
        "mic check",
        "microphone",
        "audio",
        "can you understand me",
        "do you copy",
        "one two three",
        "testing testing",
    ]
    
    CONVERSATIONAL_PHRASES = [
        "how are you",
        "what's up",
        "good morning",
        "good afternoon", 
        "good evening",
        "goodbye",
        "bye",
        "see you",
        "thanks",
        "thank you",
        "okay",
        "ok",
        "alright",
        "sure",
        "yes",
        "no",
        "maybe",
    ]
    
    @staticmethod
    def is_service_question(question: str) -> bool:
        """
        Determine if this is a real service question or just technical/conversational
        
        Args:
            question: The customer's question text
            
        Returns:
            True if it's a service question that might need escalation
            False if it's just technical/conversational
        """
        question_lower = question.lower().strip()
        
        # Check if it's a technical/audio check
        for phrase in QuestionClassifier.TECHNICAL_PHRASES:
            if phrase in question_lower:
                return False
        
        # Check if it's just conversational
        for phrase in QuestionClassifier.CONVERSATIONAL_PHRASES:
            if question_lower == phrase or question_lower.startswith(phrase):
                return False
        
        # Check if question is very short (likely not a real question)
        words = question_lower.split()
        if len(words) < 3 and '?' not in question:
            return False
        
        # Service question indicators
        service_indicators = [
            "do you offer",
            "how much",
            "what is the price",
            "what services",
            "appointment",
            "booking",
            "schedule",
            "available",
            "hours",
            "open",
            "closed",
            "location",
            "address",
            "phone",
            "contact",
            "cost",
            "price",
            "expensive",
            "cheap",
            "discount",
            "special",
            "package",
            "treatment",
            "procedure",
            "facial",
            "massage",
            "wax",
            "nail",
            "hair",
            "skin",
            "makeup",
            "spa",
            "salon",
            "botox",
            "filler",
            "laser",
            "microblading",
            "tattoo",
            "piercing",
        ]
        
        # If it contains service indicators, it's likely a service question
        for indicator in service_indicators:
            if indicator in question_lower:
                return True
        
        # If it has a question mark and is longer than 3 words, probably a service question
        if '?' in question and len(words) > 3:
            return True
        
        # Default: if we're unsure, treat as service question (better to escalate than miss)
        return True
    
    @staticmethod
    def get_standard_response(question: str) -> str:
        """
        Get a standard response for non-service questions
        
        Args:
            question: The customer's question text
            
        Returns:
            A friendly standard response
        """
        question_lower = question.lower().strip()
        
        # Audio/technical checks
        if any(phrase in question_lower for phrase in ["can you hear", "are you there", "hello", "testing"]):
            return "Yes, I can hear you perfectly! How can I help you with Glow Beauty Salon today?"
        
        # Greetings
        if any(phrase in question_lower for phrase in ["good morning", "good afternoon", "good evening"]):
            return "Good day! Welcome to Glow Beauty Salon. How can I assist you?"
        
        # Thanks
        if any(phrase in question_lower for phrase in ["thank", "thanks"]):
            return "You're very welcome! Is there anything else I can help you with today?"
        
        # Goodbyes
        if any(phrase in question_lower for phrase in ["goodbye", "bye", "see you"]):
            return "Thank you for calling Glow Beauty Salon! Have a wonderful day!"
        
        # Default conversational response
        return "I'm here to help! What would you like to know about Glow Beauty Salon?"


# Quick test function
if __name__ == "__main__":
    classifier = QuestionClassifier()
    
    test_questions = [
        ("Can you hear me?", False),
        ("Hello, are you there?", False),
        ("Testing testing one two three", False),
        ("Do you offer microblading?", True),
        ("What are your hours?", True),
        ("How much does a facial cost?", True),
        ("Thanks", False),
        ("Can I book an appointment for tomorrow?", True),
        ("Hi", False),
        ("What services do you provide?", True),
    ]
    
    print("Testing Question Classifier:\n")
    for question, expected in test_questions:
        result = classifier.is_service_question(question)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{question}'")
        print(f"   Result: {'SERVICE' if result else 'NON-SERVICE'} (Expected: {'SERVICE' if expected else 'NON-SERVICE'})")
        if not result:
            response = classifier.get_standard_response(question)
            print(f"   Response: {response}")
        print()
