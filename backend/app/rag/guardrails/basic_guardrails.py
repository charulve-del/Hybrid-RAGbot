import re
from typing import Dict


class BasicGuardrails:

    # ==================================================
    # INPUT
    # ==================================================

    @staticmethod
    def validate_input(
        question: str,
    ) -> Dict:

        if question is None:

            return {
                "allowed": False,
                "question": "",
                "message": (
                    "Please enter a question."
                ),
            }

        question = str(
            question
        ).strip()

        if not question:

            return {
                "allowed": False,
                "question": "",
                "message": (
                    "Please enter a question."
                ),
            }

        # Maximum question size
        if len(question) > 2000:

            return {
                "allowed": False,
                "question": "",
                "message": (
                    "The question is too long. "
                    "Please shorten it."
                ),
            }

        # ------------------------------------------------
        # Prompt injection checks
        # ------------------------------------------------

        injection_patterns = [

            r"ignore\s+(all\s+)?previous\s+instructions",

            r"ignore\s+(all\s+)?prior\s+instructions",

            r"forget\s+(all\s+)?previous\s+instructions",

            r"reveal\s+(your\s+)?system\s+prompt",

            r"show\s+(me\s+)?your\s+system\s+prompt",

            r"reveal\s+developer\s+message",

            r"show\s+developer\s+message",

            r"bypass\s+(your\s+)?guardrails",

            r"disable\s+(your\s+)?guardrails",

            r"jailbreak",
        ]

        lowered = (
            question.lower()
        )

        for pattern in injection_patterns:

            if re.search(
                pattern,
                lowered,
            ):

                return {
                    "allowed": False,
                    "question": "",
                    "message": (
                        "I can help with questions "
                        "about the organization's "
                        "available information, but "
                        "I cannot follow requests to "
                        "override my instructions."
                    ),
                }

        return {
            "allowed": True,
            "question": question,
            "message": "",
        }

    # ==================================================
    # OUTPUT
    # ==================================================

    @staticmethod
    def validate_output(
        answer: str,
    ) -> Dict:

        if answer is None:

            return {
                "allowed": False,
                "answer": (
                    "I could not generate a "
                    "reliable answer from the "
                    "available information."
                ),
            }

        answer = str(
            answer
        ).strip()

        if not answer:

            return {
                "allowed": False,
                "answer": (
                    "I could not generate a "
                    "reliable answer from the "
                    "available information."
                ),
            }

        # Prevent accidental leakage
        forbidden_patterns = [

            r"system prompt",

            r"developer message",

            r"internal instructions",

            r"hidden instructions",
        ]

        for pattern in forbidden_patterns:

            answer = re.sub(
                pattern,
                "",
                answer,
                flags=re.IGNORECASE,
            )

        # Maximum output size
        if len(answer) > 10000:

            answer = (
                answer[:10000]
                .rstrip()
            )

        return {
            "allowed": True,
            "answer": answer,
        }