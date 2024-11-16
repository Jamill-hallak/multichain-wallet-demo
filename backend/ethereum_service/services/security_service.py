import pyotp

class SecurityService:
    def __init__(self):
        self.otp_secrets = {}

    def generate_otp(self, user_id):
        if not user_id:
            raise ValueError("User ID is required to generate OTP.")
        secret = pyotp.random_base32()
        self.otp_secrets[user_id] = secret
        totp = pyotp.TOTP(secret)
        print(f"Generated OTP for user {user_id}: {totp.now()} (Secret: {secret})")  # Debugging line
        return totp.now()

    def verify_otp(self, user_id, otp):
        if user_id not in self.otp_secrets:
            raise ValueError("No OTP found for this user.")
        secret = self.otp_secrets[user_id]
        totp = pyotp.TOTP(secret)
        print(f"Verifying OTP for user {user_id} with OTP: {otp} and Secret: {secret}")  # Debugging line
        return totp.verify(otp)
