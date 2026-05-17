from retrieval import build_corpus_index

if __name__ == "__main__":
    n = build_corpus_index()
    print(f"Index built with {n} PRDs")
