from app.services.answer_evaluator import AnswerEvaluator


def test_answer_evaluator():

    evaluator = AnswerEvaluator()

    result = evaluator.evaluate(
        question="What is a vector database and why is it useful in a RAG system?",
        answer=(
            "A vector database stores embeddings and allows "
            "similarity search. In RAG, it retrieves relevant "
            "documents which are then provided to the language model "
            "as context."
        ),
        curriculum_topic="Vector Databases"
    )

    print("\nEvaluator result:")
    print(result)

    assert isinstance(result, dict)
    assert "score" in result
    assert "technical_correctness" in result
    assert "depth" in result
    assert "reasoning" in result
    assert "clarity" in result
    assert "strengths" in result
    assert "gaps" in result