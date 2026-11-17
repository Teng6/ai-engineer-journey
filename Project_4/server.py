from fastapi import FastAPI
from fastapi.responses import FileResponse
from Project_4.search_app import search


app = FastAPI()

@app.get("/")
def home():
    return FileResponse("Project_4/index.html")


@app.get("/search")
def search_route(q: str):
    if q.strip() == "":
        return {"query": q, "results": []}
    results = search(q)
    return {
        "query": q,
        "results": [{"score": float(s), "doc": d} for s, d in results]
    }