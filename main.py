from fastapi import FastAPI , HTTPException , Request
from pydantic import BaseModel
from enum import Enum
from src import get_info
from src.create_objects import tenant,vrf


class Input(BaseModel):
    object:str

app = FastAPI()


class ObjectType(str, Enum):
    tenants = "tenants"
    vrfs = "vrfs"
    bridge_domains = "bridge_domains"
    application_profiles = "application_profiles"
    epgs = "epgs"

class TenantInput(BaseModel):
    tenant_name: str

class VRFInput(BaseModel):
    tenant_name: str
    vrf_name: str


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

@app.post("/create/{tenant_name}/")
def create_tenant_api(detail: TenantInput):
    try:
        result = tenant.create_tenant(detail.tenant_name)
        return result

    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )


@app.post("/create/{tenant_name}/{vrf_name}")
def create_vrf_api(detail:VRFInput):
    try:
        result = vrf.create_vrf(detail.tenant_name, detail.vrf_name)
        return result

    except ConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )