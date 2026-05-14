from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return {"body": "Hi"}



def main():
    uvicorn.run(app, port=8080, host="localhost")


if __name__ == "__main__":
    main()
