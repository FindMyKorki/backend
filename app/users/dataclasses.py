from pydantic import BaseModel
from profiles.dataclasses import Profile


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True

class AuthCallbackResponse(BaseModel):
    tokens: TokensResponse
    profile: Profile | None

    class Config:
        from_attributes = True

class RefreshTokensRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True
