import json
import os
import streamlit as st

from langchain_core.documents import Document

_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@st.cache_resource(show_spinner=False)
def get_embeddings():
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=_EMBED_MODEL)


@st.cache_resource(show_spinner=False)
def get_db(persist_dir: str = "chroma_db"):
    from langchain_chroma import Chroma
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=get_embeddings(),
    )


def build_corpus_index(corpus_dir: str = "corpus", persist_dir: str = "chroma_db") -> int:
    from langchain_chroma import Chroma
    embeddings = get_embeddings()
    documents = []
    for fname in sorted(os.listdir(corpus_dir)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(corpus_dir, fname), encoding="utf-8") as f:
            prd = json.load(f)
        embed_text = prd["title"] + " " + prd["problem_statement"]
        documents.append(Document(
            page_content=embed_text,
            metadata={"full_prd": json.dumps(prd)},
        ))
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
    )
    return len(documents)


def _load_db(persist_dir: str):
    return get_db(persist_dir)


def retrieve_similar_prds(query: str, k: int = 2, persist_dir: str = "chroma_db") -> str:
    results = get_db(persist_dir).similarity_search(query, k=k)
    blocks = []
    for i, doc in enumerate(results, 1):
        prd = json.loads(doc.metadata["full_prd"])
        ac_sample = prd.get("acceptance_criteria", [])[:2]
        sm_sample = prd.get("success_metrics", [])[:2]
        block = f"--- Example {i}: {prd['title']} ---\n"
        block += f"Problem: {prd['problem_statement']}\n"
        if ac_sample:
            block += "Acceptance Criteria (sample):\n"
            for ac in ac_sample:
                block += f"  - {ac}\n"
        if sm_sample:
            block += "Success Metrics (sample):\n"
            for sm in sm_sample:
                block += f"  - {sm.get('metric', '')}: baseline {sm.get('baseline', '')}, target {sm.get('target', '')}\n"
        if len(block) > 1500:
            block = block[:1497] + "..."
        blocks.append(block)
    return "\n\n".join(blocks)


def get_similar_prd_metas(query: str, k: int = 2, persist_dir: str = "chroma_db") -> list[dict]:
    results = get_db(persist_dir).similarity_search(query, k=k)
    return [json.loads(doc.metadata["full_prd"]) for doc in results]
