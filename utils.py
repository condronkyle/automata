import time
import re

#TODO: Add Senior Eng PR Review assistant
#TODO: Use json api or function api to store code

# Function to create a message in the thread and get a response
def send_message_and_get_response(client, thread_id, assistant_id, content):
    # Create a message in the specified thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )

    # Create a run using the specified assistant, within the specified thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    return poll_for_response(client, thread_id, run.id)

# Function to poll for response, specific to each assistant
def poll_for_response(client, thread_id, run_id, max_attempts=30, delay=10):
    for attempt in range(max_attempts):
        print(f"Polling attempt {attempt + 1}/{max_attempts}...")

        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            return messages.data[0].content[0].text.value

        time.sleep(delay)
    return None

# Function to determine the targeted agent from a message
def determine_target_agent(message, current_agent, agents_dict):
    #TODO switch statement for the diff current agents
    content = message.content
    if '[To E]' in content:
        return agents_dict["E"], agents_dict["E"].thread.thread_id, message.extract_delivery_message()
    # bug for when E tries to multitask
    elif ('[To P]' in content) and ('[To T]' in content):
        return agents_dict["E"], agents_dict["E"].thread.thread_id, "You can only message one person at a time. Send your entire code to T for testing."
    elif '[To P]' in content:
        return agents_dict["P"], agents_dict["P"].thread.thread_id, message.extract_delivery_message()
    elif '[To T]' in content:
        # Send T the whole message
        return agents_dict["T"], agents_dict["T"].thread.thread_id, message.content
    elif '[To K]' in content:
        return 'K', 'K', message.extract_delivery_message()
    else:
        return current_agent, current_agent.thread.thread_id, "This is the manager stepping in. Go ahead and do the work in your next message, and send it to your relevant teammate. And remember, you must always end your response with a message to one of your teammates by using [To <X>]."
        # TODO: Logic to re-prompt for more info

    pattern = r"\[To (E|P|T|K)\]"
    matches = re.findall(pattern, message)

    if len(matches) > 1:
        return current_agent, current_agent.thread_id, "You can only message one person at a time. Send your code to T for testing."
    elif matches:
        target = matches[0]
        # Process the target
    else:
        print("No matches found.")

    if match:
        target = match.group(1)
        # Select the target agent from the dictionary
        if target in agents_dict:
            target_agent = agents_dict[target]
            return target_agent, target_agent.thread_id, message

    # Default to current agent if no target is found
    return current_agent, current_agent.thread_id, message


def print_conversation(agent_sending, message):
    print(f"\nAssistant {agent_sending.name}:")
    print(message)
    print("--------------------------------------------------\n")
