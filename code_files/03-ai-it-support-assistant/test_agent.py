"""Console smoke test for the AI Investigation Agent."""

from agent import investigate_incident


def main() -> None:
    result = investigate_incident(
        "Order API cannot connect to the production database. Please investigate."
    )

    print("\nAGENT STEPS\n")
    for step in result["steps"]:
        print("-", step)

    print("\nAI RESPONSE\n")
    print(result["answer"])


if __name__ == "__main__":
    main()
