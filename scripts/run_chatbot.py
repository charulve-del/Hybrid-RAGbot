from src.app.chatbot import (
    HybridRAGBot,
)


def main():

    print("=" * 70)
    print("HYBRID RAG POLICY CHATBOT")
    print("=" * 70)

    bot = HybridRAGBot()

    try:

        while True:

            print()

            question = input(
                "Ask your policy question "
                "(type 'exit' to quit): "
            ).strip()

            if question.lower() in {
                "exit",
                "quit",
            }:

                break

            if not question:

                continue

            print(
                "\nProcessing..."
            )

            result = bot.ask(
                question
            )

            print(
                "\n" + "=" * 70
            )

            print(
                "ANSWER"
            )

            print(
                "=" * 70
            )

            print(
                result["answer"]
            )

            citations = (
                result.get(
                    "citations",
                    [],
                )
            )

            if citations:

                print(
                    "\nCitations:",
                    ", ".join(
                        f"[{x}]"
                        for x in citations
                    ),
                )

    except KeyboardInterrupt:

        print(
            "\nStopping chatbot..."
        )

    finally:

        bot.close()


if __name__ == "__main__":
    main()