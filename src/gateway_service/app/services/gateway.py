from uuid import UUID
import sys
from datetime import datetime

from cruds.library import LibraryCRUD
from cruds.reservation import ReservationCRUD
from cruds.rating import RatingCRUD
from schemas.library import (
  LibraryResponse,
  LibraryPaginationResponse,
  BookResponse,
  LibraryBookEntityResponse,
  LibraryBookResponse,
  LibraryBookPaginationResponse,
  LibraryBookUpdate,
)
from schemas.reservation import (
  Reservation,
  BookReservationResponse,
  TakeBookRequest,
  ReservationCreate,
  TakeBookResponse,
)
from schemas.rating import (
  Rating,
  UserRatingResponse,
)
from enums.status import ReservationStatus, ConditionStatus
from exceptions.http import BadRequestException, NotFoundException


class GatewayService():
  def __init__(
      self,
      libraryCRUD: LibraryCRUD,
      reservationCRUD: ReservationCRUD,
      ratingCRUD: RatingCRUD,
  ):
    self._libraryCRUD: LibraryCRUD = libraryCRUD()
    self._reservationCRUD: ReservationCRUD = reservationCRUD()
    self._ratingCRUD: RatingCRUD = ratingCRUD()

  async def get_all_libraries_in_city(
      self,
      city: str,
      page: int = 1,
      size: int = 100,
  ):
    libraries = await self._libraryCRUD.get_all_libraries(
      page=page,
      size=size,
      city=city,
    )

    return LibraryPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=libraries.totalElements,
      items=libraries.items,
    )
  

  async def get_books_in_library(
      self,
      library_uid: UUID,
      show_all: bool = False,
      page: int = 1,
      size: int = 100,
  ):
    library_books = await self._libraryCRUD.get_all_library_books(
      page=page,
      size=size,
    )

    library_book_items: list[LibraryBookResponse] = []
    for library_book in library_books:
      if library_book.library.libraryUid == library_uid:
        if library_book.availableCount != 0 or show_all == True:
          library_book_items.append(
            LibraryBookResponse(
              name=library_book.book.name,
              author=library_book.book.author,
              genre=library_book.book.genre,
              condition=library_book.book.condition,
              bookUid=library_book.book.bookUid,
              availableCount=library_book.availableCount,
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
  

  async def get_user_rating(
      self,
      X_User_Name: str,
  ):
    ratings: list[Rating] = await self._ratingCRUD.get_all_ratings(
      username=X_User_Name,
    )
    
    if ratings:
      if len(ratings) > 1:
        raise BadRequestException(prefix="get_user_rating")
    
      return UserRatingResponse(
        stars=ratings[0].stars,
      )
    else:
      raise NotFoundException(prefix="get_user_rating")
    

  async def take_book(
      self,
      X_User_Name: str,
      take_book_request: TakeBookRequest,
  ):
    user_rented_books = await self._reservationCRUD.get_all_reservations(
      size=sys.maxsize,
      username=X_User_Name,
      status=ReservationStatus.RENTED,
    )
    user_rating = await self.get_user_rating(
      X_User_Name=X_User_Name,
    )

    if (len(user_rented_books) >= user_rating.stars):
      raise BadRequestException(prefix="take_book")
    
    library_book = await self.__get_book_in_library(
      libraryUid=take_book_request.libraryUid,
      bookUid=take_book_request.bookUid,
    )

    if (library_book.availableCount == 0):
      raise BadRequestException(prefix="take_book")
    
    await self._libraryCRUD.patch_library_book(
      id=library_book.id,
      update=LibraryBookUpdate(
        available_count=library_book.availableCount - 1,
      ),
    )
    
    reservation_uid = await self._reservationCRUD.add_reservation(
      ReservationCreate(
        username=X_User_Name,
        library_uid=take_book_request.libraryUid,
        book_uid=take_book_request.bookUid,
        status=ReservationStatus.RENTED,
        start_date=datetime.now().strftime('%Y-%m-%d'),
        till_date=take_book_request.tillDate.strftime('%Y-%m-%d'), # ???
      )
    )

    reservation = await self._reservationCRUD.get_reservation_by_uid(
      uid=reservation_uid,
    )

    return TakeBookResponse(
      reservationUid=reservation.reservationUid,
      status=reservation.status,
      startDate=reservation.startDate,
      tillDate=reservation.tillDate,
      library=library_book.library,
      book=library_book.book,
      rating=user_rating,
    )


  async def __get_book_in_library(
      self,
      libraryUid: UUID,
      bookUid: UUID,
  ) -> LibraryBookEntityResponse:
    library_books = await self._libraryCRUD.get_all_library_books(
      size=sys.maxsize,
    )

    library_book_items: list[LibraryBookEntityResponse] = []
    for library_book in library_books:
      if library_book.book.bookUid == bookUid and library_book.library.libraryUid == libraryUid:
        library_book_items.append(
          library_book,
        )

    if len(library_book_items) > 1:
      raise BadRequestException(prefix="__get_book_in_library")
    elif len(library_book_items) == 0:
      raise NotFoundException(prefix="__get_book_in_library")
    else:
      return library_book_items[0]
