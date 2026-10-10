
class ContextBuilder:

    def build(self, ranked_chunks, max_chunks=3):
        context_parts = []
        source_map = {}

        for i, (score, chunk) in enumerate(
            ranked_chunks[:max_chunks], start=1
        ):
            label = f"SOURCE {i}"

            source_map[label] = {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "text": chunk.text,
                "score": float(score)
            }

            context_parts.append(
                f"[{label}]\n"
                f"Document: {chunk.document_id}\n"
                f"Page: {chunk.page_number or 'Unknown'}\n"
                f"Evidence:\n{chunk.text}"
            )

        return "\n\n".join(context_parts), source_map
