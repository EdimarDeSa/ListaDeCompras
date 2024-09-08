from sqlalchemy.orm import scoped_session, Session

from app.DataBase.models.dto_models import UnityTypeDTO
from app.Enums.enums import LangEnum, ResponseCode
from app.InternalResponse.internal_errors import InternalErrors
from app.Repositories.base_repository import BaseRepository


class UnityTypeRepository(BaseRepository):
    def read_all(self, db_session: scoped_session[Session], language: LangEnum) -> list[UnityTypeDTO]:
        self.db_session = db_session

        try:
            query = self._query.select_all_unity_types()

            result = self.db_session.execute(query).all()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.UNITY_TYPE_NOT_FOUND, language=language)

            unity_types: list[UnityTypeDTO] = [UnityTypeDTO.model_validate(data.UnityType) for data in result]

            return unity_types

        except Exception as e:
            self.return_db_error(e, language)

    def read_by_name(
        self, db_session: scoped_session[Session], unity_type_name: str, language: LangEnum
    ) -> UnityTypeDTO:
        self.db_session = db_session

        try:
            query = self._query.select_unity_type_by_name(unity_type_name)

            result = self.db_session.execute(query).first()

            if result is None:
                raise InternalErrors.NOT_FOUND_404(rc=ResponseCode.UNITY_TYPE_NOT_FOUND, language=language)

            unity_type: UnityTypeDTO = UnityTypeDTO.model_validate(result.UnityType)

            return unity_type

        except Exception as e:
            self.return_db_error(e, language)
