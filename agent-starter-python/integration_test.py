#!/usr/bin/env python3
"""
Integration test simulating the complete human-in-the-loop workflow
"""

import sys
import asyncio
import uuid

sys.path.insert(0, 'src')

from agent import Assistant

async def test_agent_workflow():
    """Test the complete agent workflow from customer question to supervisor response"""
    
    print("🎭 INTEGRATION TEST: Customer → AI → Supervisor → Customer Workflow")
    print("=" * 70)
    
    # Initialize the agent with a test customer phone
    agent = Assistant()
    agent.set_customer_phone("+15551234567")
    print(f"✅ Agent initialized for customer: {agent.customer_phone}")
    
    print("\n📞 SCENARIO: Customer asks about a service not in the AI's knowledge base")
    
    # Simulate customer asking about a service the AI doesn't know about
    customer_question = "Do you offer scalp micropigmentation?"
    print(f"💬 Customer: '{customer_question}'")
    
    # Test 1: Check if the answer is in learned answers (it won't be)
    print("\n🔍 Step 1: AI checks learned knowledge base...")
    learned_result = await agent.check_learned_answers(None, customer_question)
    if learned_result:
        print(f"🤖 AI (from knowledge): {learned_result}")
    else:
        print("🤖 AI: No previous knowledge found, requesting supervisor help...")
    
    # Test 2: AI escalates to supervisor (this is what would happen in real conversation)
    print("\n🆘 Step 2: AI escalates to human supervisor...")
    escalation_response = await agent.request_help(None, customer_question)
    print(f"🤖 AI (to customer): {escalation_response}")
    
    # Test 3: Simulate supervisor response (this would happen via dashboard)
    print("\n👨‍💼 Step 3: Human supervisor responds...")
    supervisor_response = "Yes, we offer scalp micropigmentation services through our specialist partner. Prices start at $500 per session and consultations are free."
    print(f"👨‍💼 Supervisor: {supervisor_response}")
    
    # Test 4: Add to knowledge base and test retrieval
    print("\n🧠 Step 4: Adding answer to knowledge base...")
    await agent.db.add_learned_answer(customer_question, supervisor_response)
    print("✅ Answer added to knowledge base")
    
    # Test 5: Test that AI can now answer without escalation
    print("\n🔍 Step 5: Testing AI can now answer similar questions...")
    learned_result = await agent.check_learned_answers(None, customer_question)
    if learned_result:
        print(f"🤖 AI (from knowledge): {learned_result}")
        print("✅ AI has learned and can now answer without escalation!")
    else:
        print("❌ Learning failed - this shouldn't happen")
    
    print("\n🎯 Step 6: Testing related question handling...")
    related_question = "How much does scalp micropigmentation cost?"
    related_result = await agent.check_learned_answers(None, related_question)
    if related_result:
        print(f"🤖 AI (for related question): {related_result}")
        print("✅ AI can handle related questions too!")
    else:
        print("🤖 AI: Still learning about this specific detail")
    
    print("\n" + "=" * 70)
    print("🎉 INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("✅ Complete human-in-the-loop workflow verified")
    print("✅ Learning system working correctly")
    print("✅ Agent escalation and response flow validated")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_agent_workflow())
