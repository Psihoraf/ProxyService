import secrets

class KeyGenerator:
    def generate_activation_key(sel) -> str:
        return secrets.token_urlsafe(24)[:32]

key_generator = KeyGenerator()