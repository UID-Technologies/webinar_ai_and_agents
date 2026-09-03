"""Console smoke test for the Enterprise Copilot."""

from copilot_agent import run_enterprise_copilot


def main() -> None:
    query = "Create ticket for payroll app access issue for employee E1001"
    result = run_enterprise_copilot(query)

    print("\nSTEPS")
    for step in result["steps"]:
        print("-", step)

    print("\nACTIONS")
    for action in result["actions"]:
        print(action)

    print("\nANSWER")
    print(result["answer"])

    print("\nCITATIONS")
    print(result["citations"])


if __name__ == "__main__":
    main()
