from openai import OpenAI
from typing import List


def build_prompt(query: str, search_results: List[dict]) -> str:

    prompt_template = """
    You're a assistant that informs the user on the latest cryptocurrency hacks and exploits. Answer the QUESTION based on the CONTEXT from our crytocurrency hacks and exploits database.
    Use only the facts from the CONTEXT when answering the QUESTION. Do not include any reference to the CONTEXT in your answer.
    
    QUESTION: {question}
    
    CONTEXT:
    {context}
    """.strip()
    
    entry_template = """
    title: {title}
    date: {date}
    summary: {summary}
    tags: {tags}
    """.strip()
    
    context = ""
    
    for doc in search_results:
        context = context + entry_template.format(**doc) + "\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt: str, model_name: str) -> str:
    client = OpenAI(
        base_url='http://localhost:11434/v1/',
        api_key='ollama',
    )
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
    except ConnectionError:
        err_response = "Could not connect to ollama endpoint. Make sure ollama is running locally."
        print(err_response)
        return err_response


