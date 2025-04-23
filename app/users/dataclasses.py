from gotrue import OAuthResponse
from profiles.dataclasses import Profile
from pydantic import BaseModel, EmailStr
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


class MyProfileResponse(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_tutor: bool


class FeaturedReview(BaseModel):
    id: int
    rating: Optional[float] = None
    comment: str
    student_id: str


class MyTutorProfileResponse(BaseModel):
    bio: Optional[str] = None
    bio_long: Optional[str] = None
    rating: Optional[float] = None
    contact_email: Optional[str] = None
    phone_number: Optional[str] = None
    featured_review: Optional[FeaturedReview] = None


class MyUserResponse(BaseModel):
    id: str
    provider_email: str
    provider_display_name: str
    profile: Optional[MyProfileResponse] = None
    tutor_profile: Optional[MyTutorProfileResponse] = None


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


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    avatar_url: Optional[str] = None
