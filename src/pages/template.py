from fastapi.templating import Jinja2Templates

from src.config.project_config import get_settings

settings = get_settings()

templates = Jinja2Templates(directory=f"{settings.TEMPLATE_URL}")
