import re
import random

class SupportBot:
    def _init_(self):
        # Initialize negative responses and exit commands
        self.negative_res = {"no", "nope", "nay", "not a chance", "sorry"}
        self.exit_commands = {"quit", "pause", "exit", "goodbye", "bye", "farewell"}
        # Define regex patterns and corresponding functions for support responses
        self.support_responses = {
            'ask_about_product': (r'\bproduct\b', self.ask_about_product),
            'technical_support': (r'\btechnical.*support\b', self.technical_support),
            'about_returns': (r'\breturn policy\b', self.ask_about_returns),
            'general_query': (r'\bhow.*help\b', self.general_query)
        }
        self.name = ""

    def greet(self):
        # Welcome message and get user's name
        print("Hello! Welcome to our customer support.")
        self.name = input("What's your name?\n").strip()
        # Ask how the bot can assist the user
        will_help = input(f"Hi {self.name}, how can I assist you today?\n").strip().lower()
        # Check if user declines assistance
        if will_help in self.negative_res:
            print("Alright, have a great day!")
        else:
            # Start the chat session
            self.chat()

    def chat(self):
        while True:
            # Get user's query
            reply = input("Please tell me your query: ").strip().lower()
            # Check if user wants to exit
            if self.make_exit(reply):
                print("Thanks for reaching out. Have a great day!")
                break
            # Get and print response
            response = self.get_response(reply)
            print(response)

    def make_exit(self, reply):
        # Check if the reply contains any exit command
        return any(command in reply for command in self.exit_commands)

    def get_response(self, reply):
        # Check user's query against support responses
        for pattern, function in self.support_responses.values():
            if re.search(pattern, reply):
                # Call corresponding function for matched pattern
                return function()
        # If no match found, provide a default response
        return self.no_match_intent()

    def ask_about_product(self):
        responses = [
            "Our product is top-notch and has excellent reviews!",
            "You can find all product details on our website."
        ]
        return random.choice(responses)

    def technical_support(self):
        responses = [
            "Please visit our technical support page for detailed assistance.",
            "You can also call our tech support helpline for immediate help."
        ]
        return random.choice(responses)

    def ask_about_returns(self):
        response = """
        Our return policy ensures customer satisfaction. Here are the key points:
        - We offer a 30-day return period from the date of purchase.
        - Please ensure the product is in its original condition when returning.
        - Refunds will be processed promptly upon receipt of the returned item.
        - For more details, you can visit our website or contact our customer support.
        """
        return response.strip()

    def general_query(self):
        responses = [
            "How can I assist you further?",
            "Is there anything else you'd like to know?"
        ]
        return random.choice(responses)

    def no_match_intent(self):
        responses = [
            "I'm sorry, I didn't quite understand that. Can you please rephrase?",
            "My apologies, can you provide more details?"
        ]
        return random.choice(responses)

if __name__ == "__main__":
    # Create an instance of SupportBot and start the greeting process
    bot = SupportBot()
    bot.greet()