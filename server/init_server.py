import shutil
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, Request, Response, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from telegram import Update

from db.db import init_db
from db.product_crud import create_product, get_all_products
from server.routers.products import router as products_router


def init_server():
    app = FastAPI(lifespan=lifespan)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates("templates")
    app.include_router(products_router, prefix="/api")
    

    @app.get("/")
    async def read_root(request: Request):
        return JSONResponse({"message": "OK"})

    @app.post("/telegram")
    async def get_update(request: Request):
        payload = await request.json()
        update = Update.de_json(payload, request.app.state.bot_app.bot)
        await request.app.state.bot_app.update_queue.put(update)
        return Response(status_code=status.HTTP_200_OK)

    @app.get("/timur")
    async def timur(request: Request):
        await request.app.state.bot_app.bot.send_message(
            chat_id=1668408264, text="кто то зашёл на страницу"
        )
        return JSONResponse({"message": "OK"})

    @app.get("/products")
    async def products(request: Request):
        products = await get_all_products()
        return templates.TemplateResponse(
            request,
            "index.html",
            {"request": request, "products": products},
        )
    @app.post("/create_product")
    async def create_product_view(
        request: Request,
        title: str = Form(...),
        price: int = Form(...),
        photo: UploadFile = File(...),
        description: str = Form(...),
    ):
        file_path = f"static/uploads/{photo.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        await create_product(title, price, file_path, description)
        return RedirectResponse("/products", 301)

    @app.get("/api/products")
    async def get_products(request: Request):
        products = await get_all_products()
        return [
            {
                "id": p.id,
                "title": p.name,
                "price": p.price,
                "desription": p.description,
                "photo": "/" + p.photo,
            }
            for p in products
        ]

    @app.get("/add_product")
    async def add_product(request: Request):
        return templates.TemplateResponse(
            request,
            "add_product.html",
            {
                "request": request,
            },
        )
    
    @app.get('/product/{product_id}')
    async def product_page(
        request: Request,
        product_id: int,
    ):
        return templates.TemplateResponse(
            request,
            "product.html",
            {
                "request": request,
            
            },
        )

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    # запуск приложения
    await init_db()

    # bot_app = init_bot()
    # app.state.bot_app = bot_app
    # await bot_app.initialize()
    # await bot_app.start()
    # await bot_app.bot.set_webhook(WEBHOOK_URL + "/telegram")
    yield
    # конец приложения
