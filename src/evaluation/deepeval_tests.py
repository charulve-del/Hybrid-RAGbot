import os

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
)


def evaluate_answer(
    question: str,
    answer: str,
    context: list[str],
):

    if not os.getenv(
        "OPENAI_API_KEY"
    ):

        raise RuntimeError(
            "OPENAI_API_KEY is not set."
        )

    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=context,
    )

    relevancy = AnswerRelevancyMetric(
        threshold=0.7,
    )

    faithfulness = FaithfulnessMetric(
        threshold=0.7,
    )

    results = evaluate(
        test_cases=[test_case],
        metrics=[
            relevancy,
            faithfulness,
        ],
    )

    return results