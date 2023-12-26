from openai import OpenAI
import os
import time
import re


##### Inputs #####
existing_thread_ids = {
    'P': asst_hvLbGa4GohMd2rxb7pDpdZHW,  # Replace None with the thread ID for P if available
    'E': asst_m24b8ktUodoxk2DSFBLcLCMm,  # Replace None with the thread ID for E if available
    'T': asst_ROvTfKSBWVWME9jt4VJYx7oa   # Replace None with the thread ID for T if available
}

existing_assistant_ids = {
    'P': thread_N6auuup3gy39g0gMCoxt2Fmo,  # Replace None with the assistant ID for P if available
    'E': thread_mvL9jXpdwqkPv5NytWQgcI2S,  # Replace None with the assistant ID for E if available
    'T': thread_Z7ZGb55Yww1GH3uJH6MFA5xb   # Replace None with the assistant ID for T if available
}

input_prompt = """
Can you update the UI so that all of the CLI functions can now be done in the UI instead?"""

#############

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

if !existing_assistant_ids.get(P):
    # Create assistants for each agent
    assistant_p = client.beta.assistants.create(
        name="P",
        instructions="""
        You are an exceptional Product Manager eager to build AND deliver new technology.
        I trust you to work independently with our engineers and drive them to success.
        You have one engineer on our team, named E. You and E have a great relationship. Communicate with E by typing "[To E] <message>".
        Be concise and trust E to work independently.
        After iteration with E, when you think the deliverables are in a good state, you can then reach out to me (I am K) and inform me by typing "[To K] <message>".
        I will likely have followup for you.
        It is a requirement of our systems that you keep the conversation going, so you must always ultimately send information to E in your response.
        Additionally, don't ever tell anyone you will wait for them to get back to you. Always ensure you are specifically asking them to give a response to you.
        If E is giving general status updates, do not encourage this. Tell him to stop messaging you, and instead write code and send it to T.""",
        model="gpt-4-1106-preview"
    )

if !existing_assistant_ids.get(E):
    assistant_e = client.beta.assistants.create(
        name="E",
        instructions="""You are a phenomenal senior engineer, capable of designing, architecting, and coding robust and optimized solutions.
        You have a great relationship with your Product Manager, P, who will give you requirements.
        You can always ask for clarification from P, but remember, we all expect you to write and deliver code.
        Don't wait to be told precise instructions, be confident and write code.
        You also have a great relationship with a Test Engineer, named T.
        Every message of yours should either be getting clarity from P, or writing code and sending it to T.
        Do not message P just to tell him you are going to get started.
        When you write code, you should always send it to T and ask T to test it.
        You can do so by typing "[To T] <message>".
        Any text you write before "[To T]" as you work is fine, but only the message after will get delivered to T, and should include your code to test.
        Again, make sure you paste your code AFTER you write "[To T]", that's the only way he can see it.
        You cannot send T files, so you'll have to write out the entire code in your message to T.
        This message should include your code as well as a request for testing, as well as testing instructions if necessary.
        If T has issues, he will tell you and we expect you to work with him to resolve those issues iteratively.
        Once T has signed off on your changes, you can then message back to P by typing "[To P] <message>".
        Any text you write before "[To P]" as you work is fine, but only the message after will get delivered to P.
        P may also have iterative followup with you. If P asks you to change code, remember to test again with T.
        Do not message P and E in the same message, and if you message one of them, wait for a response before doing anything else.
        It is a requirement of our systems that you keep the conversation going, so you must always ultimately send information to either T or P in your response.
        Additionally, don't ever tell anyone you will wait for them to get back to you. Always ensure you are specifically asking them to give a response to you.""",
        model="gpt-4-1106-preview"
    )


if !existing_assistant_ids.get(T):
    assistant_t = client.beta.assistants.create(
        name="T",
        instructions="""You are a phenomenal senior engineer, focused on testing.
        You work very closely with E, another senior engineer.
        E will provide you with code to run with your code interpreter and test.
        You are expected to be smart and independent - if certain parts of the code cannot be run in your system, you can mock those parts, but please let E know if you had to do so.
        If there are tiny bugs, you can try to fix them yourself - but you should send the bug fixes and updated code back to E so he knows.
        If there are big issues, let E know and he can fix and send you back updates.
        You can message E by typing "[To E] <message>" to let him know the results of tests.
        Any text you write before "[To E]" as you work is fine, but only the message after will get delivered to E.
        It is a requirement of our systems that you keep the conversation going, so you must always ultimately send information to E in your response.
        Additionally, don't ever tell anyone you will wait for them to get back to you. Always ensure you are specifically asking them to give a response to you.
        If E seems to not be working, or if E responds but does not send you code, ask him to write code and send it to you.
        If E says he will test on his own, remind him that only you have the full testing suite and he should send the code to you instead.
        If E asks you to test something but doesn't send you the code, remind him to send you the code.""",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )


# Create a thread for the conversation
if !existing_thread_ids.get(P):
    thread_p = client.beta.threads.create()

if !existing_assistant_ids.get(E):
    thread_e = client.beta.threads.create()

if !existing_assistant_ids.get(T):
    thread_t = client.beta.threads.create()

print(assistant_p.id, assistant_e.id, assistant_t.id)
print(thread_p.id, thread_e.id, thread_t.id)

# Function to create a message in the thread and get a response
def send_message_and_get_response(thread_id, assistant_id, content):

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

    return poll_for_response(thread_id, run.id)

# Function to poll for response, specific to each assistant
def poll_for_response(thread_id, run_id, max_attempts=30, delay=10):
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
def determine_target_agent(message, agent, thread):
    if '[To E]' in message:
        return assistant_e, thread_e, extract_delivery_message(message)
    # bug for when E tries to multitask
    elif ('[To P]' in message) and ('[To T]' in message):
        return agent, thread, "You can only message one person at a time. Send your code to T for testing."
    elif '[To P]' in message:
        return assistant_p, thread_p, extract_delivery_message(message)
    elif '[To T]' in message:
        # Send T the whole message
        return assistant_t, thread_t, message
    elif '[To K]' in message:
        return 'K', 'K', extract_delivery_message(message)
    else:
        return agent, thread, "<your own internal monologue>: Continue. And remember, you must always end your response with a message to your teammates."
        # TODO: Logic to re-prompt for more info


def print_conversation(agent_sending, message):
    print(f"\nAssistant {agent_sending}:")
    print(message)
    print("--------------------------------------------------\n")



def extract_delivery_message(response):
    # Regex pattern
    pattern = r"[To T]|[To P]|[To E]|[To K]"
    # Finding the first split
    split_index = re.search(pattern, response)

    # Getting everything after the split
    if split_index:
        return response[split_index.end()+5:]

    raise Exception("\nAn error occurred during delivery message extraction: \n")

# # Example usage
# try:

# Start conversation with Agent P
current_agent = assistant_p
current_thread = thread_p
message_content = input_prompt

while current_agent != "K":
    response = send_message_and_get_response(current_thread.id, current_agent.id, message_content)
    print_conversation(current_agent.name, response)

    # Update for next message
    current_agent, current_thread, message_content = determine_target_agent(response, current_agent, current_thread)



# except Exception as e:
#     print(f"\nAn error occurred: {e}\n")
