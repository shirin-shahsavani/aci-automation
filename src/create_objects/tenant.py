from src.apic_client import (
    get_apic_session,
    login,
    logout,
    get_managed_objects_by_class,
    post_managed_object,
)


def create_tenant(tenant_name: str):
    session = get_apic_session()
    token = login(session)

    if not token:
        raise ConnectionError(
            "APIC connection failed. Check .env values and network reachability."
        )

    try:
        data = get_managed_objects_by_class(session, "fvTenant")

        for item in data["imdata"]:
            attributes = item["fvTenant"]["attributes"]

            if attributes.get("name") == tenant_name:
                return {
                    "status": "exists",
                    "name": tenant_name,
                    "dn": attributes.get("dn"),
                }

        result = post_managed_object(
            session,
            "fvTenant",
            {"name": tenant_name}
        )

        return {
            "status": "created",
            "name": tenant_name,
            "data": result,
        }

    finally:
        logout(session)

# if __name__ == "__main__":
#     result = create_tenant("tenant--me")
#     print(result)


