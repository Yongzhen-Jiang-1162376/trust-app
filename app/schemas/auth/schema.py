from marshmallow import Schema, fields, validate
from app.schemas.hr.schema import PortfolioSchema


class AuthUserSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str()
    email = fields.Str()
    title = fields.Str()
    is_superadmin = fields.Bool()
    is_active = fields.Bool()
    is_blocked = fields.Bool()
    portfolios = fields.Nested(PortfolioSchema(only=('id', 'portfolio')), many=True)
