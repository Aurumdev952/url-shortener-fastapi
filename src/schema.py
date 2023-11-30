from pydantic import BaseModel


class LinkSchema(BaseModel):
    url: str
    alias: str | None

    class Config:
        from_attributes = True


class Link(LinkSchema):
    id: int
    uuid: str
    is_active: bool

    class Config:
        from_attributes = True
