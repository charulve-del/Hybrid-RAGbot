from typing import Any, Dict

from src.retrieval.hybrid_retriever import (
    HybridRetriever,
)

from src.generation.answer_generator import (
    AnswerGenerator,
)

from src.guardrails.basic_guardrails import (
    BasicGuardrails,
)

from src.guardrails.nemo_guardrails import (
    NemoGuardrail,
)


class HybridRAGBot:

    def __init__(self):

        print(
            "\n" + "=" * 60
        )

        print(
            "INITIALIZING HYBRID RAG BOT"
        )

        print(
            "=" * 60
        )

        self.basic_guardrails = (
            BasicGuardrails()
        )

        self.nemo_guardrails = (
            NemoGuardrail()
        )

        self.retriever = (
            HybridRetriever(
                vector_k=5,
                graph_k=5,
            )
        )

        self.generator = (
            AnswerGenerator()
        )

        print(
            "\nHybrid RAG Bot ready."
        )

    # ========================================================
    # ASK
    # ========================================================

    def ask(
        self,
        question: str,
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # INPUT GUARDRAIL
        # ----------------------------------------------------

        input_result = (
            self.basic_guardrails
            .validate_input(
                question
            )
        )

        if not input_result["allowed"]:

            return {
                "question": question,
                "answer": input_result[
                    "message"
                ],
                "retrieval": None,
                "citations": [],
                "blocked": True,
            }

        clean_question = (
            input_result[
                "question"
            ]
        )

        # ----------------------------------------------------
        # NEMO INPUT
        # ----------------------------------------------------

        clean_question = (
            self.nemo_guardrails
            .check_input(
                clean_question
            )
        )

        # ----------------------------------------------------
        # HYBRID RETRIEVAL
        # ----------------------------------------------------

        retrieval = (
            self.retriever.retrieve(
                clean_question
            )
        )

        merged_chunks = (
            retrieval.get(
                "merged_chunks",
                [],
            )
        )

        # ----------------------------------------------------
        # NO RETRIEVAL
        # ----------------------------------------------------

        if not merged_chunks:

            answer = (
                "I could not find enough "
                "information in the available "
                "knowledge base to answer "
                "this question."
            )

            return {
                "question": clean_question,
                "answer": answer,
                "retrieval": retrieval,
                "citations": [],
                "blocked": False,
            }

        # ----------------------------------------------------
        # GENERATION
        # ----------------------------------------------------

        generated = (
            self.generator.generate(
                question=clean_question,
                merged_chunks=merged_chunks,
            )
        )

        answer = generated[
            "answer"
        ]

        # ----------------------------------------------------
        # OUTPUT GUARDRAIL
        # ----------------------------------------------------

        output_result = (
            self.basic_guardrails
            .validate_output(
                answer
            )
        )

        answer = output_result[
            "answer"
        ]

        # ----------------------------------------------------
        # NEMO OUTPUT
        # ----------------------------------------------------

        answer = (
            self.nemo_guardrails
            .check_output(
                clean_question,
                answer,
            )
        )

        return {
            "question": clean_question,
            "answer": answer,
            "retrieval": retrieval,
            "citations": generated[
                "citations"
            ],
            "blocked": False,
        }

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        try:

            self.retriever.close()

        except Exception as exc:

            print(
                "Warning while closing "
                "retriever:",
                exc,
            )