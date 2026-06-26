import asyncio

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
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


def run_reduce_phase(repos: list[dict], mini_cards: list[str]) -> str:
    if not mini_cards:
        raise ValueError("Cannot run reduce phase: no mini-cards received from map phase.")
    llm = ChatOpenAI(model=REDUCE_MODEL, temperature=0.3)
    combined = "\n\n---\n\n".join(
        f"[{i+1}] URL: {repos[i]['url']}\n{card}" if i < len(repos) else f"[{i+1}] {card}"
        for i, card in enumerate(mini_cards)
    )
    messages = [
        SystemMessage(content=REDUCE_SYSTEM_PROMPT),
        HumanMessage(content=combined),
    ]
    response = llm.invoke(messages)
    return response.content


def run_processing(repos: list[dict]) -> str:
    mini_cards = asyncio.run(run_map_phase(repos))
    return run_reduce_phase(repos, mini_cards)
