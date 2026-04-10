from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from .. import crud, schemas
from ..core.security import get_current_admin

router = APIRouter()

# Subject endpoints
@router.post("/subjects", response_model=dict)
def create_subject(subject: schemas.SubjectCreate, current_user: dict = Depends(get_current_admin)):
    """Create a new subject (admin only)"""
    existing = crud.get_subject_by_code(subject.code)
    if existing:
        raise HTTPException(status_code=400, detail="Subject code already exists")
    return crud.create_subject(subject.model_dump())

@router.get("/subjects", response_model=list[dict])
def get_subjects():
    """Get all subjects"""
    return crud.get_all_subjects()

@router.get("/subjects/{subject_id}", response_model=dict)
def get_subject(subject_id: str):
    """Get subject by ID"""
    try:
        subject = crud.get_subject(ObjectId(subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: str, current_user: dict = Depends(get_current_admin)):
    """Delete a subject (admin only)"""
    try:
        subject = crud.get_subject(ObjectId(subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    crud.delete_subject(ObjectId(subject_id))
    return {"message": "Subject deleted successfully"}

@router.put("/subjects/{subject_id}", response_model=dict)
def update_subject(subject_id: str, subject: schemas.SubjectCreate, current_user: dict = Depends(get_current_admin)):
    """Update a subject (admin only)"""
    try:
        existing = crud.get_subject(ObjectId(subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not existing:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.update_subject(ObjectId(subject_id), subject.model_dump())

# Class endpoints
@router.post("/classes", response_model=dict)
def create_class(class_: schemas.ClassCreate, current_user: dict = Depends(get_current_admin)):
    """Create a new class (admin only)"""
    try:
        subject = crud.get_subject(ObjectId(class_.subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.create_class(class_.model_dump())

@router.get("/classes", response_model=list[dict])
def get_classes():
    """Get all classes"""
    return crud.get_all_classes()

@router.get("/classes/{class_id}", response_model=dict)
def get_class(class_id: str):
    """Get class by ID"""
    try:
        class_ = crud.get_class(ObjectId(class_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid class ID")
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@router.get("/subjects/{subject_id}/classes", response_model=list[dict])
def get_classes_by_subject(subject_id: str):
    """Get all classes for a subject"""
    try:
        subject = crud.get_subject(ObjectId(subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.get_classes_by_subject(ObjectId(subject_id))

@router.delete("/classes/{class_id}")
def delete_class(class_id: str, current_user: dict = Depends(get_current_admin)):
    """Delete a class (admin only)"""
    try:
        class_ = crud.get_class(ObjectId(class_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid class ID")
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    crud.delete_class(ObjectId(class_id))
    return {"message": "Class deleted successfully"}

@router.put("/classes/{class_id}", response_model=dict)
def update_class(class_id: str, class_: schemas.ClassCreate, current_user: dict = Depends(get_current_admin)):
    """Update a class (admin only)"""
    try:
        existing = crud.get_class(ObjectId(class_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid class ID")
    if not existing:
        raise HTTPException(status_code=404, detail="Class not found")
    try:
        subject = crud.get_subject(ObjectId(class_.subject_id))
    except:
        raise HTTPException(status_code=400, detail="Invalid subject ID")
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return crud.update_class(ObjectId(class_id), class_.model_dump())
