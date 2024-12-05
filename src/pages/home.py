from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from .template import templates
from src.api.controllers.house_controllers import get_selected_house


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def homepage(
        request: Request,
        ):
    """

    :param request:
    :return:
    """

    return templates.TemplateResponse(request, "homepage.html")


@router.get("/house/{house_id}", response_class=HTMLResponse)
async def house_page(
        request: Request,
        data=Depends(get_selected_house)
        ):
    """
    
    :param request:
    :param data:
    :return:
    """

    return templates.TemplateResponse(request, "house-page.html", context={"data": data})
