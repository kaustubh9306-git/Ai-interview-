from app.services.llm_service import LLMService


service = LLMService()

result = service.generate(
    system_prompt=(
        "You are a strict technical interviewer "
        "specializing in AI engineering."
    ),
    user_prompt=(
        "Ask me one technical interview question "
        "about Retrieval-Augmented Generation."
    )
)

print("\nLLM RESPONSE:\n")
print(result)