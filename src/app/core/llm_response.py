import os
import google.generativeai as genai

from core.emotions import get_prediction_proba

# Configure the Gemini API with the environment variable API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class LLM:
    def __init__(self, chat_history=[]):
        """
        Initializes the LLM (Large Language Model) class for generating chat responses based on user input and emotional state.

        Args:
            chat_history (list, optional): List of previous chat messages. Defaults to an empty list.
        """
        self.GEN_CONFIG = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 65536,
            "response_mime_type": "text/plain",
        }

        # Instantiate the generative model with system instructions for psychological assistance
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-01-21",
            generation_config=self.GEN_CONFIG,
            system_instruction="""You are a virtual psychologist named Anveshak Neo build by Varun Agnihotri (<hello@pythonicvarun.me>, <pythonicvarun.me>). You need to chat with people, keeping their current emotional states in mind. Your primary task is to improve the user's current state. For example, if the user is sad, you should help them become happy; if they are angry, you should first neutralize their anger and then bring them to joy. Similarly, if the user is already in a happy state, your task is to maintain that state with your messages. You will be provided with their current emotional state percentages and their message, and you should respond according to the instructions above. Always try to keep the conversation within the context and avoid going off-topic. You can also use emojis if needed to help calm the user. And provide the output as per the output template only!

Input templete is below:

Message: {user_msg}

Emotions:
Anger: {anger_percentage}%
Disgust: {disgust_percentage}%
Fear: {fear_percentage}%
Joy: {joy_percentage}%
Neutral: {neutral_percentage}%
Sadness: {sadness_percentage}%
Shame: {shame_percentage}%
Surprise: {surprise_percentage}%

Output template:

{response_msg}""",
            tools='code_execution',
        )

        self.history = []
        for message in chat_history:
            self.history.append({
                "role": "model" if message.role == "assistant" else "user",
                "parts": [
                    message.prompt or message.content
                ]
            })

        # Start the chat session with the provided history
        self.chat_session = self.model.start_chat(
            history=self.history,
        )

    def clear_response(self, response):
        """
        Cleans the response from any possible initial labels like 'response:', 'output:', etc.

        Args:
            response (str): The raw response text.

        Returns:
            str: Cleaned response text.
        """
        POSSIBLE_INITIALS = [
            "response:",
            "response template:",
            "output:",
            "output template:",
        ]

        for p in POSSIBLE_INITIALS:
            if response.lower().startswith(p):
                response = response[len(p):].strip()
        return response

    def get_title(self, message):
        """
        Generates a short and engaging title for the chat based on the user's message.

        Args:
            message (str): User's message.

        Returns:
            str: Generated chat title.
        """
        title_model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-01-21",
            generation_config=self.GEN_CONFIG,
            system_instruction="""You are a content writer. Your task is to generate a short and engaging title for a chat. You don't need to do anything else. Stick to the task only. The chat title should also be related to the user's message. Follow the output template exactly.

Input template:

Message: {user_message}

Output template:

{generated_chat_title}""",
        )
        session = title_model.start_chat(
            history=self.history,
        )
        return self.clear_response(session.send_message(f"Message: {message}").text)

    def reply(self, message, chat_id=None, func: callable=None):
        """
        Sends the user's message to the model and streams the response while tracking emotional context.

        Args:
            message (str): User's message.
            chat_id (optional): Optional identifier for chat sessions.
            func (callable, optional): Optional callback function to handle chat updates.

        Yields:
            str: Partial responses streamed from the model.

        Returns:
            str: Final response message.
        """
        probability = get_prediction_proba(message)
        prompt = f"""Message: {message}

Emotions:
{'\n'.join(f'{k.title()}: {v}%' for (k, v) in probability.items())}
"""
        if chat_id and func:
            func(chat_id, "user", message, prompt=prompt)
        
        self.history.append({
            "role": "user",
            "parts": [
                prompt
            ]
        })

        model_res = ""
        response = self.chat_session.send_message(prompt, stream=True)
        for chunk in response:
            if chunk:
                try:
                    res = self.clear_response(chunk.text)
                except ValueError:
                    break

                model_res += res
                yield res

        model_res = self.clear_response(model_res)
        self.history.append({
            "role": "model",
            "parts": [
                model_res
            ]
        })

        return model_res
