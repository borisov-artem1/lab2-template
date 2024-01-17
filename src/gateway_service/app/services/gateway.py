from uuid import UUID
from cruds.library import LibraryCRUD
from cruds.reservation import ReservationCRUD

from schemas.library import (
  LibraryResponse,
  LibraryPaginationResponse,
  BookResponse,
  LibraryBookEntityResponse,
  LibraryBookResponse,
  LibraryBookPaginationResponse
)

from schemas.reservation import (
  Reservation,
  BookReservationResponse,
)


class GatewayService():
  def __init__(
      self,
      libraryCRUD: LibraryCRUD,
      reservationCRUD: ReservationCRUD,
  ):
    self._libraryCRUD: LibraryCRUD = libraryCRUD()
    self._reservationCRUD: ReservationCRUD = reservationCRUD()

  async def get_all_libraries_in_city(
      self,
      city: str,
      page: int = 1,
      size: int = 100,
  ):
    libraries_json = await self._libraryCRUD.get_all_libraries(
      page=page,
      size=size,
      city=city,
    )

    return LibraryPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=libraries_json["totalElements"],
      items=libraries_json["items"],
    )
  

  async def get_books_in_library(
      self,
      library_uid: UUID,
      show_all: bool = False,
      page: int = 1,
      size: int = 100,
  ):
    library_books_json = await self._libraryCRUD.get_all_library_books(
      page=page,
      size=size,
    )

    library_books: list[LibraryBookEntityResponse] = library_books_json["items"]

    library_book_items: list[LibraryBookResponse] = []
    for library_book in library_books:
      print(f"\n\n\n{library_book['library']['library_uid']}\n\n\n")

      if library_book["library"]["library_uid"] == str(library_uid):
        if int(library_book["available_count"]) != 0 or show_all == True:
          library_book_items.append(
            LibraryBookResponse(
              name=library_book["book"]["name"],
              author=library_book["book"]["author"],
              genre=library_book["book"]["genre"],
              condition=library_book["book"]["condition"],
              bookUid=library_book["book"]["book_uid"],
              availableCount=library_book["available_count"],
            )
          )

    return LibraryBookPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=len(library_book_items),
      items=library_book_items[(page - 1) * size : page * size]
    )
  
  
  async def get_user_rented_books(
      self,
      X_User_Name: str,
      page: int = 1,
      size: int = 100,
  ):
    reservations: list[Reservation] = await self._reservationCRUD.get_all_reservations(
      page=page,
      size=size,
      username=X_User_Name,
    )

    book_reservations: list[BookReservationResponse] = []
    for reservation in reservations:
      library: LibraryResponse = await self._libraryCRUD.get_library_by_uid(reservation.libraryUid)
      book: BookResponse = await self._libraryCRUD.get_book_by_uid(reservation.bookUid)

      book_reservations.append(
        BookReservationResponse(
          reservationUid=reservation.reservationUid,
          username=reservation.username,
          status=reservation.status,
          startDate=reservation.startDate,
          tillDate=reservation.tillDate,
          library=library,
          book=book,
        )
      )

    return book_reservations

