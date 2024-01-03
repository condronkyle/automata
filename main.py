import json
from client import Client
from assistants import ProductManager, Engineer, TestEngineer
from message import Message
from utils import determine_target_agent, print_conversation
from thread import Thread

def main(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)

    assistant_ids = config.get("assistant_ids", {})
    thread_ids = config.get("thread_ids", {})
    initial_prompt = config.get("initial_prompt", "")


    client = Client()

    # Initialize assistants
    product_manager = ProductManager(client, assistant_id=assistant_ids.get("P"))
    engineer = Engineer(client, assistant_id=assistant_ids.get("E"))
    test_engineer = TestEngineer(client, assistant_id=assistant_ids.get("T"))

    # Initialize threads
    product_manager.thread = Thread(client, thread_id=thread_ids.get("P"))
    engineer.thread = Thread(client, thread_id=thread_ids.get("E"))
    test_engineer.thread = Thread(client, thread_id=thread_ids.get("T"))

    current_agent = product_manager
    current_thread = product_manager.thread.thread_id
    message = Message(initial_prompt

    while not current_agent.is_final_agent():
        response = current_agent.send_message_and_get_response(message.content)
        print_conversation(current_agent, response)

        # Process the response to get the actual message content
        message.content = message.extract_delivery_message()

        # Determine the next target agent and thread based on the response
        current_agent, current_thread, message = determine_target_agent(message.content, response, current_agent)

if __name__ == "__main__":
    config_file = 'config.json'
    main(config_file)