import re

class Message:
    def __init__(self, content):
        self.content = content

    @staticmethod
    def initial_prompt():
        return """
        Can you create a basic local database system to track information about restaurants, chefs, and dishes.
        Please also create a locally hosted UI to edit, query, and update these tables.
        """

    def extract_delivery_message(self):
        # Regex pattern to identify the target recipient
        pattern = r"\[To (E|P|T|K)\]"
        # Finding the first split
        split_index = re.search(pattern, self.content)

        # Getting everything after the split
        if split_index:
            return self.content[split_index.end()+5:] + "And remember, don't tell me you ae going to work soon. Actually do the work in the next message!"

        raise Exception("An error occurred during delivery message extraction.")