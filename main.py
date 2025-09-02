from agent.agent_core import LogAnalysisAgent

def main():
    agent = LogAnalysisAgent()
    try:
        report=agent.analyze_logs()
        with open("analysis_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
        print("\nReport saved to analysis_report.txt")
    except FileNotFoundError:
        print("anomalies.json file not found. Please create it in the project root.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()