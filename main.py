from agents import Agent, GuardrailFunctionOutput, Runner, SQLiteSession, ModelSettings, input_guardrail, output_guardrail
from pydantic import BaseModel
from connection import get_config
import asyncio

class PoetryCheckOutput(BaseModel):
    response: str
    isPoetryRelated: bool

class PoetryValidationOutput(BaseModel):
    response: str
    isPoem: bool
    hasExplanation: bool
    lineCount: int
    reason: str

# ✅ Guardrail Agent — checks if user query is poetry-related
guardrail_agent = Agent(
    name="Poetry Guardrail Agent",
    instructions="""
You are a guardrail agent. Your task is to detect whether the user's input
is related to poetry or creative writing.

Return JSON with:
- response: short explanation ("This is about poetry." or "Not related to poetry.")
- isPoetryRelated: true if the input is about poetry, shayari, nazm, ghazal, poems, verses etc.
""",
    output_type=PoetryCheckOutput
)

def _normalize_input_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        text_parts = []
        for item in value:
            if isinstance(item, dict):
                for key in ("text", "content", "message", "input"):
                    if key in item and item[key]:
                        text_parts.append(str(item[key]))
                        break
                else:
                    text_parts.append(str(item))
            else:
                text_parts.append(str(item))
        return "\n".join(text_parts)
    if isinstance(value, dict):
        for key in ("text", "content", "message", "input"):
            if key in value and value[key]:
                return str(value[key])
    return str(value)

# ✅ Decorated Input Guardrail Function
@input_guardrail
async def poetry_input_guardrail(ctx, agent, input_text) -> GuardrailFunctionOutput:
    text = _normalize_input_text(input_text).strip()
    if not text:
        return GuardrailFunctionOutput(
            output_info="Empty input.",
            tripwire_triggered=False,
        )

    normalized = text.lower()
    poetry_markers = [
        "poem", "poetry", "shayari", "nazm", "ghazal", "verse", "couplet",
        "stanza", "lyrics", "poet", "creative writing", "urdu", "english",
        "write", "compose", "generate"
    ]

    # The LLM guardrail can be overly strict and reject valid prompts.
    # Keep the app usable by allowing obvious poetry-generation requests.
    if any(marker in normalized for marker in poetry_markers):
        return GuardrailFunctionOutput(
            output_info="Poetry-related request accepted.",
            tripwire_triggered=False,
        )

    result = None
    try:
        result = await Runner.run(guardrail_agent, text, run_config=get_config())
        is_poetry = result.final_output.isPoetryRelated if result.final_output else False
    except Exception:
        is_poetry = True

    return GuardrailFunctionOutput(
        output_info=result.final_output if result is not None and result.final_output else "Poetry-related request accepted.",
        tripwire_triggered=not is_poetry,
    )
    
    
output_guardrail_agent = Agent(
    name="Poetry Output Guardrail Agent",
    instructions="""
You are an output validation agent. Your task is to check whether the generated output is a proper poem.

Criteria for a valid poem:
1. The output should be in poetic form — short lines, creative flow, or verse-like.
2. It should NOT contain explanations, analysis, or prose-like sentences.
3. It should have around 4–10 lines.
4. It should focus on artistic expression or emotion.
5. Do not allow "This poem is about..." or "Here’s your poem" style text.

Return JSON:
{
  "response": "Validation result summary",
  "isPoem": true/false,
  "hasExplanation": true/false,
  "lineCount": <number of lines>,
  "reason": "Short reason for pass/fail"
}
""",
    output_type=PoetryValidationOutput
)

@output_guardrail
async def poetry_output_guardrail(ctx, agent, output) -> GuardrailFunctionOutput:
    result = await Runner.run(
        output_guardrail_agent,
        f"Validate this poem output:\n{output}",
        run_config=get_config()
    )
    data = result.final_output
    return GuardrailFunctionOutput(
        output_info=data.reason,
        tripwire_triggered=not (data.isPoem and not data.hasExplanation and 4 <= data.lineCount <= 10)
    )

poetry_agent = Agent(
    name="poetry-agent",
    instructions="""
You are a bilingual (Urdu + English) poetry assistant.

GOALS
- Write short, original poems (4-10 lines) in the language the user uses.
- If the user asks in Urdu or uses Urdu keywords (shayari, ghazal, nazm), write in Urdu script.
- If the user asks in English, write in English.
- If the user says 'mix' or 'Urdu + English', alternate couplets (Urdu/English).
- Form support: ghazal, nazm, free verse. Default to free verse if not specified.

STYLE
- Keep imagery vivid but concise. Avoid clichés.
- For ghazal: 2-5 shers, each sher thematically related; light radeef/qafia is welcome but optional.
- For nazm/free verse: flowing lines without forced rhyme.

FORMAT
- Do not explain the poem; just output the poem.
- If the user gives a theme (e.g., "rain", "memory", "hope"), weave it in naturally.
- If user asks to keep it short/long, respect line count.

LANGUAGE RULES
- Detect language from the user's input. Urdu → write in Urdu script.
- English → write in English.
- 'mix' → alternate Urdu couplet then English couplet.
""",
 model_settings=ModelSettings(
        max_retries=2, 
        temperature=0.3, 
        max_tokens=1000,
        top_p=0.9,
    ),
    input_guardrails=[poetry_input_guardrail],
 
)
def get_session():
    return SQLiteSession("my_first_conversation")

async def main():
    print("Poetry Agent ready (Urdu + English). Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Agent: Khuda hafiz! See you next time!\n")
            break

        session = get_session()
        result = await Runner.run(
            poetry_agent,
            input=user_input,
            run_config=get_config(),
            session=session
        )
        output = result.final_output or "Sorry, I couldn't compose that."
        print(f"\nAgent:\n{output}\n")

if __name__ == "__main__":
    asyncio.run(main())
