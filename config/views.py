from pathlib import Path
from fastapi import Depends
from fastapi.templating import Jinja2Templates
from typing import Annotated
from inertia import InertiaConfig, inertia_dependency_factory, Inertia

TEMPLATES_DIR = Path("templates")

MAIL_DIR = TEMPLATES_DIR / "mail" / "emails"

MAIL_TEMPLATE = MAIL_DIR / "report.html"

templates = Jinja2Templates(directory=TEMPLATES_DIR)
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
