from src.retrieval.hybrid_retriever import (
    HybridRetriever,
)

from src.llm.answer_generator import (
    AnswerGenerator,
)

from src.guardrails import (
    GuardrailPipeline,
)


def main():

    print(
        "\n"
        + "=" * 60
    )

    print(
        "FINAL RAG PIPELINE TEST"
    )

    print(
        "=" * 60
    )

    question = input(
        "\nEnter your policy question: "
    ).strip()

    # ======================================================
    # GUARDRAIL
    # ======================================================

    guardrails = GuardrailPipeline()

    valid, validated_question = (
        guardrails.validate_input(
            question
        )
    )

    if not valid:

        print(
            "\nInput blocked:"
        )

        print(
            validated_question
        )

        return

    hybrid = None

    try:

        # ==================================================
        # HYBRID RETRIEVAL
        # ==================================================

        hybrid = HybridRetriever(
            vector_k=5,
            graph_k=5,
        )

        retrieval_result = (
            hybrid.retrieve(
                validated_question
            )
        )

        print(
            "\nRetrieved information:"
        )

        print(
            "Vector results:",
            len(
                retrieval_result.get(
                    "vector_results",
                    [],
                )
            ),
        )

        print(
            "Graph entities:",
            len(
                retrieval_result.get(
                    "graph_entities",
                    [],
                )
            ),
        )

        print(
            "Graph relationships:",
            len(
                retrieval_result.get(
                    "graph_relationships",
                    [],
                )
            ),
        )

        print(
            "Merged chunks:",
            len(
                retrieval_result.get(
                    "merged_chunks",
                    [],
                )
            ),
        )

        # ==================================================
        # ANSWER GENERATION
        # ==================================================

        print(
            "\nGenerating final answer..."
        )

        generator = AnswerGenerator()

        answer = generator.generate(
            validated_question,
            retrieval_result,
        )

        # ==================================================
        # OUTPUT GUARDRAIL
        # ==================================================

        valid_output, final_answer = (
            guardrails.validate_output(
                answer
            )
        )

        if not valid_output:

            print(
                "\nOutput blocked:"
            )

            print(
                final_answer
            )

            return

        # ==================================================
        # FINAL RESPONSE
        # ==================================================

        print(
            "\n"
            + "=" * 60
        )

        print(
            "FINAL ANSWER"
        )

        print(
            "=" * 60
        )

        print(
            f"\n{final_answer}"
        )

    except Exception as e:

        print(
            "\nRAG pipeline failed."
        )

        print(
            "Exception type:",
            type(e).__name__,
        )

        print(
            "Exception:",
            e,
        )

    finally:

        if hybrid:

            hybrid.close()


if __name__ == "__main__":
    main()