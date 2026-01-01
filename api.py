import streamlit as st
from rag_core import answer
from fastapi import FastAPI, Request, HTTPException, status

app = FastAPI()


@app.post("/chat")
async def get_answer(request: Request):
    payload = await request.json()

    query = payload.get("query")

    if not query:
        raise HTTPException(status_code=400, detail="The 'query' param is required")

    try:
        resp, rows = answer(query, k=5)

        # Format the context rows
        context_list = [
            {
                "source": row[0],
                "chunk": row[1],
                "modality": row[2] if len(row) > 2 else "text",
                "score": row[3] if len(row) > 3 else 0,
            }
            for row in rows
        ]
        return {"response": resp, "context": context_list}

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
