from client import Client
from assistants import ProductManager, Engineer, TestEngineer
from message import Message
from utils import determine_target_agent, print_conversation

def main():
    client = Client()
    product_manager = ProductManager(client)
    engineer = Engineer(client)
    test_engineer = TestEngineer(client)

    current_agent = product_manager
    current_thread = product_manager.thread_id
    message_content = Message.initial_prompt()

    while not current_agent.is_final_agent():
        response = current_agent.send_message_and_get_response(current_thread, message_content)
        print_conversation(current_agent, response)

        # Process the response to get the actual message content
        message_content = Message.extract_delivery_message(response)

        # Determine the next target agent and thread based on the response
        current_agent, current_thread, message_content = determine_target_agent(response, current_agent, current_thread)

if __name__ == "__main__":
    main()
