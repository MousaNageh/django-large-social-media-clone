from user.models import OTP
from random import randint


class OTPQuerySet:

    @classmethod
    def create_or_replace_otp(cls, user_id):
        code = cls.generate_code()
        opt, created = OTP.objects.update_or_create(
            user_id=user_id, defaults={"code": code}
        )
        return opt

    @staticmethod
    def is_code_expired(otp_instance=None, user_id=None):
        if otp_instance:
            return OTP.is_expired
        if user_id:
            return OTP.objects.get(user_id=user_id).is_expired
        if not otp_instance and not user_id:
            raise Exception(
                "otp_instance or user_id are required (at least one of them)"
            )

    @staticmethod
    def is_code_is_invalid_or_expired(user_id, code):
        invalid = False
        expired = False
        try:
            opt = OTP.objects.get(user_id=user_id, code=code)
            expired = opt.is_expired
        except OTP.DoesNotExist:
            invalid = True
        return invalid, expired

    @staticmethod
    def generate_code(code_len=6):
        range_start = 10 ** (code_len - 1)
        range_end = (10**code_len) - 1
        return randint(range_start, range_end)
