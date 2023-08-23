from pydantic import BaseModel


class CreateStage_user(BaseModel):
    stage_id: int
    connected_user_id: int


class UpdateStage_user(BaseModel):
    id: int
    stage_id: int
    connected_user_id: int


