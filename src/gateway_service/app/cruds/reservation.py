from uuid import UUID
import requests
from requests import Response

from cruds.base import BaseCRUD
from utils.settings import get_settings

from schemas.reservation import Reservation


class ReservationCRUD(BaseCRUD):
  def __init__(self):
    settings = get_settings()
    reservation_host = settings["services"]["gateway"]["reservation_host"]
    reservation_port = settings["services"]["reservation"]["port"]

    self.http_path = f'http://{reservation_host}:{reservation_port}/api/v1/'

  async def get_all_reservations(
      self,
      page: int = 1,
      size: int = 100,
      username: str | None = None,
  ):
    response: Response = requests.get(
      url=f'{self.http_path}reservation/?page={page}&size={size}'\
        f'{f"&username={username}" if username else ""}'
    )
    self._check_status_code(response.status_code)

    reservation_json: list[Reservation] = response.json()

    reservations = []
    for reservation in reservation_json:
      reservations.append(
        Reservation(
          reservationUid=reservation["reservation_uid"],
          username=reservation["username"],
          bookUid=reservation["book_uid"],
          libraryUid=reservation["library_uid"],
          status=reservation["status"],
          startDate=reservation["start_date"],
          tillDate=reservation["till_date"],
        )
      )
    
    return reservations
