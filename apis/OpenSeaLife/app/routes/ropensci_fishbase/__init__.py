from fastapi import APIRouter

from app.routes.ropensci_fishbase.comnames import router as comnames_router

router = APIRouter(prefix="/ropensci-fishbase", tags=["ropensci-fishbase"])
router.include_router(comnames_router)
