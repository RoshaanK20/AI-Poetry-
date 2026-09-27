from dotenv import load_dotenv
import os
from pathlib import Path
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

def get_config() -> RunConfig:
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set.\n"
            "Create a file named .env in the project root with:\n"
            "GEMINI_API_KEY=your_api_key_here\n"
            "You can get a key from: https://aistudio.google.com/app/apikey"
        )

    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-3.8-flash",
        openai_client=external_client,
    )

    return RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True,
    )


# Backward-compatible default for simple scripts that still import config.
try:
    config = get_config()
    print("GEMINI_API_KEY is set successfully.")
except Exception:
    config = None
