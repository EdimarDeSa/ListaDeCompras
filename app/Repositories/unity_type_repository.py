from sqlalchemy import Sequence
from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.dto_models import UnityTypeDTO
from app.DataBase.schemas.unity_type_schema import UnityType
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UnityTypeRepository(BaseRepository):
    def __init__(self):
        self._query = self.create_query()
        self._logger = self.create_logger(__name__)

    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[UnityTypeDTO]:
        try:
            self._logger.debug("Trying to get all unity types")
            query = self._query.select_all_unity_types()

            result: Sequence[UnityType] = db_session.execute(query).scalars().all()
            self._logger.info(f"Unity types found: {result}")

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.UNITY_TYPE_NOT_FOUND, language=language)

            unity_types: list[UnityTypeDTO] = [UnityTypeDTO.model_validate(u, from_attributes=True) for u in result]

            return unity_types

        except Exception as e:
            self.return_db_error(e, language)

    def read_by_name(
        self, db_session: scoped_session[Session], unity_type_name: str, language: LangEnum
    ) -> UnityTypeDTO:
        try:
            self._logger.debug(f"Trying to get unity type by name: {unity_type_name}")
            query = self._query.select_unity_type_by_name(unity_type_name)

            result: UnityType = db_session.execute(query).scalars().first()
            self._logger.info(f"Unity type found: {result}")

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.UNITY_TYPE_NOT_FOUND, language=language)

            unity_type: UnityTypeDTO = UnityTypeDTO.model_validate(result)

            return unity_type

        except Exception as e:
            self.return_db_error(e, language)
