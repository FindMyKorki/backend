from pydantic import BaseModel
from profiles.dataclasses import Profile
from gotrue import OAuthResponse


class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True

class CodeForSessionResponse(BaseModel):
    tokens: TokensResponse
    profile: Profile | None

    class Config:
        from_attributes = True

class RefreshTokensRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True

class SignInResponse(BaseModel):
    code_verifier: str
    oauth_repsponse: OAuthResponse

    class Config:
        from_attributes = True

class CallbackResponse(BaseModel):
    code: str

    class Config:
        from_attributes = True
