from es_retrieval import *
from ingest_docs import *
from llm_generation import *
import time
from monitoring import *
from connect_bq import *
from datetime import datetime
import os
    

def rag(query: str, llm_model_name = "llama3.1") -> None:

    init_time = time.time()
    
    index_name = "rekt_knowledgebase"
    embedding_model_name = "multi-qa-MiniLM-L6-cos-v1"
    ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")

    # Index Documents
    es_client = connect_es(ELASTIC_URL)
    documents = retrieve_documents()
    emb_model = embedding_model(embedding_model_name)
    index_docs(index_name, es_client, documents, emb_model)


    # Generate Answer
    search_results = elastic_search_hybrid(query, index_name, es_client, emb_model)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, llm_model_name)


    # Evaluate Answer
    cosine_similarity = compute_similarity(query, answer, emb_model)
    relevance = judge_relevance(query, answer, llm_model_name)


    end_time = time.time()
    elapsed_time = end_time - init_time

    current_timestamp = datetime.now()
    timestamp_string = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    answer_dict = {
        "question": query,
        "answer": answer,
        "llm_model": llm_model_name,
        "response_time": elapsed_time,
        "cosine_similarity": cosine_similarity,
        "relevance": relevance["Relevance"],
        "relevance_explanation": relevance["Explanation"],
        "timestamp": timestamp_string
    }


    return answer_dict
