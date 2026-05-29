from datetime import timedelta
from fastapi import APIRouter, HTTPException
from app.schemas.otp import OTPRequest, OTPVerify, OTPResponse
from app.core.security import create_access_token

router = APIRouter()

# Simple mock database mapping phone -> active otp code
MOCK_OTP_DB = {}

@router.post("/request", response_model=OTPResponse)
def request_otp(payload: OTPRequest) -> OTPResponse:
    """
    Initiate an OTP request. In mock mode, a preset code of '1234' is mapped to the phone number.
    """
    phone = payload.phone_number
    # Simulate sending SMS
    MOCK_OTP_DB[phone] = "1234"
    
    return OTPResponse(
        success=True,
        message=f"Mock SMS sent to {phone}. Code is 1234."
    )


@router.post("/verify", response_model=OTPResponse)
def verify_otp(payload: OTPVerify) -> OTPResponse:
    """
    Verify the sent OTP. If matching, returns a signed verification JWT token
    granting authority to place orders.
    """
    phone = payload.phone_number
    code = payload.otp_code

    if phone not in MOCK_OTP_DB:
        raise HTTPException(status_code=400, detail="No active OTP request found for this phone number")

    if MOCK_OTP_DB[phone] == code:
        # OTP is correct! Generate a JWT session token valid for 30 minutes
        token = create_access_token(subject=phone, expires_delta=timedelta(minutes=30))
        # Clear code from memory
        del MOCK_OTP_DB[phone]
        
        return OTPResponse(
            success=True,
            message="OTP verified successfully",
            verification_token=token
        )
    
    raise HTTPException(status_code=401, detail="Invalid OTP code entered. Hint: enter 1234")
