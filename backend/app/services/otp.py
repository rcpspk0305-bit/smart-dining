from datetime import timedelta
from typing import Dict, Optional
from app.core.security import create_access_token

# In-memory database mapping phone -> active otp code
MOCK_OTP_STORAGE: Dict[str, str] = {}


class OTPService:
    @staticmethod
    def send_otp(phone_number: str) -> str:
        """
        Sends an SMS OTP. For mock simulation, the code is always set to '123456'.
        """
        MOCK_OTP_STORAGE[phone_number] = "123456"
        return f"Mock verification code dispatched to {phone_number}. Hint: enter 123456"

    @staticmethod
    def verify_otp(phone_number: str, otp_code: str) -> Optional[str]:
        """
        Validate the SMS code. If correct, returns a signed JWT verification token.
        """
        if phone_number in MOCK_OTP_STORAGE and MOCK_OTP_STORAGE[phone_number] == otp_code:
            # Code verified! Generate 30 minute checkout token
            token = create_access_token(subject=phone_number, expires_delta=timedelta(minutes=30))
            del MOCK_OTP_STORAGE[phone_number]
            return token
        return None
