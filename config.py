from pathlib import Path
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from typing import Annotated
from inertia import InertiaConfig, inertia_dependency_factory, Inertia

templates = Jinja2Templates(directory=Path("templates"))

manifest_json = Path("views") / "src"

inertia_config = InertiaConfig(
    templates=templates,
    manifest_json_path=f"{manifest_json}",
    environment="development",
    use_flash_messages=True,
    use_flash_errors=True,
    entrypoint_filename="main.js",
    assets_prefix="/static",
)

inertia_dependency = inertia_dependency_factory(inertia_config)

InertiaDependency = Annotated[Inertia, Depends(inertia_dependency)]

views_dir = Path(".") / "views"
