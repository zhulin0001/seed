from flask import request, g

from seed.schema.base import BaseSchema
# from seed.api.endpoints._base import RestfulBaseView
from seed.api.endpoints.buser import Buser
from seed.models.databases import Databases as DatabasesModel
from seed.utils.auth import api_require_admin

class DatabasesSchema(BaseSchema):
    class Meta:
        model = DatabasesModel

class Databases(Buser):
    """ 数据库设置
    """
    model_class = DatabasesModel
    schema_class = DatabasesSchema
    decorators = [api_require_admin]

    def get(self, bussiness_id):
        """ 通过业务ID得到数据库列表
        """
        query_session = self.session.query(self.model_class)
        datas = query_session.filter(self.model_class.bussiness_id==bussiness_id).all()
        datas = [row.row2dict() for row in datas] if datas else []
        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)

    def put(self, bussiness_id):
        input_json = request.get_json()

        schema = self.schema_class()
        databases, errors = schema.load(input_json)
        if errors:
            return self.response_json(self.HttpErrorCode.PARAMS_VALID_ERROR, msg=errors)
        databases.save()

        common_batch_crud(DatabasesSchema, DatabasesModel, databases)

        datas, errors = DatabasesSchema(many=True).dump(databases)

        return self.response_json(self.HttpErrorCode.SUCCESS, data=datas)