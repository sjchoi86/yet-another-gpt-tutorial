import re
from IPython.display import Markdown,display

def printmd(string):
    display(Markdown(string))
    
def extract_quoted_words(string):
    quoted_words = re.findall(r'"([^"]*)"', string)
    return quoted_words    