from deepeval import evaluate
from deepeval.evaluate import AsyncConfig

# your existing imports
# your existing RAG imports
# your existing metric imports


def main():

    # -----------------------------------------
    # 1. Load test cases
    # -----------------------------------------
    test_cases = load_test_cases()

    print(f"Loaded {len(test_cases)} test cases")

    # -----------------------------------------
    # 2. Create metrics
    # -----------------------------------------
    metrics = [
        answer_relevancy_metric,
        faithfulness_metric,
        contextual_precision_metric,
        contextual_recall_metric,
    ]

    # -----------------------------------------
    # 3. Run DeepEval
    # -----------------------------------------
    evaluate(
        test_cases=test_cases,
        metrics=metrics,
        async_config=AsyncConfig(
            run_async=False
        ),
    )


if __name__ == "__main__":
    main()