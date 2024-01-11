from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from cruds.library_book import LibraryBookCRUD
from enums.responses import RespLibraryBookEnum
from schemas.library_book import LibraryBook, LibraryBookFilter, LibraryBookCreate, LibraryBookUpdate, ConditionStatus
from utils.database import get_db
from services.library_book import LibraryBookService


def get_library_book_crud() -> LibraryBookCRUD:
  return LibraryBookCRUD


router = APIRouter(
  prefix="/library_book",
  tags=["LibraryBook REST API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespLibraryBookEnum.InvalidData.value,
  },
)


@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=list[LibraryBook],
  responses={
    status.HTTP_200_OK: RespLibraryBookEnum.GetAll.value,
  }
)
async def get_all_library_book(
  db: Annotated[Session, Depends(get_db)],
  library_bookCRUD: Annotated[LibraryBookCRUD, Depends(get_library_book_crud)],
  library_id: Annotated[int | None, Query(ge=1)] = None,
  book_id: Annotated[int | None, Query(ge=1)] = None,
  available_count: Annotated[int | None, Query(ge=1)] = None,
  page: Annotated[int, Query(ge=1)] = 1,
  size: Annotated[int, Query(ge=1)] = 100,
):
  return await LibraryBookService(
    library_bookCRUD=library_bookCRUD,
    db=db,
  ).get_all(
      filter=LibraryBookFilter(
        library_id=library_id,
        book_id=book_id,
        available_count=available_count,
      ),
      page=page,
      size=size,
    )


@router.get(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBook,
  responses={
    status.HTTP_200_OK: RespLibraryBookEnum.GetByUID.value,
    status.HTTP_404_NOT_FOUND: RespLibraryBookEnum.NotFound.value,
  },
)
async def get_library_book_by_uid(
  db: Annotated[Session, Depends(get_db)],
  library_bookCRUD: Annotated[LibraryBookCRUD, Depends(get_library_book_crud)],
  uid: UUID,
):
  return await LibraryBookService(
    library_bookCRUD=library_bookCRUD,
    db=db,
  ).get_by_uid(
    uid=uid,
  )


@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_class=Response,
  responses={
    status.HTTP_201_CREATED: RespLibraryBookEnum.Created.value,
  },
)
async def create_library_book(
  db: Annotated[Session, Depends(get_db)],
  library_bookCRUD: Annotated[LibraryBookCRUD, Depends(get_library_book_crud)],
  library_book_create: LibraryBookCreate,
):
  library_book = await LibraryBookService(
    library_bookCRUD=library_bookCRUD,
    db=db,
  ).create(
    library_book_create=library_book_create,
  )

  return Response(
    status_code=status.HTTP_201_CREATED,
    headers={"Location": f"/api/v1/library_book/{library_book.library_book_uid}"}
  )


@router.patch(
  "/{uid}",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBook,
  responses={
    status.HTTP_200_OK: RespLibraryBookEnum.Patch.value,
    status.HTTP_404_NOT_FOUND: RespLibraryBookEnum.NotFound.value,
  },
)
async def update_library_book(
  db: Annotated[Session, Depends(get_db)],
  library_bookCRUD: Annotated[LibraryBookCRUD, Depends(get_library_book_crud)],
  uid: UUID,
  library_book_update: LibraryBookUpdate,
):
  return await LibraryBookService(
    library_bookCRUD=library_bookCRUD,
    db=db,
  ).patch(
    uid=uid,
    library_book_patch=library_book_update,
  )


@router.delete(
  "/{uid}/",
  status_code=status.HTTP_204_NO_CONTENT,
  response_class=Response,
  responses={
    status.HTTP_204_NO_CONTENT: RespLibraryBookEnum.Delete.value,
    status.HTTP_404_NOT_FOUND: RespLibraryBookEnum.NotFound.value,
  },
)
async def delete_library_book(
  db: Annotated[Session, Depends(get_db)],
  library_bookCRUD: Annotated[LibraryBookCRUD, Depends(get_library_book_crud)],
  uid: UUID,
):
  return await LibraryBookService(
    library_bookCRUD=library_bookCRUD,
    db=db,
  ).delete(
    uid=uid,
  )
