import ollama


class ai_assistant:
    def __init__(self, name="MovieMan"):
        self.client = ollama.Client()
        self.id = self.identity()
        self.messages = [
            {"role": "system", "content" : f"Your name is {name} and you are an ai assistant for a movie"},
            {}
        ]

    def identity(self):
        with open('ai_identity.txt', 'r') as file:
            content = file.read()

        print(content)