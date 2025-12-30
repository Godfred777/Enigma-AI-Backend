from fastapi import APIRouter, Depends
from app.services.vector_store import VectorService
from app.schemas.research import ResearchRequest

router = APIRouter()

@router.post("/save_finding")
async def save_finding(
    request: ResearchRequest, 
    vector_service: VectorService = Depends()
):
    """
    Called by the Researcher Agent when it finds a good paper.
    """
    result = await vector_service.save_citation(
        project_id=str(request.project_id),
        title=request.title,
        abstract=request.abstract,
        url=request.url
    )
    return {"status": "saved", "id": result[0]['id']}