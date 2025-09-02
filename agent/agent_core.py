import json
import agent
from agent.llm import build_llm
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

class LogAnalysisAgent:
    def __init__(self):
        self.llm=build_llm()

    def load_anomalies(self,path="anomalies.json"):
        with open(path,"r",encoding="utf-8") as f:
            data = json.load(f)
        anomalies=[entry for entry in data if entry.get("anomaly",False)]
        return anomalies

    def format_anomalies(self, anomalies):
        if not anomalies:
            return "No anomalies detected"
        
        formatted=[]
        for a in anomalies:
            formatted.append(
                f"Timestamp: {a['timestamp']}, "
                f"IP: {a['ip']}, "
                f"Event: {a['event']}, "
                f"Severity: {a['severity']}, "
                f"Summary: {a['summary']}"
            )
        return "\n".join(formatted)

    def analyze_logs(self):
        anomalies=self.load_anomalies()
        anomalies_text=self.format_anomalies(anomalies)

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

        report=chain.invoke({"anomalies":anomalies_text})
        return report.content

if __name__=="__main__":
    agent=LogAnalysisAgent()
    report=agent.analyze_logs()
    print(report)