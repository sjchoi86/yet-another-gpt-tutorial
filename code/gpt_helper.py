import copy
import os
import openai
from tenacity import retry, stop_after_attempt, wait_fixed
from IPython.display import Markdown,display
from util import printmd

def set_openai_api_key_from_txt(key_path='./key.txt',VERBOSE=True):
    """
        Set OpenAI API Key from a txt file
    """
    with open(key_path, 'r') as f: 
        OPENAI_API_KEY = f.read()
    openai.api_key = OPENAI_API_KEY
    if VERBOSE:
        print ("OpenAI API Key Ready from [%s]."%(key_path))
    
class GPTchatClass():
    def __init__(self,
                 gpt_model = 'gpt-4',
                 role_msg  = 'Your are a helpful assistant.',
                 VERBOSE   = True
                ):
        self.gpt_model     = gpt_model
        self.messages      = [{'role':'system','content':f'{role_msg}'}]
        self.init_messages = [{'role':'system','content':f'{role_msg}'}]
        self.VERBOSE       = VERBOSE
        self.response      = None
        if self.VERBOSE:
            print ("Chat agent using [%s] initialized with the follow role:[%s]"%
                   (self.gpt_model,role_msg))
    
    def _add_message(self,role='assistant',content=''):
        """
            role: 'assistant' / 'user'
        """
        self.messages.append({'role':role, 'content':content})
        
    def _get_response_content(self):
        if self.response:
            return self.response['choices'][0]['message']['content']
        else:
            return None
        
    def _get_response_status(self):
        if self.response:
            return self.response['choices'][0]['message']['finish_reason']
        else:
            return None
    
    @retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
    def chat(self,user_msg='hi',
             PRINT_USER_MSG=True,PRINT_GPT_OUTPUT=True,
             RESET_CHAT=False,RETURN_RESPONSE=True):
        self._add_message(role='user',content=user_msg)
        self.response = openai.ChatCompletion.create(
            model    = self.gpt_model,
            messages = self.messages
        )
        # Backup response for continous chatting
        self._add_message(role='assistant',content=self._get_response_content())
        if PRINT_USER_MSG:
            print("[USER_MSG]")
            printmd(user_msg)
        if PRINT_GPT_OUTPUT:
            print("[GPT_OUTPUT]")
            printmd(self._get_response_content())
        # Reset
        if RESET_CHAT:
            self.messages =  copy.copy(self.init_messages)
        # Return
        if RETURN_RESPONSE:
            return self._get_response_content()
