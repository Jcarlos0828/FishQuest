from fastapi import APIRouter

from app.routes.ropensci_fishbase.comnames import router as comnames_router
from app.routes.ropensci_fishbase.countref import router as countref_router

router = APIRouter(prefix="/ropensci-fishbase", tags=["ropensci-fishbase"])
router.include_router(comnames_router)
router.include_router(countref_router)
