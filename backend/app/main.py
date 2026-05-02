from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_connection

app = FastAPI(title="CMS Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CMS Backend is running"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/posts")
def get_posts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, content FROM posts ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    posts = []
    for row in rows:
        posts.append({
            "id": row[0],
            "title": row[1],
            "content": row[2]
        })

    return {"posts": posts}
