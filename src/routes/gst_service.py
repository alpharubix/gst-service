from fastapi import APIRouter
from src.schemas.gst_service import GstAnalyzeRequest, GstAnalyzeResponse,ScoreMeWebhookPayload
from src.controllers.gst_service import analyze_gst, handle_webhook

router = APIRouter(prefix="/gst", tags=["GST"])

@router.post("/analyze", response_model=GstAnalyzeResponse)
async def gst_analyze(request: GstAnalyzeRequest):
    result = await analyze_gst(
        account_id=request.account_id,
        gstin=request.gstin,
        from_date=request.from_date,
        to_date=request.to_date
    )
    return result

@router.post("/webhook")
async def gst_webhook(payload: ScoreMeWebhookPayload):
    result = await handle_webhook(payload.model_dump(by_alias=True))
    return result


