import secrets

class ActivationKey:
    def generate_activation_key(sel) -> str:
        return secrets.token_urlsafe(24)[:32]