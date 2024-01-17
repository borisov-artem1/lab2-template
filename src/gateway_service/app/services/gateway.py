from cruds.library import LibraryCRUD

from schemas.library import LibraryResponse, LibraryPaginationResponse


class GatewayService():
  def __init__(
      self,
      libraryCRUD: LibraryCRUD, 
  ):
    self._libraryCRUD: LibraryCRUD = libraryCRUD()

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
