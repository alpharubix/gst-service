from datetime import datetime, timezone
import uuid
from fastapi import HTTPException
from src.models.gst_reference import GstReference
from src.logger import get_logger


logger = get_logger(__name__)

async def analyze_gst(account_id: str, gstin: list[str], from_date: str, to_date: str):
    logger.info(f"New GST request | account_id: {account_id} | gstin: {gstin}")
    
    # Step 1 — generating a fake reference_id for now
    # later this will be replaced by the real ScoreMe API call
    fake_reference_id = str(uuid.uuid4())

    # Step 2 — save to MongoDB with status SUBMITTED
    gst_record = GstReference(
        reference_id=fake_reference_id,
        account_id=account_id,
        status="SUBMITTED",
        request_initiated_time=datetime.now(timezone.utc),
        initial_request_response_code=200,
        initial_request_response={"message": "mock response - ScoreMe not connected yet"}
    )
    await gst_record.insert()
    logger.info(f"Saved to DB | reference_id: {fake_reference_id}")

    # Step 3 — return the reference_id to the frontend
    return {
        "reference_id": fake_reference_id,
        "status": "SUBMITTED",
        "message": "Request submitted successfully"
    }


async def handle_webhook(payload: dict):
    logger.info(f"Webhook received | referenceId: {payload['referenceId']}")

    # Step 1 — find the document in MongoDB using reference_id
    record = await GstReference.find_one(
        GstReference.reference_id == payload["referenceId"]
    )

    # Step 2 — if not found, something is wrong
    if not record:
        logger.warning(f"referenceId not found: {payload['referenceId']}")
        raise HTTPException(status_code=404, detail="reference_id not found")
    
    # Step 3 — already completed, ignore duplicate webhook
    if record.status == "COMPLETED":
        logger.warning(f"Duplicate webhook ignored | referenceId: {payload['referenceId']}")
        return {"message": "Already processed, ignoring duplicate"}

    # Step 4 — update the document with webhook data
    record.status = "COMPLETED"
    record.file_url = payload["fileUrl"]
    record.webhook_response_code = 200
    record.webhook_response_receive_time = datetime.now(timezone.utc)
    record.webhook_response = payload
    await record.save()

    logger.info(f"Status updated to COMPLETED | referenceId: {payload['referenceId']}")
    return {"message": "Webhook received and saved successfully"}