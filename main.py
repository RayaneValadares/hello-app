from fastapi import FastAPI 

app = FastAPI() 

@app.get("/") 
async def root(): 
    return {"message": "Olá, esse é o resultado do meu projeto de CI/CD com o Github Actions"}
    