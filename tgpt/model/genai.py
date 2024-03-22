import os
import json
from io import StringIO
from langchain.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate

class Generator:

    def __init__(self):
        self.llm = openai.OpenAI(temperature = 0.5)

    def get_template(self):
        template = PromptTemplate(
            input_variables=["cc", "ett", "tf"], template = """
            I am a driver on the road, generate a travel advisory for me given that there is a
            {cc} amount of cars near me, I am {ett} away from my destination and the 
            expected traffic flow to my destination is {tf}.
            """
        )
        return template
    
    def generate(self, context:dict):
        resp_ = StringIO()
        resp_.write("Roadworks nearby:\n" + self.create_rw_str(context["ti"]) + "\n")
        resp_.write("\n" + LLMChain(llm = self.llm, 
                        prompt = self.get_template(), 
                        verbose = True).run(cc = context["cc"], 
                                            ett = context["ett"], 
                                            tf = context["tf"]))
        resp = resp_.getvalue()
        resp_.close()
        return resp
        