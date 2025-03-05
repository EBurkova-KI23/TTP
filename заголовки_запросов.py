from fastapi import FastAPI, Request, HTTPException
import re

app = FastAPI()

@app.get("/headers")
def get_headers(request: Request):
    user_agent = request.headers.get("User-Agent")
    accept_language = request.headers.get("Accept-Language")

    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing required headers")

    # Пример простого регулярного выражения для проверки формата Accept-Language
    if not re.match(r"^[a-z]{2}-[A-Z]{2}(,[a-z]{2};q=\d\.\d)?(,[a-z]{2};q=\d\.\d)?$", accept_language):
        raise HTTPException(status_code=400, detail="Invalid 'Accept-Language' format")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


# uvicorn заголовки_запросов:app --reload
#curl -X GET "http://127.0.0.1:8000/headers" -H "User-Agent: Mozilla/5.0" -H "Accept-Language: en-US,en;q=0.9,es;q=0.8"
#curl -X GET "http://127.0.0.1:8000/headers" -H "User-Agent: Mozilla/5.0"
#curl -X GET "http://127.0.0.1:8000/headers" -H "User-Agent: Mozilla/5.0" -H "Accept-Language: invalid-format"