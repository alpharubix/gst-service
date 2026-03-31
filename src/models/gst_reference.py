from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class GstReference(Document):
    reference_id: str                          # ScoreMe's tracking ID
    account_id: str                            # which customer made this request
    status: str = "INITIATED"                 # INITIATED → SUBMITTED → COMPLETED / FAILED
    
    # --- initial request fields ---
    request_initiated_time: Optional[datetime] = None
    request_end_time: Optional[datetime]  = None
    initial_request_response_code: Optional[int] = None
    initial_request_response: Optional[dict] = None

    # --- webhook fields (filled later by ScoreMe) ---
    webhook_response_code: Optional[int] = None
    webhook_response_receive_time: Optional[datetime] = None
    webhook_response: Optional[dict] = None
    file_url: Optional[str] = None            # the ZIP/PDF download link

    class Settings:
        name = "gst_webhook_reciever"          # exact collection name in MongoDB