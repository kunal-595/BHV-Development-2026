import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, create_engine, SQLModel, select
from models import PatientRecord
from github_service import create_private_vault, upload_file_to_vault

# 1. Database Connection setup
sqlite_url = "sqlite:///database/vault.db"
engine = create_engine(sqlite_url)

# 2. Lifespan for clean startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This ensures the database is created properly on start
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

# 3. Setup Folders
os.makedirs("database", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
templates = Jinja2Templates(directory="templates")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 4. Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with Session(engine) as session:
        # Fetching all records for the Recovery Gallery
        statement = select(PatientRecord)
        records = session.exec(statement).all()
    return templates.TemplateResponse("index.html", {"request": request, "records": records})

@app.post("/upload")
async def handle_upload(
    patient_name: str = Form(...),
    narrative: str = Form(...),
    file: UploadFile = Form(...)
):
    file_location = f"uploads/{file.filename}"
    
    with Session(engine) as session:
        # DEDUPLICATION CHECK: prevents the 'double image' issue
        existing = session.exec(select(PatientRecord).where(
            PatientRecord.patient_name == patient_name,
            PatientRecord.narrative == narrative
        )).first()
        
        if not existing:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            new_record = PatientRecord(
                patient_name=patient_name,
                narrative=narrative,
                image_path=file_location
            )
            session.add(new_record)
            session.commit()
            
            # GitHub Cloud Sync
            try:
                repo_name = create_private_vault(patient_name)
                if repo_name:
                    upload_file_to_vault(repo_name, file_location)
                    print(f"--- SUCCESS: Cloud Vault updated for {patient_name} ---")
            except Exception as e:
                print(f"Cloud error (check token/connection): {e}")

    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)