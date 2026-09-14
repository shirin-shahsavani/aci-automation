from fastapi import FastAPI , HTTPException , Request
from pydantic import BaseModel
from enum import Enum
from src import get_info


class Input(BaseModel):
    object:str

app = FastAPI()


class ObjectType(str, Enum):
    tenants = "tenants"
    vrfs = "vrfs"
    bridge_domains = "bridge_domains"
    application_profiles = "application_profiles"
    epgs = "epgs"

@app.post("/info/{object_name}/")
def show_objects(object_name: ObjectType):
    try:
        function_name = f"get_{object_name.value}"
        function = getattr(get_info, function_name, None)
        if function is None:
            raise HTTPException(
                status_code=404,
                detail=f"Function not found: {function_name}",
            )
        result=function()
        return {
            "object": object_name.value,
            "data": result,
        }
    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )


