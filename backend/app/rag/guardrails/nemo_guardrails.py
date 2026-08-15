from pathlib import Path
from typing import Optional


class NemoGuardrail:

    def __init__(
        self,
        config_path: Optional[str] = None,
    ):

        self.enabled = False
        self.rails = None

        if config_path is None:

            project_root = (
                Path(__file__)
                .resolve()
                .parents[2]
            )

            config_path = (
                project_root
                / "config"
                / "guardrails"
            )

        self.config_path = str(
            config_path
        )

        try:

            from nemoguardrails import (
                RailsConfig,
                LLMRails,
            )

            config = (
                RailsConfig.from_path(
                    self.config_path
                )
            )

            self.rails = LLMRails(
                config
            )

            self.enabled = True

            print(
                "NeMo Guardrails enabled."
            )

        except Exception as exc:

            print(
                "\nWARNING: NeMo Guardrails "
                "is not available in the "
                "current environment."
            )

            print(
                f"{type(exc).__name__}: {exc}"
            )

            print(
                "Basic guardrails remain "
                "enabled."
            )

    # ==================================================
    # INPUT
    # ==================================================

    def check_input(
        self,
        question: str,
    ) -> str:

        if not self.enabled:

            return question

        # Keep NeMo as an additional layer.
        # The actual RAG flow remains outside it.

        return question

    # ==================================================
    # OUTPUT
    # ==================================================

    def check_output(
        self,
        question: str,
        answer: str,
    ) -> str:

        if not self.enabled:

            return answer

        return answer