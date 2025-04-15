from agents import qa_agent_respond
import os
import json
from datetime import datetime
import time
from typing import Dict, Any
import sys
from dotenv import load_dotenv

def check_api_key() -> bool:
    """Check if the AviationStack API key is set in environment variables."""
    load_dotenv()  # Load environment variables
    if not os.getenv('AVIATIONSTACK_API_KEY'):
        print("⚠️ Warning: AVIATIONSTACK_API_KEY environment variable is not set.")
        print("Please set your API key using:")
        print("Windows PowerShell: $env:AVIATIONSTACK_API_KEY='your_api_key'")
        print("Linux/Mac: export AVIATIONSTACK_API_KEY='your_api_key'")
        return False
    return True

def display_welcome_message() -> None:
    """Display the welcome message and available commands."""
    print("\n✈️ Welcome to the Real-Time Airline Assistant!")
    print("Type 'exit' to quit or 'help' for available commands.\n")
    print("Available commands:")
    print("- Ask about a specific flight (e.g., 'What is the status of flight AI123?')")
    print("- Type 'help' to see this message again")
    print("- Type 'exit' to quit")
    print("- Type 'history' to see your recent queries")
    print("- Type 'clear' to clear the screen\n")

def display_help() -> None:
    """Display the help message with available commands and examples."""
    print("\n📚 Available Commands:")
    print("1. Flight Information:")
    print("   - 'What is the status of flight AI123?'")
    print("   - 'Tell me about flight AI456'")
    print("   - 'Is flight AI789 on time?'")
    print("2. System Commands:")
    print("   - 'help' - Show this help message")
    print("   - 'exit' or 'quit' - Exit the program")
    print("   - 'history' - Show recent queries")
    print("   - 'clear' - Clear the screen")
    print("\n💡 Tips:")
    print("- Flight numbers should be in the format 'AI123'")
    print("- You can ask about departure time, status, or destination")
    print("- The system provides real-time flight information\n")

def process_response(response: str) -> None:
    """Process and display the response from the QA agent."""
    try:
        response_data = json.loads(response)
        if "answer" in response_data:
            print("\nAI:", response_data["answer"])
        else:
            print("\nAI: Sorry, I couldn't process your request. Please try again.")
    except json.JSONDecodeError:
        print("\nAI: Error processing the response. Please try again.")
    except Exception as e:
        print(f"\nAI: An error occurred: {str(e)}")
        print("Please try again or contact support if the problem persists.")

def main() -> None:
    """Main function to run the airline assistant."""
    try:
        if not check_api_key():
            sys.exit(1)

        display_welcome_message()
        query_history: list[str] = []

        while True:
            try:
                user_query = input("\nYou: ").strip()
                
                if not user_query:
                    continue
                    
                if user_query.lower() in ["exit", "quit"]:
                    print("\n👋 Thank you for using the Airline Assistant. Goodbye!")
                    break
                    
                if user_query.lower() == "help":
                    display_help()
                    continue

                if user_query.lower() == "history":
                    if query_history:
                        print("\n📜 Recent Queries:")
                        for i, query in enumerate(query_history[-5:], 1):
                            print(f"{i}. {query}")
                    else:
                        print("\nNo recent queries found.")
                    continue

                if user_query.lower() == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    display_welcome_message()
                    continue

                # Process the query
                response = qa_agent_respond(user_query)
                process_response(response)
                
                # Add to history if it's a flight query
                if "flight" in user_query.lower():
                    query_history.append(user_query)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Program interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {str(e)}")
                print("Please try again or contact support if the problem persists.")
                continue

    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
