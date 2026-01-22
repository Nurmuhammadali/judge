from pydantic import BaseModel


class ProblemCreate(BaseModel):
    id: int
    title: str
    description: str

    input_description: str
    output_description: str

    time_limit_sec: int
    memory_limit_mb: int

    class Config:
        from_attributes = True

class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str
    input_description: str
    output_description: str
    time_limit_sec: int
    memory_limit_mb: int
    class Config:
        orm_mode = True