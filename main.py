from inertia import InertiaResponse
from config.views import InertiaDependency
from config.app import app
from services.db import hungry


@app.get("/", response_model=None)
async def index(inertia: InertiaDependency) -> InertiaResponse:
    print("hello")
    return await inertia.render("Index", {"name": "connor"})
