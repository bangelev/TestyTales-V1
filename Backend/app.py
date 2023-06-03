from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from routes.recipes_routes import recipes_router
from routes.auth_routes import auth_router
from routes.users_routes import user_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GET method for root page


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Doesn't expect anything

    Returns a "beautiful" home page.
    """
    html_content = """
    <html>
        <head>
            <title>Testy Tales</title>
        </head>
        <body>
            <h1 style="text-align: center; margin-top: 250px; font-size: 2.5rem">Welcome to the mind-blowingly stunning landing page of Testy Tales!</h1>
            <p style="padding: 0 50px 0 50px; font-size: 1.8rem">Brace yourself for a truly imaginary culinary experience that will leave you craving for non-existent flavors and tantalizing dishes that only exist in the realm of pure imagination! Prepare to be captivated by the invisible aromas and taste the sheer absence of flavors!</p>
            <p style="padding: 0 50px 0 50px; font-size: 1rem; text-align: center; color:grey ">P.S. If the developer wasn't lazy, it would be ... a landing page! Danke!!</p>
        </body>
    </html>
    """

    return html_content
app.include_router(recipes_router)
app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("app:app",
                host='0.0.0.0',
                port=4000,
                reload=True,
                log_level="info")
