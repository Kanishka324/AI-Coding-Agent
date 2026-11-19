
from agent.controller import CodingAgent


def main():

    print("=" * 50)
    print("          AI CODING AGENT")
    print("=" * 50)

    agent = CodingAgent()

    user_prompt = input(
        "\nWhat would you like me to build? "
    ).strip()

    if not user_prompt:
        print("No task provided. Exiting.")
        return

    try:
        response = agent.run(user_prompt)

        print("\n===== AGENT RESPONSE =====")
        print(response)

    except KeyboardInterrupt:
        print("\nAgent stopped by user.")

    except Exception as error:
        print(f"\nAgent error: {error}")

    print("\nAI Coding Agent finished.")


if __name__ == "__main__":
    main()
