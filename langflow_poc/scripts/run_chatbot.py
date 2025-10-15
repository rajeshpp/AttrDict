"""
Customer Support Chatbot Runner
Interacts with the LangFlow customer support RAG chatbot
"""
import os
import sys
from dotenv import load_dotenv
from langflow_client import LangFlowClient

load_dotenv()


def run_chatbot_interactive(flow_id: str):
    """
    Run the chatbot in interactive mode
    
    Args:
        flow_id: ID of the LangFlow flow to use
    """
    client = LangFlowClient()
    session_id = "session_001"  # Maintain conversation context
    
    # Tweaks to pass OpenAI API key and other parameters
    tweaks = {
        "OpenAIEmbeddings-1": {
            "openai_api_key": os.getenv("OPENAI_API_KEY")
        },
        "ChatOpenAI-1": {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    }
    
    print("=" * 60)
    print("ACME Corp Customer Support Chatbot")
    print("=" * 60)
    print("Ask me anything about our products and services!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for contacting ACME Corp! Have a great day!")
                break
            
            # Run the flow
            print("Bot: ", end="", flush=True)
            response = client.run_flow(
                flow_id=flow_id,
                message=user_input,
                tweaks=tweaks,
                session_id=session_id
            )
            
            # Extract and print the response
            if response and "outputs" in response:
                output = response["outputs"][0]
                if "outputs" in output and len(output["outputs"]) > 0:
                    message = output["outputs"][0]["results"]["message"]["text"]
                    print(message)
                else:
                    print("I apologize, but I couldn't generate a response. Please try again.")
            else:
                print("Error: Unexpected response format")
                print(f"Response: {response}")
            
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\n\nThank you for contacting ACME Corp! Have a great day!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'quit' to exit.\n")


def test_chatbot(flow_id: str):
    """
    Test the chatbot with predefined questions
    
    Args:
        flow_id: ID of the LangFlow flow to use
    """
    client = LangFlowClient()
    
    # Test questions
    test_questions = [
        "What is the price of SmartWidget Pro?",
        "How do I reset my device?",
        "What is your return policy?",
        "How long does shipping take?",
        "My device won't connect to WiFi, what should I do?",
    ]
    
    tweaks = {
        "OpenAIEmbeddings-1": {
            "openai_api_key": os.getenv("OPENAI_API_KEY")
        },
        "ChatOpenAI-1": {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    }
    
    print("=" * 60)
    print("Testing Customer Support Chatbot")
    print("=" * 60 + "\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"Test {i}/{len(test_questions)}")
        print(f"Question: {question}")
        
        try:
            response = client.run_flow(
                flow_id=flow_id,
                message=question,
                tweaks=tweaks
            )
            
            if response and "outputs" in response:
                output = response["outputs"][0]
                if "outputs" in output and len(output["outputs"]) > 0:
                    message = output["outputs"][0]["results"]["message"]["text"]
                    print(f"Answer: {message}")
                else:
                    print("Answer: Could not generate response")
            else:
                print(f"Error: Unexpected response format")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 60 + "\n")


def main():
    """Main function"""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Interactive mode: python run_chatbot.py <flow_id>")
        print("  Test mode: python run_chatbot.py <flow_id> --test")
        print("\nTo get flow_id, upload the flow using upload_flow.py or check LangFlow UI")
        sys.exit(1)
    
    flow_id = sys.argv[1]
    test_mode = len(sys.argv) > 2 and sys.argv[2] == "--test"
    
    if test_mode:
        test_chatbot(flow_id)
    else:
        run_chatbot_interactive(flow_id)


if __name__ == "__main__":
    main()
