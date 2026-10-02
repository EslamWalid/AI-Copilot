from typing import Literal
from pydantic import BaseModel


class RouterState(BaseModel):
    route: Literal["google_form", "assessment_agent", "other"]