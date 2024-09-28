import json
from llm_generation import llm
from sentence_transformers import SentenceTransformer

def compute_similarity(user_question: str, generated_answer: str, embedding_model: SentenceTransformer) -> float:
    
    v_q = embedding_model.encode(user_question)
    v_answer = embedding_model.encode(generated_answer)
    
    return float(v_q.dot(v_answer))



def judge_relevance(user_question: str, generated_answer: str, model_name: str) -> dict:
    judge_prompt_template = """
    You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
    Your task is to analyze the relevance of the generated answer compared to a user's question.
    Based on the relevance and similarity of the generated answer to the original answer, you will classify
    it as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

    Here is the data for evaluation:

    Question: {question}
    Generated Answer: {answer}

    Please analyze the content and context of the generated answer in relation to the original
    answer and provide your evaluation in parsable JSON without using code blocks:

    {{
    "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
    "Explanation": "[Provide a brief explanation for your evaluation]"
    }}
    """.strip()


    prompt = judge_prompt_template.format(question=user_question, answer=generated_answer)

    evaluation = llm(prompt, model_name)


    try:
        json_eval = json.loads(evaluation)
        return json_eval
    except json.JSONDecodeError:
        result = {"Relevance": "UNKNOWN", "Explanation": "Failed to parse evaluation"}
        return result
