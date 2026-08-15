from typing import Tuple


class OutputGuardrail:

    MAX_ANSWER_LENGTH = 6000

    def validate(
        self,
        answer: str,
    ) -> Tuple[bool, str]:

        if answer is None:

            return (
                False,
                "I was unable to generate an answer.",
            )

        answer = answer.strip()

        if not answer:

            return (
                False,
                "I was unable to generate an answer.",
            )

        if len(answer) > self.MAX_ANSWER_LENGTH:

            return (
                False,
                "The generated answer was too long. "
                "Please ask a more specific question.",
            )

        # Basic prompt-leak protection
        forbidden_output_patterns = [
            "system prompt:",
            "developer message:",
            "internal instructions:",
        ]

        lowered = answer.lower()

        for pattern in forbidden_output_patterns:

            if pattern in lowered:

                return (
                    False,
                    "I couldn't provide a safe answer "
                    "to that question.",
                )

        return True, answer