import shutil
from fastapi import  UploadFile, File, HTTPException, Depends, APIRouter
from sqlalchemy.orm import  Session
from datetime import datetime
from pathlib import Path
from app.core import get_db, settings
from app.models import AnalysisRecord, FileRecord


from app.services import mock_ai_analyze, analyze_with_openai

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": settings.APP_NAME + " Service API",
        "version": settings.VERSION,
        "endpoints": {
            "upload": "POST /files/upload",
            "list": "GET /files",
            "analyze": "POST /files/{file_id}/analyze",
            "get_analysis": "GET /files/{file_id}/analysis"
        }
    }

@router.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        existing_files = db.query(FileRecord).filter(
            FileRecord.original_name == file.filename
        ).order_by(FileRecord.version.desc()).all()
        
        version = 1
        if existing_files:
            version = existing_files[0].version + 1
        
        file_extension = Path(file.filename).suffix
        base_name = Path(file.filename).stem
        versioned_filename = f"{base_name}_v{version}{file_extension}"
        file_path = settings.STORAGE_DIR / versioned_filename
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = file_path.stat().st_size
        
        file_record = FileRecord(
            original_name=file.filename,
            version=version,
            path=str(file_path),
            file_size=file_size,
            uploaded_by=1
        )
        
        db.add(file_record)
        db.commit()
        db.refresh(file_record)
        
        return {
            "message": "File uploaded successfully",
            "file_id": file_record.id,
            "original_name": file_record.original_name,
            "version": file_record.version,
            "size": file_record.file_size,
            "uploaded_at": file_record.uploaded_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/files")
def list_files(db: Session = Depends(get_db)):
    files = db.query(FileRecord).order_by(FileRecord.uploaded_at.desc()).all()
    
    result = []
    for file_record in files:
        result.append({
            "id": file_record.id,
            "name": file_record.original_name,
            "version": file_record.version,
            "size": file_record.file_size,
            "uploaded_at": file_record.uploaded_at.isoformat(),
            "uploaded_by": file_record.uploaded_by
        })
    
    return {"files": result, "total": len(result)}

@router.post("/files/{file_id}/analyze")
def analyze_file(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_data = {
        "file_name": file_record.original_name,
        "file_size": file_record.file_size,
        "version": file_record.version,
        "uploaded_at": file_record.uploaded_at.isoformat()
    }
    
    analysis_result = mock_ai_analyze(file_data)
    # analysis_result = analyze_with_openai(file_data)
    
    existing_analysis = db.query(AnalysisRecord).filter(
        AnalysisRecord.file_id == file_id
    ).first()
    
    if existing_analysis:
        existing_analysis.analysis_result = analysis_result
        existing_analysis.analyzed_at = datetime.utcnow()
    else:
        analysis_record = AnalysisRecord(
            file_id=file_id,
            analysis_result=analysis_result
        )
        db.add(analysis_record)
    
    db.commit()
    
    return {
        "message": "Analysis completed",
        "file_id": file_id,
        "analysis": analysis_result
    }

@router.get("/files/{file_id}/analysis")
def get_analysis(file_id: int, db: Session = Depends(get_db)):
    file_record = db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    analysis = db.query(AnalysisRecord).filter(
        AnalysisRecord.file_id == file_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=404, 
            detail="Analysis not found. Please run analysis first using POST /files/{file_id}/analyze"
        )
    
    return {
        "file_id": file_id,
        "file_name": file_record.original_name,
        "version": file_record.version,
        "analysis": analysis.analysis_result,
        "analyzed_at": analysis.analyzed_at.isoformat()
    }

@router.get("/health")
def health_check():
    return {"status": "healthy"}