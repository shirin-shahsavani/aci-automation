from src.apic_client import (
    get_apic_session,
    login,
    logout,
    get_managed_objects_by_class,
)


def get_objects(class_name: str, object_name: str):
    """Retrieve and display objects of a specific APIC class."""
    global object_list
    session = get_apic_session()
    token = login(session)

    if token:
        data = get_managed_objects_by_class(session, class_name)
        object_list=[]
        for item in data["imdata"]:
            attributes = item[class_name]["attributes"]

            name = attributes.get("name", "")
            dn = attributes.get("dn", "")

            object = f" {name} |   DN: {dn}"
            object_list.append(object)

        logout(session)
        return object_list


    else:
        raise ConnectionError(
            "APIC connection failed. Check .env values and network reachability."
        )


def get_tenants():
    return get_objects("fvTenant", "Tenant")


def get_vrfs():
    return get_objects("fvCtx", "VRF")


def get_bridge_domains():
    return get_objects("fvBD", "Bridge Domain")


def get_application_profiles():
    return get_objects("fvAp", "Application Profile")


def get_epgs():
    return get_objects("fvAEPg", "EPG")



