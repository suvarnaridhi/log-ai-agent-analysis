import os
import base64
from langchain_core.prompts import PromptTemplate
import agent
from agent.summary_agent import SummaryAgent
from agent.llm import build_llm
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

class AlertAgent:
    def __init__(self,credentials_path="agent/credentials.json",token_path="token.json", to_email=None):
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"{credentials_path} not found. Please create it in the project root.")
        
        if to_email is None:
            raise ValueError("Please provide a recipient email address.")
        
        self.llm=build_llm()
        credentials=get_gmail_credentials(
            token_file=token_path,
            scopes=["https://www.googleapis.com/auth/gmail.send"],
            client_secrets_file=credentials_path,
        )
        api_resource=build_resource_service(credentials=credentials)
        self.toolkit=GmailToolkit(api_resource=api_resource)
        self.to_email=to_email or os.getenv("ALERT_EMAIL")

    def send_alert(self,anomalies,threshold=0.95):
        high_severity=[ a for a in anomalies if float(a.get("severity", 0)) > threshold ]

        if not high_severity:
            print("No high-severity anomalies found. No alert sent.")
            return None
        
        anomalies_text = "\n".join(
            f"Timestamp: {a['timestamp']}, IP: {a['ip']}, Event: {a['event']}, "
            f"Severity: {a['severity']}, Summary: {a['summary']}"
            for a in high_severity
        )
        summary_agent=SummaryAgent()
        report=summary_agent.analyze_logs(anomalies_text)

        template = """
        You are a cybersecurity assistant.
        Task:
        - Create a short urgent subject line for an alert email.
        - Wrap the provided anomaly report into a professional email body.
        - Format the body in proper HTML tags, so that when the email is sent it is properly formatted.

        Report:
        {report}

        Format strictly as:
        Subject: <subject line>
        Body:
        <email body>
        """
        prompt=PromptTemplate(input_variables=["report"],template=template)
        chain=prompt | self.llm
        result=chain.invoke({"report": report}).content

        try:
            subject_line = result.split("Subject:")[1].split("Body:")[0].strip()
            body_html = result.split("Body:")[1].strip()
        except Exception:
            subject_line = "Security Alert"
            body_html = f"<pre>{report}</pre>"

        send_tool = [t for t in self.toolkit.get_tools() if "send" in t.name.lower()][0]

        try:
            result = send_tool.run({
                "to": self.to_email,
                "subject": subject_line,
                "message": body_html  
            })


            print("Alert email sent successfully")
            return result
        
        except Exception as e:
            print(f"Failed to send alert: {e}")
            return None
 


