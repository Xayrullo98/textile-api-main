from pydantic import BaseModel


class CreateStage_user(BaseModel):
    stage_id: int
    crated_user_id: int


class UpdateStage_user(BaseModel):
    id: int
    stage_id: int
    user_id: int


