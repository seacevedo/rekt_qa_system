from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
from typing import List
from tqdm.auto import tqdm


def connect_es(connection_url: str) -> Elasticsearch:
    try:
        return Elasticsearch(connection_url) 
    except ConnectionError:
        print("Connection to Elasticsearch service refused. Check the connection endpoint.")


def index_docs(index_name: str, es_client: Elasticsearch, documents: List[dict], embedding_model: SentenceTransformer) -> None:

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "title": {"type": "text"},
                "date": {"type": "text"},
                "summary": {"type": "text"},
                "tags": {"type": "keyword"},
                "title_vec": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "date_vec": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "tags_vec": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "summary_vec": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "all_vec": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
            }
        }
    }


    es_client.indices.delete(index=index_name, ignore_unavailable=True)
    es_client.indices.create(index=index_name, body=index_settings)



    print("Indexing Documents...")
    for doc in tqdm(documents):
        title = doc['title']
        summary = doc['summary']
        doc['all_vector'] = embedding_model.encode(title + ' ' + summary)
        es_client.index(index=index_name, document=doc)

def elastic_search_hybrid(query: str, index_name: str, es_client: Elasticsearch, embedding_model: SentenceTransformer) -> List[dict]: 
    v_q = embedding_model.encode(query)
    
    knn_query = {
        "field": "all_vec",
        "query_vector": v_q,
        "k": 5,
        "num_candidates": 10000,
        "boost": 0.8
    }

    keyword_query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "date", "summary", "tags"],
                    "type": "best_fields",
                    "boost": 0.2,
                }
            }
        }
    }

    response = es_client.search(
        index=index_name,
        query=keyword_query,
        knn=knn_query,
        size=5
    )

    result_docs = []

    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])

    return result_docs

def embedding_model(model_name: str) -> SentenceTransformer:
    try:
        return SentenceTransformer(model_name)
    except OSError:
        print("Sentence-transformer Model Name is Invalid.")
    



