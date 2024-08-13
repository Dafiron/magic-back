from fastapi import FastAPI
from routers import login,numbers_sql


app = FastAPI(
    title= "Magic Tricks Back.",
    version="0.1 BETA",
    description= "Backend perteneciente a el proyecto Magic Tricks : Dafiron"
)

app.include_router(login.router)
app.include_router(numbers_sql.router)

@app.get("/")
async def root():
    return "Magic Tricks Backend: En linea"