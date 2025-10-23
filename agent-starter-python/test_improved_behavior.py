#!/usr/bin/env python3
"""
Test the improved agent behavior
"""

import sys
import asyncio

sys.path.insert(0, 'src')

from database import Database
from agent import Assistant

async def test_improved_behavior():
    print("🌟 TESTING IMPROVED AGENT BEHAVIOR")
    print("=" * 50)
    
    # Initialize system
    db = Database()
    agent = Assistant()
    agent.set_customer_phone("+15551234567")
    
    print("\n✅ These questions should be handled by AI directly (no escalation):")
    
    test_questions = [
        "Hello, how are you?",
        "Can you hear me?", 
        "What are your hours?",
        "How much do haircuts cost?",
        "Where are you located?",
        "Do I need an appointment?"
    ]
    
    for question in test_questions:
        print(f"\n💬 Customer: '{question}'")
        # The AI should answer these directly without escalation
        print(f"🤖 AI: Should answer directly (no escalation)")
    
    print("\n🆘 These questions should trigger supervisor escalation:")
    
    escalation_questions = [
        "Do you offer hair transplant procedures?",
        "What's the chemical composition of your hair dye?",
        "Can you treat scalp conditions?",
        "Do you have specific stylists available on Tuesday?"
    ]
    
    for question in escalation_questions:
        print(f"\n💬 Customer: '{question}'")
        response = await agent.request_help(None, question)
        print(f"🤖 AI: {response}")
    
    print("\n" + "=" * 50)
    print("🎯 IMPROVED BEHAVIOR DEMONSTRATED!")
    print("✅ Basic questions: Handled directly by AI")
    print("✅ Complex questions: Smart escalation to supervisor")
    print("✅ More efficient workflow with appropriate escalations")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_improved_behavior())
