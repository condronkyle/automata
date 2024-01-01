from thread import thread
from utils import send_message_and_get_response

class Assistant:
    def __init__(self, client, name, instructions, model):
        self.client = client
        self.name = name
        self.instructions = instructions
        self.model = model
        self.assistant_id = None
        self.thread_id = None
        self.create_assistant()

    def create_assistant(self):
        if not self.assistant_id:
            assistant = self.client.client.beta.assistants.create(
                name=self.name,
                instructions=self.instructions,
                model=self.model
            )
            self.assistant_id = assistant.id
            self.thread_id = self.client.client.beta.threads.create().id

    def send_message_and_get_response(self, thread_id, message_content):
        return send_message_and_get_response(self.client.client, thread_id, self.assistant_id, message_content)

    def is_final_agent(self):
        return self.name == "K"  # Assuming 'K' is the final agent in the workflow

class ProductManager(Assistant):
    def __init__(self, client):
        super().__init__(
            client,
            "P",
            """You are an exceptional Product Manager eager to build AND deliver new technology.
            I trust you to work independently with our engineers and drive them to success.
            You have one engineer on our team, named E. You and E have a great relationship. Communicate with E by typing "[To E] <message>".
            Be concise and trust E to work independently.
            After iteration with E, when you think the deliverables are in a good state, you can then reach out to me (I am K) and inform me by typing "[To K] <message>".
            I will likely have followup for you.
            It is a requirement of our systems that you keep the conversation going, so you must always ultimately send information to E in your response.
            Additionally, don't ever tell anyone you will wait for them to get back to you. Always ensure you are specifically asking them to give a response to you.
            If E is giving general status updates, do not encourage this. Tell him to stop messaging you, and instead write code and send it to T.""",
            "gpt-4-1106-preview"
        )

class Engineer(Assistant):
    def __init__(self, client):
        super().__init__(
            client,
            "E",
            """You are a phenomenal senior engineer, focused on testing.
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
            "gpt-4-1106-preview"
        )

class TestEngineer(Assistant):
    def __init__(self, client):
        super().__init__(
            client,
            "T",
            """You are a phenomenal senior engineer, focused on testing.
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
            "gpt-4-1106-preview"
        )
