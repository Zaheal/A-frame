from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.api.controllers.house_controllers import set_user_id_in_cookie, get_selected_house
from .template import templates


router = APIRouter(tags=['pages'])


@router.get("/", response_class=HTMLResponse)
def homepage(
        request: Request,
        operations=Depends(set_user_id_in_cookie)
        ):
    """

    :param request:
    :param operations:
    :return:
    """

    return templates.TemplateResponse(request, "index.html")
