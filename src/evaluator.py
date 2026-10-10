
def evaluate_retrieval(pipeline, test_cases, k=3):
    hits = 0
    reciprocal_rank_total = 0.0
    total = len(test_cases)

    if total == 0:
        raise ValueError("Evaluation dataset is empty.")

    for case in test_cases:
        results, _, _ = pipeline.retrieve(case["query"])

        ranked_chunks = [chunk for _, chunk in results[:k]]
        expected = set(case["expected_documents"])

        ranked_documents = [
            chunk.document_id for chunk in ranked_chunks
        ]

        relevant_ranks = [
            rank
            for rank, document_id in enumerate(
                ranked_documents, start=1
            )
            if document_id in expected
        ]

        hit = bool(relevant_ranks)
        hits += int(hit)

        if relevant_ranks:
            reciprocal_rank_total += 1 / relevant_ranks[0]

        print(f"\nQuery: {case['query']}")
        print(f"Expected documents: {sorted(expected)}")
        print(f"Retrieved documents: {ranked_documents}")
        print(f"Hit@{k}: {hit}")

    metrics = {
        f"hit_at_{k}": hits / total,
        f"mrr_at_{k}": reciprocal_rank_total / total
    }

    print(f"\nHit@{k}: {metrics[f'hit_at_{k}']:.2%}")
    print(f"MRR@{k}: {metrics[f'mrr_at_{k}']:.3f}")

    return metrics
