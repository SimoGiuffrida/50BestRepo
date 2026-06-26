import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts import MAP_SYSTEM_PROMPT, REDUCE_SYSTEM_PROMPT

MAP_MODEL = "gpt-4o-mini"
REDUCE_MODEL = "gpt-4o"


async def run_map_phase(repos: list[dict]) -> list[str]:
    llm = ChatOpenAI(model=MAP_MODEL, temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        ("system", MAP_SYSTEM_PROMPT),
        ("human", "Repository: {name}\nDescription: {description}\nREADME:\n{readme_text}"),
    ])
    chain = prompt | llm
    try:
        responses = await chain.abatch(repos)
        return [r.content for r in responses]
    except Exception as e:
        print(f"Map phase failed: {e}")
        return []
