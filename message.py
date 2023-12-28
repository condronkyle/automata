import re

class Message:
    @staticmethod
    def initial_prompt():
        return """
        Can you create a basic local database system to track information about restaurants, chefs, and dishes.
        Please also create a locally hosted UI to edit, query, and update these tables.
        """

    @staticmethod
    def extract_delivery_message(response):
        # Regex pattern to identify the target recipient
        pattern = r"\[To (E|P|T|K)\]"
        # Finding the first split
        split_index = re.search(pattern, response)

        # Getting everything after the split
        if split_index:
            return response[split_index.end() + 1:].strip()

        raise Exception("An error occurred during delivery message extraction.")
