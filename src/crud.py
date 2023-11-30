from sqlalchemy.orm import Session

import models, schema, utils


def get_link_by_uuid(db: Session, uuid: str):
    return db.query(models.Link).filter(models.Link.uuid == uuid).first()


def get_link(db: Session, id: int):
    return db.query(models.Link).filter(models.Link.id == id).first()


def get_links(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Link).offset(skip).limit(limit).all()


def create_link(db: Session, link: schema.LinkSchema):
    if not utils.is_valid_url(link.url):
        return None
    uuid = utils.generate_unique_string()
    db_link = models.Link(uuid=uuid, url=link.url)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link
