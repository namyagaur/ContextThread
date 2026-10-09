
class ContextBuilder:

    def build(self, ranked_chunks, max_chunks=3):
        selected = ranked_chunks[:max_chunks]
        context_parts = []
        source_map = {}

        for i, (score, chunk) in enumerate(selected, start=1):
            source_id = f"SOURCE {i}"

            source_map[source_id] = {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "page_number": chunk.page_number,
                "text": chunk.text,
                "score": float(score)
            }

            context_parts.append(
                f"[{source_id}]\n"
                f"File: {chunk.document_id}\n"
                f"Page: {chunk.page_number or 'Unknown'}\n"
                f"Evidence:\n{chunk.text}"
            )

        return "\n\n".join(context_parts), source_map
