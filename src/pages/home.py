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


# Функция для генерации всех дат в диапазоне
def get_dates_in_range(start_date, end_date):
    current_date = datetime.today().date()
    if end_date >= current_date:
        delta = end_date - start_date
        return [start_date.strftime('%Y-%m-%d') for i in range(delta.days)]


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
        booked_dates.append([str(reserv.start)[:10], str(reserv.end)[:10]])

    
    return templates.TemplateResponse(request, "/house-page.html", context={"data": data, "booked_dates": booked_dates, "user": user})
