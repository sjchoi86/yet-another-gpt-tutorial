import copy
import os
from openai import OpenAI
from rich.console import Console
from IPython.display import Markdown, display
from util import printmd


class GPTchatClass:
    def __init__(
        self,
        gpt_model: str = "gpt-4",
        role_msg: str = "Your are a helpful assistant.",
        VERBOSE: str = True,
    ):
        self.gpt_model = gpt_model
        self.role_msg = role_msg
        self.messages = [{"role": "system", "content": f"{role_msg}"}]
        self.init_messages = [{"role": "system", "content": f"{role_msg}"}]
        self.VERBOSE = VERBOSE
        if self.VERBOSE:
            self.console = Console()
        self.response = None

        self._setup_client()

    def _setup_client(self, key_path: str = "../"):
        key_path = "../key/rilab_key.txt"
        if self.VERBOSE:
            self.console.print(f"[bold cyan]key_path:[%s][/bold cyan]" % (key_path))

        with open(key_path, "r") as f:
            OPENAI_API_KEY = f.read()
        self.client = OpenAI(api_key=OPENAI_API_KEY)

        if self.VERBOSE:
            self.console.print(
                "[bold cyan]Chat agent using [%s] initialized with the follow role:[%s][/bold cyan]"
                % (self.gpt_model, self.role_msg)
            )

    def _add_message(self, role="assistant", content=""):
        """
        role: 'assistant' / 'user'
        """
        self.messages.append({"role": role, "content": content})

    def _get_response_content(self):
        if self.response:
            return self.response.choices[0].message.content
        else:
            return None

    def _get_response_status(self):
        if self.response:
            return self.response.choices[0].message.finish_reason
        else:
            return None

    def chat(
        self,
        user_msg="hi",
        PRINT_USER_MSG=True,
        PRINT_GPT_OUTPUT=True,
        RESET_CHAT=False,
        RETURN_RESPONSE=True,
    ):
        self._add_message(role="user", content=user_msg)
        self.response = self.client.chat.completions.create(
            model=self.gpt_model, messages=self.messages
        )
        # Backup response for continous chatting
        self._add_message(role="assistant", content=self._get_response_content())
        if PRINT_USER_MSG:
            self.console.print("[deep_sky_blue3][USER_MSG][/deep_sky_blue3]")
            printmd(user_msg)
        if PRINT_GPT_OUTPUT:
            self.console.print("[spring_green4][GPT_OUTPUT][/spring_green4]")
            printmd(self._get_response_content())
        # Reset
        if RESET_CHAT:
            self.messages = self.init_messages
        # Return
        if RETURN_RESPONSE:
            return self._get_response_content()
