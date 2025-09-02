from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from agent.llm import build_llm

class QueryAgent:
    def __init__(self):
        self.llm=build_llm()
    
    def query(self,question,anomalies):
        template="""
        You are a cybersecurity log query answering expert.
        You will be given a list of anomalies and a natural language question asked by the user.
        Answer the question in a way that the user can easily understand.
        Answer ONLY using the anomalies provided.
        If the answer cannot be found, say "Not found in anomalies."

        Anomalies:
        {anomalies}

        Question: {question}
        Answer:
        """

        prompt=PromptTemplate(
            input_variables=["anomalies", "question"],
            template=template
        )

        chain= prompt | self.llm

        return chain.invoke({
            "anomalies":anomalies,
            "question":question
        }).content