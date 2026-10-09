class ContextBuilder:

    def build(self, ranked_chunks, max_chunks=3):
        selected = ranked_chunks[:max_chunks]

        context_parts = []

        for i, (score, chunk) in enumerate(selected, start=1):
            context_parts.append(
                f"[SOURCE {i}]\n"
                f"Chunk ID: {chunk.id}\n"
                f"{chunk.text}"
            )

        return "\n\n".join(context_parts)