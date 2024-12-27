from uuid import UUID
from pydantic import BaseModel


class FollowSchema(BaseModel):
    follower_id:UUID
    following_id:UUID
