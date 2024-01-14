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

    libraries = []
    for lib_dict in libraries_json:
      libraries.append(
        LibraryResponse(
          name=lib_dict["name"],
          city=lib_dict["city"],
          address=lib_dict["address"],
          library_uid=lib_dict["library_uid"],
        )
      )

    return LibraryPaginationResponse(
      page=page,
      size=size,
      totalElemnts=len(libraries),
      items=libraries,
    )
