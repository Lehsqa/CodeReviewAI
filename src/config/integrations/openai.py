from pydantic import AnyHttpUrl, BaseModel


class OpenAISettings(BaseModel):
    temperature: float = 1.0
    model: str = "invalid"
    api_key: str = "invalid"
    base_url: str = "invalid"


class PromptSettings(BaseModel):
    system_message: str = """
    You are a senior code reviewer. You are reviewing the code of a {candidate_level} developer.

    Assignment Description:
    {assignment_description}

    Candidate's Code:
    {code_contents}

    Please analyze the code and provide feedback in JSON format.

    Here are some examples, I'm gonna provide you the json_structure.
    json_structure: {json_structure}

    Ensure the JSON is valid and parsable. Do not include any additional text outside the JSON structure.
    """
    json_structure: str = """{{
        "downsides_comments": "string - Provide detailed downsides and comments about the code.",
        "rating": "string - Provide an overall rating out of 10 (ex. 7/10).",
        "conclusion": "string - Provide a concluding statement summarizing the review."
    }}"""


class APISettings(BaseModel):
    openai: OpenAISettings = OpenAISettings()
    prompt: PromptSettings = PromptSettings()


class Settings(BaseModel):
    api: APISettings = APISettings()
