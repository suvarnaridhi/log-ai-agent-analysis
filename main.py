import json
from agent.summary_agent import SummaryAgent
import argparse
from agent.llm import build_llm
from agent.query_agent import QueryAgent


def load_anomalies(path="anomalies.json"):
    with open(path,"r",encoding="utf-8") as f:
        data = json.load(f)
    anomalies=[entry for entry in data if entry.get("anomaly",False)]
    return anomalies

def format_anomalies(anomalies):
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


def main():
    parser=argparse.ArgumentParser(description="Log Analysis Agent")
    parser.add_argument("--mode",choices=["summarize","query"],required=True,help="Mode to run")
    parser.add_argument("--question", type=str, help="Question to ask the query agent")
    args = parser.parse_args()

    try:
        anomalies=load_anomalies()
        anomalies_text=format_anomalies(anomalies)
    except FileNotFoundError:
        print("anomalies.json file not found. Please create it in the project root.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    if args.mode=="summarize":
        try:
            agent=SummaryAgent()
            report=agent.analyze_logs(anomalies_text)
            with open("analysis_report.txt", "w", encoding="utf-8") as f:
                f.write(report)
            print("\nReport saved to analysis_report.txt")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif args.mode=="query":
        if not args.question:
            print("Please provide a question with --question")
            return
        try:
            agent=QueryAgent()
            answer=agent.query(args.question,anomalies_text)
            print("\n Query Answer: ")
            print(answer)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()