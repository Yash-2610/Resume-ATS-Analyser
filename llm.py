from dotenv import load_dotenv
from groq import Groq
import os
load_dotenv()

## --defines llm
llm = Groq(api_key=os.environ["GROQ_API"])