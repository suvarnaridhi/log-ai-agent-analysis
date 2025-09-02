import json
from agent.llm import build_llm
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class SummaryAgent:
    def __init__(self):
        self.llm=build_llm()

    def analyze_logs(self,anomalies):

        template="""
                You are a cybersecurity log analysis assistant.
                You will be given a list of detected anomalies.

                Task:
                1.Summarize the anomalies in plain English in a way that a non-technical person could understand.
                2.Suggest actions to mitigate the anomalies that can be taken (e.g., blocking IPs, ignore, investigating further, etc.).

                Anomalies:
                {anomalies}

                Format the response as:

                Analysis summary:
                Summary: <short paragraph>

                Actions:
                - <anomaly_1> : <action_1>
                - <anomaly_2> : <action_2>
                - <anomaly_3> : <action_3>

            """

        prompt=PromptTemplate(input_variables=["anomalies"], template=template)
        chain=prompt | self.llm

        report=chain.invoke({"anomalies":anomalies})
        return report.content

