from pydantic import BaseModel, field_validator
from datetime import datetime

# --- what the frontend sends to POST /gst/analyze ---
class GstAnalyzeRequest(BaseModel):
    gstin: list[str]        # list of GST numbers e.g. ["29AGDPB9439B1ZD"]
    
    from_date: str          # e.g. "022025" (mmyyyy)
    to_date: str            # e.g. "012026"
    account_id: str         # which customer is making this request

    @field_validator("from_date", "to_date")
    @classmethod
    def validate_date_format(cls, value):
        # must be exactly 6 characters
        if len(value) != 6:
            raise ValueError("Date must be in mmyyyy format e.g. 022025")
        
        month = int(value[:2])   # first 2 chars = month
        year = int(value[2:])    # last 4 chars = year

        # month must be 01-12
        if month < 1 or month > 12:
            raise ValueError("Month must be between 01 and 12")

        # year must be reasonable
        if year < 2000 or year > 2100:
            raise ValueError("Year seems invalid")

        return value

    @field_validator("to_date")
    @classmethod
    def validate_date_range(cls, to_date, values):
        from_date = values.data.get("from_date")
        if not from_date:
            return to_date

        # convert mmyyyy to actual dates for comparison
        from_dt = datetime(int(from_date[2:]), int(from_date[:2]), 1)
        to_dt = datetime(int(to_date[2:]), int(to_date[:2]), 1)

        if to_dt < from_dt:
            raise ValueError("to_date cannot be before from_date")

        return to_date

# --- what we send back to frontend after calling ScoreMe ---
class GstAnalyzeResponse(BaseModel):
    reference_id: str
    status: str
    message: str



# what ScoreMe sends to our webhook
class ScoreMeWebhookPayload(BaseModel):
    referenceId: str        # ScoreMe uses camelCase
    fileUrl: str
    responseCode: str
    responseMessage: str

