from llm.parser import get_parser
from llm.prompt_temp import get_prompt
from llm.models import get_model



def get_chain():
    parser,format_instruction=get_parser()
    llm=get_model()
    prompt=get_prompt()
    chain=prompt | llm | parser

    return chain , format_instruction