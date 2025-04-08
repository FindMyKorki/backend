from pydantic import BaseModel, EmailStr
from profiles.dataclasses import Profile
from gotrue import OAuthResponse
from typing import Optional

class TokensResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class CodeForSessionResponse(BaseModel):
    tokens: TokensResponse
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True


class RefreshTokensRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True


class SignInResponse(BaseModel):
    code_verifier: str
    oauth_response: OAuthResponse

    class Config:
        from_attributes = True


class CallbackResponse(BaseModel):
    code: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None
    is_tutor: Optional[bool] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True