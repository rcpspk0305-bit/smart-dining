from fastapi import APIRouter, HTTPException
from app.schemas.otp import OTPSendRequest, OTPVerifyRequest, OTPResponse
from app.services.otp import OTPService

router = APIRouter()


@router.post("/send", response_model=OTPResponse)
def send_otp(payload: OTPSendRequest) -> OTPResponse:
    """
    POST /api/otp/send
    Request an SMS OTP code to verify a customer's phone number.
    In mock mode, the code is always '123456'.
    """
    message = OTPService.send_otp(payload.phone_number)
    return OTPResponse(
        success=True,
        message=message
    )


@router.post("/verify", response_model=OTPResponse)
def verify_otp(payload: OTPVerifyRequest) -> OTPResponse:
    """
    POST /api/otp/verify
    Verify the sent OTP. Returns a signed JWT checkout token on success.
    """
    token = OTPService.verify_otp(payload.phone_number, payload.otp_code)
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Invalid verification code entered. Hint: use 123456"
        )
        
    return OTPResponse(
        success=True,
        message="Phone number verified successfully",
        verification_token=token
    )
