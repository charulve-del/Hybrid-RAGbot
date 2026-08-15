from .input_guardrail import InputGuardrail
from .output_guardrail import OutputGuardrail


class GuardrailPipeline:

    def __init__(self):

        self.input = InputGuardrail()
        self.output = OutputGuardrail()

    def validate_input(
        self,
        question: str,
    ):

        return self.input.validate(
            question
        )

    def validate_output(
        self,
        answer: str,
    ):

        return self.output.validate(
            answer
        )