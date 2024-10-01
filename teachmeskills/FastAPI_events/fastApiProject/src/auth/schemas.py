from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    """
    Base schema for user data.
    Contains required fields username and email.
    """

    username: str = Field(..., min_length=2, max_length=50)

    email: EmailStr = Field(..., max_length=256)


class UserSchema(UserBaseSchema):
    """
    Schema for representing an existing user.
    Inherits fields from UserBaseSchema and adds the id field.
    """

    # User's ID, type int
    id: int

    # Enable model configuration to load from attributes
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    """
    Schema for creating a new user.
    Inherits fields from UserBaseSchema and adds the password field.
    """

    password: str = Field(..., min_length=8, max_length=50)
    # Flag indicating if the user is an admin
    is_admin: bool


class UserCredentialsSchema(BaseModel):
    """
    Schema for user credentials (username and password).
    """

    username: str

    password: str


class AdminCreateSchema(UserCreateSchema):
    """
    Schema for creating an admin user.
    Inherits fields from UserCreateSchema and adds the is_admin field.
    """

    # Flag indicating if the user is an admin
    is_admin: bool


class AccessTokenSchema(BaseModel):
    """
    Schema for access token.
    """

    access_token: str


class RefreshTokenSchema(BaseModel):
    """
    Schema for refresh token.
    """

    refresh_token: str


class TokenPairSchema(AccessTokenSchema, RefreshTokenSchema):
    """
    Schema for a pair of tokens (access and refresh).
    Inherits fields from AccessTokenSchema and RefreshTokenSchema.
    """

    pass
