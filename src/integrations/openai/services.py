from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.config import settings

from .contracts import Result

model = ChatOpenAI(
        **settings.integrations.openai.api.openai.model_dump(),
    )


async def analyze_code(assignment_description: str, code_contents: str, candidate_level: str) -> Result:
    structured_llm = model.with_structured_output(Result, method="json_mode")
    system_prompt = settings.integrations.openai.api.prompt.system_message.format(
        assignment_description=assignment_description,
        candidate_level=candidate_level,
        code_contents=code_contents.replace("{", "{{").replace("}", "}}"),
        json_structure=settings.integrations.openai.api.prompt.json_structure
    )
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", "{input}")]
    )
    few_shot_structured_llm = prompt | structured_llm
    data = await few_shot_structured_llm.ainvoke({"input": ""})
    return data
