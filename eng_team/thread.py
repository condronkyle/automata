class Thread:
    def __init__(self, client, thread_id=None):
        self.client = client
        self.thread_id = thread_id or self.create_thread()

    def create_thread(self):
        return self.client.client.beta.threads.create().id

