from geoip2.database import Reader


class UserIpUtility:

    @staticmethod
    def get_client_ip(request):
        real_ip = request.META.get("X-Forwarded-For")
        if real_ip:
            ip = real_ip.split(",")[
                0
            ]  # In case there are multiple IPs, take the first one.
        else:
            ip = request.META.get(
                "REMOTE_ADDR"
            )  # Directly connected, not through a proxy.
        return ip

    @staticmethod
    def get_country_code_from_ip(ip):
        with Reader("ip_country.mmdb") as reader:
            try:
                return reader.country(ip).country.iso_code
            except Exception as e:
                print(e)
                return ""

    @classmethod
    def get_country_from_request(cls, request):
        ip = cls.get_client_ip(request)
        return cls.get_country_code_from_ip(ip)
