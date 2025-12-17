def rag_prompt(context, question):
    return f"""
You are answering questions based only on the provided scientific context.

Context:
{context}

Question:
{question}

Answer with citations.
"""
