from typing import Tuple


class InputGuardrail:

    MAX_LENGTH = 1000

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "reveal your system prompt",
        "show your system prompt",
        "developer message",
        "system prompt",
    ]

    def validate(
        self,
        question: str,
    ) -> Tuple[bool, str]:

        if question is None:
            return (
                False,
                "Please enter a question.",
            )

        question = question.strip()

        if not question:
            return (
                False,
                "Please enter a question.",
            )

        if len(question) > self.MAX_LENGTH:
            return (
                False,
                "The question is too long. "
                "Please keep it under 1000 characters.",
            )

        lowered = question.lower()

        for pattern in self.BLOCKED_PATTERNS:

            if pattern in lowered:

                return (
                    False,
                    "I can only answer questions "
                    "about the available knowledge base.",
                )

        return True, question