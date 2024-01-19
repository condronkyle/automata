import json
from client import Client
from assistant import ProductManager, Engineer, TestEngineer
from message import Message
from utils import determine_target_agent, print_conversation

def main(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)

    assistant_ids = config.get("assistant_ids", {})
    thread_ids = config.get("thread_ids", {})
    initial_prompt = config.get("initial_prompt", "")

    print(assistant_ids)
    print(thread_ids)
    print(initial_prompt)

    client = Client()

    # Initialize assistants and threads
    product_manager = ProductManager(client, assistant_id=assistant_ids.get("P"), thread_id=thread_ids.get("P"))
    engineer = Engineer(client, assistant_id=assistant_ids.get("E"), thread_id=thread_ids.get("E"))
    test_engineer = TestEngineer(client, assistant_id=assistant_ids.get("T"), thread_id=thread_ids.get("T"))

    agents_dict = {}
    agents_dict["P"] = product_manager
    agents_dict["E"] = engineer
    agents_dict["T"] = test_engineer
    

    print("IDs:\n")
    for name, agent in agents_dict.items():
        print(name + ":")
        print(agent.assistant_id)
        print(agent.thread.thread_id)

    current_agent = product_manager
    current_thread = product_manager.thread.thread_id
    message_content = Message(initial_prompt).content

    while not current_agent.is_final_agent():
        response = current_agent.send_message_and_get_response(message_content)
        print_conversation(current_agent, response)

        new_message = Message(response)
        # Determine the next target agent and thread based on the response
        current_agent, current_thread, message_content = current_agent.determine_target_agent(new_message, agents_dict)

if __name__ == "__main__":
    config_file = 'config.json'
    main(config_file)