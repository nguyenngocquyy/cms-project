from fastapi import FastAPI

app = FastAPI(title="CMS Backend API")

@app.get("/")
def root():
    return {"message": "CMS Backend is running"}

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/posts")
def get_posts():
    sample_posts = [
        {
            "id": 1,
            "title": "First Post",
            "content": "This is the first sample post"
        },
        {
            "id": 2,
            "title": "Second Post",
            "content": "This is the second sample post"
        }
    ]
    return {"posts": sample_posts}
