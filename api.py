
import streamlit as st
from rag_core import answer
from fastapi import  FastAPI, Request,HTTPException,status

app = FastAPI()


@app.post("/chat")
async def get_answer(request: Request):
    payload = await request.json()
    
    question = payload.get("question")  
    
    try:
        resp, rows = answer(question, k=5)

        return {"answer": resp}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
        

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

