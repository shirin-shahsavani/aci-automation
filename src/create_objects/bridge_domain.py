from fastapi import HTTPException
from src.apic_client import (
    get_apic_session,
    login,
    logout,
    get_managed_objects_by_class,
    post_managed_object,
    post_managed_object_with_child
)


def create_bd(
    tenant_name: str,
    bd_name: str,
    vrf_name: str,
):
    session = get_apic_session()
    token = login(session)

    if not token:
        raise ConnectionError(
            "APIC connection failed. Check .env values and network reachability."
        )

    try:
        # Tenant validation
        tenants = get_managed_objects_by_class(session, "fvTenant")

        tenant_exists = False

        for item in tenants["imdata"]:
            attributes = item["fvTenant"]["attributes"]

            if attributes.get("name") == tenant_name:
                tenant_exists = True
                break
        if not tenant_exists:
            raise HTTPException(
                status_code=404,
                detail=f"Tenant '{tenant_name}' does not exist."
            )
        vrfs = get_managed_objects_by_class(session, "fvCtx")

        vrf_exists = False

        for item in vrfs["imdata"]:
            attributes = item["fvCtx"]["attributes"]

            name = attributes.get("name")
            dn = attributes.get("dn", "")

            if (
                name == vrf_name
                and dn == f"uni/tn-{tenant_name}/ctx-{vrf_name}"
            ):
                vrf_exists = True
                break

        if not vrf_exists:
            raise HTTPException(
                status_code=404,
                detail=f"VRF '{vrf_name}' does not exist in tenant '{tenant_name}'."
            )
        bds = get_managed_objects_by_class(session, "fvBD")
        bd_exists = False

        for item in bds["imdata"]:
            attributes = item["fvBD"]["attributes"]

            name = attributes.get("name")
            dn = attributes.get("dn", "")

            if (
                    name == bd_name
                    and dn == f"uni/tn-{tenant_name}/BD-{bd_name}"
            ):
                bd_exists = True
                break
        if bd_exists:
            return {
                "status": "exists",
                "name": bd_name,
                "dn": f"uni/tn-{tenant_name}/BD-{bd_name}",
            }

        result = post_managed_object_with_child(
            session,
            f"uni/tn-{tenant_name}",
            "fvBD",
            {
                "name": bd_name,
            },
            "fvRsCtx",
            {
                "tnFvCtxName": vrf_name,
            },
        )

        return {
                "status": "created",
                "name": bd_name,
                "tenant": tenant_name,
                "vrf": vrf_name,
                "data": result,
        }


    finally:
        logout(session)

