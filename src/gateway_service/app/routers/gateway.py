from fastapi import APIRouter, Depends, status, Query, Header
from fastapi.responses import Response
from typing import Annotated
from uuid import UUID


from cruds.library import LibraryCRUD
from enums.responses import RespEnum
from schemas.library import (
  LibraryPaginationResponse,
  LibraryBookPaginationResponse,
  )
from services.gateway import GatewayService


def get_library_crud() -> LibraryCRUD:
  return LibraryCRUD


router = APIRouter(
  tags=["Gateway API"],
  responses={
    status.HTTP_400_BAD_REQUEST: RespEnum.InvalidData.value,
  }
)


@router.get(
  "/libraries", 
  status_code=status.HTTP_200_OK,
  response_model=LibraryPaginationResponse,
  responses={
    status.HTTP_200_OK: RespEnum.GetAllLibraries.value,
  }
)
async def get_list_of_libraries(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    city: Annotated[str, Query(max_length=80)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD
    ).get_all_libraries_in_city(
      city=city,
      page=page,
      size=size
    )


@router.get(
  "/libraries/{libraryUid}/books",
  status_code=status.HTTP_200_OK,
  response_model=LibraryBookPaginationResponse,
  responses={
    status.HTTP_200_OK: RespEnum.GetAllBooksInLibrary.value,
  }
)
async def get_books_in_library(
    libraryCRUD: Annotated[LibraryCRUD, Depends(get_library_crud)],
    libraryUid: UUID,
    showAll: bool = False,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1)] = 100,
  ):
  return await GatewayService(
      libraryCRUD=libraryCRUD
    ).get_books_in_library(
      library_uid=libraryUid,
      show_all=showAll,
      page=page,
      size=size
    )

