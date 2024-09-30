import ollama
import json

class ai_assistant:
    def __init__(self, name="MovieMan"):
        self.client = ollama.Client()
        self.messages = self.load_history()

        if not self.messages:
            # If no history exists, start with the initial system message
            self.messages = [
                {"role": "system", "content" : f"Your name is {name} and {self.identity()}"}
            ]

    def load_history(self):
        try:
            messages = []
            with open('A.I/ai_chat_history.json', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    try:
                        message = json.loads(line)  # Use `json.loads` instead of `json.load`
                        messages.append(message)
                    except json.JSONDecodeError:
                        continue
            return messages
        except Exception as e:
            print(f"Error occurred: {e}")
        return []

    def identity(self):
        with open('A.I/ai_identity.txt', 'r') as file:
            content = file.read()
        return content
    
    def get_response(self, user_input='', output=True):
        # Add the user's new message to the conversation history
        self.messages.append({"role": "user", "content": user_input})
        self.save_history(self.messages[-1])  # Save the new user message

        # Now, generate a response to only the latest user input, using history as context
        response = self.client.chat(
            model="gemma2:2b",
            messages=self.messages,  # Include the entire message history
            stream=True  # Streaming allows for partial responses
        )

        # Print the assistant's response in a stream-like fashion
        content = ""
        for i in response:
            content = i['message']['content']
            if output:
                print(content, end='', flush=True)
        print("\n")

        # Append the assistant's response to the conversation history
        self.messages.append({"role": "assistant", "content": content})
        self.save_history(self.messages[-1])  # Save the new assistant message

    def save_history(self, message):
        # Append new messages to the chat history file
        with open('A.I/ai_chat_history.json', 'a') as file:
            json.dump(message, file)
            file.write("\n")  # Ensure each message is on a new line
