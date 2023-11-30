import random
import string
import time
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import starlette.status as status
import logging
import uvicorn

import crud, schema
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Url Shortener", debug=True)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        print("db connected", db)
        yield db
    finally:
        db.close()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


@app.get("/")
async def root():
    print("Test")
    return "Welcome to urls shortener"


@app.post("/link", response_model=schema.Link)
async def create_link(link: schema.LinkSchema, db: Session = Depends(get_db)):
    # raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_link(db=db, link=link)


@app.get("/links", response_model=list[schema.Link])
async def read_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    links = crud.get_links(db, skip=skip, limit=limit)
    logger.info("Read links", links)
    return links


@app.get("/{uuid}")
async def redirect_link(uuid: str, db: Session = Depends(get_db)):
    link = crud.get_link_by_uuid(db=db, uuid=uuid)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link.url, status_code=status.HTTP_301_MOVED_PERMANENTLY)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
