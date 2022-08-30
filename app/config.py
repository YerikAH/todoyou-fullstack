import secrets
secretKey = secrets.token_hex(20)
class Config:
  SECRET_KEY = secretKey
  WTF_CSRF_ENABLED= False
  PRESERVE_CONTEXT_ON_EXCEPTION = False