from fastapi import HTTPException

from src.apic_client import (
    get_apic_session,
    login,
    logout,
    get_managed_objects_by_class,
    post_managed_object,
)


def create_vrf(tenant_name: str, vrf_name: str):
    session = get_apic_session()
    token = login(session)

    if not token:
        raise ConnectionError(
            "APIC connection failed. Check .env values and network reachability."
        )

    try:
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

        for item in vrfs["imdata"]:
            attributes = item["fvCtx"]["attributes"]

            name = attributes.get("name")
            dn = attributes.get("dn", "")

            # Check that this VRF belongs to the requested tenant
            if name == vrf_name and dn == f"uni/tn-{tenant_name}/ctx-{vrf_name}":
                return {
                    "status": "exists",
                    "name": vrf_name,
                    "dn": dn,
                }

        result = post_managed_object(
            session,
            f"uni/tn-{tenant_name}",
            "fvCtx",
            {
            "name": vrf_name,
            },
        )

        return {
            "status": "created",
            "name": vrf_name,
            "tenant": tenant_name,
            "data": result,
        }

    finally:
        logout(session)
