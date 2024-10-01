from fastapi import FastAPI, Depends, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_forklifts(request: Request, search: str = "", db: Session = Depends(get_db)):
    forklifts = db.query(models.Forklift)
    if search:
        search = search.strip()
        forklifts = forklifts.filter(models.Forklift.number.ilike(f"%{search}%"))
    forklifts = forklifts.all()
    return templates.TemplateResponse("index.html", {"request": request, "forklifts": forklifts, "search": search})

@app.post("/forklifts/add")
def add_forklift(brand: str = Form(...), number: str = Form(...), capacity: float = Form(...), db: Session = Depends(get_db)):
    forklift = models.Forklift(brand=brand, number=number, capacity=capacity)
    db.add(forklift)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.post("/forklifts/edit/{forklift_id}")
def edit_forklift(forklift_id: int, brand: str = Form(...), number: str = Form(...), capacity: float = Form(...), db: Session = Depends(get_db)):
    forklift = db.query(models.Forklift).filter(models.Forklift.id == forklift_id).first()
    if not forklift:
        raise HTTPException(status_code=404, detail="Forklift not found")
    forklift.brand = brand
    forklift.number = number
    forklift.capacity = capacity
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.get("/forklifts/delete/{forklift_id}")
def delete_forklift(forklift_id: int, db: Session = Depends(get_db)):
    forklift = db.query(models.Forklift).filter(models.Forklift.id == forklift_id).first()
    if not forklift:
        raise HTTPException(status_code=404, detail="Forklift not found")
    if forklift.downtimes:
        return RedirectResponse(url="/?error=Cannot delete forklift with downtimes", status_code=status.HTTP_302_FOUND)
    db.delete(forklift)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.post("/downtimes/edit/{downtime_id}")
def edit_downtime(
    downtime_id: int,
    forklift_id: int = Form(...),
    start_time: str = Form(...),
    end_time: Optional[str] = Form(None),
    reason: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    downtime = db.query(models.Downtime).filter(models.Downtime.id == downtime_id).first()
    if downtime:
        downtime.forklift_id = forklift_id
        downtime.start_time = datetime.fromisoformat(start_time)
        downtime.end_time = datetime.fromisoformat(end_time) if end_time else None
        downtime.reason = reason
        db.commit()
        return Response(status_code=200)
    else:
        return Response(status_code=404)

@app.delete("/downtimes/delete/{downtime_id}")
def delete_downtime(
    downtime_id: int,
    db: Session = Depends(get_db)
):
    downtime = db.query(models.Downtime).filter(models.Downtime.id == downtime_id).first()
    if downtime:
        db.delete(downtime)
        db.commit()
        return Response(status_code=200)
    else:
        return Response(status_code=404)

def calculate_downtime_duration(downtime: models.Downtime):
    end_time = downtime.end_time or datetime.utcnow()
    duration = end_time - downtime.start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes = remainder // 60

    if hours > 0:
        downtime_duration = f"{int(hours)} часов, {int(minutes)} минут"
    else:
        downtime_duration = f"{int(minutes)} минут"

    downtime_schema = schemas.Downtime(
        id=downtime.id,
        forklift_id=downtime.forklift_id,
        start_time=downtime.start_time,
        end_time=downtime.end_time,
        downtime_duration=downtime_duration,
        reason=downtime.reason
    )
    return downtime_schema

@app.get("/api/forklifts/{forklift_id}/downtimes")
def get_downtimes(forklift_id: int, db: Session = Depends(get_db)):
    downtimes = db.query(models.Downtime).filter(models.Downtime.forklift_id == forklift_id).order_by(models.Downtime.start_time.desc()).all()
    return [calculate_downtime_duration(dt) for dt in downtimes]

@app.post("/downtimes/add")
def add_downtime(
    forklift_id: int = Form(...),
    start_time: str = Form(...),
    end_time: Optional[str] = Form(None),
    reason: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time) if end_time else None

    downtime = models.Downtime(
        forklift_id=forklift_id,
        start_time=start_time,
        end_time=end_time,
        reason=reason
    )
    db.add(downtime)
    db.commit()
    return RedirectResponse(url="/", status_code=302)
