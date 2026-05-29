from pydantic import BaseModel, Field
from typing import Optional


class OTPSendRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$", examples=["+15555550199"])


class OTPVerifyRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$", examples=["+15555550199"])
    otp_code: str = Field(..., min_length=4, max_length=6, examples=["1234"])


class OTPResponse(BaseModel):
    success: bool
    message: str
    verification_token: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "OTP verified successfully",
                "verification_token": "token_xyz789"
            }
        }
