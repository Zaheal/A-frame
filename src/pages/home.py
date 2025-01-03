from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from .template import templates
from src.api.controllers.house_controllers import get_selected_house
from src.auth.user import current_active_user
from src.models.core_models import User
from src.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_class=HTMLResponse)
def homepage(
        request: Request,
        user: User | None = Depends(current_active_user),
        ):
    """

    :param request:
    :return:
    """

    return templates.TemplateResponse(request, "/homepage.html", context={'user': user})


@router.get("/house/{house_id}", response_class=HTMLResponse)
async def house_page(
        request: Request,
        data=Depends(get_selected_house),
        user: User | None = Depends(current_active_user),
        ):
    """
    
    :param request:
    :param data:
    :return:
    """

    booked_dates = []
    for reserv in data.busy_times:
        if reserv.end.date() < datetime.now().date():
            booked_dates.append([str(reserv.start)[:10], str(reserv.end)[:10]])

    if not booked_dates:
        booked_dates.append(["2023-01-01", "2023-01-02"])
    
    return templates.TemplateResponse(request, "/house-page.html", context={"data": data, "booked_dates": booked_dates, "user": user})
