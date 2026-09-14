from src.apic_client import (
    get_apic_session,
    login,
    logout,
    get_managed_objects_by_class,
)


def get_objects(class_name: str, object_name: str):
    """Retrieve and display objects of a specific APIC class."""
    session = get_apic_session()
    token = login(session)

    if token:
        #print("[+] Token acquired successfully.")

        data = get_managed_objects_by_class(session, class_name)
        print(f"{object_name}s:")
        for item in data["imdata"]:
            attributes = item[class_name]["attributes"]

            name = attributes.get("name", "")
            dn = attributes.get("dn", "")

            print(f" {name} |   DN: {dn}")

        logout(session)

    else:
        print("[-] Connection failed. Check .env values and network reachability.")


def get_tenants():
    get_objects("fvTenant", "Tenant")


def get_vrfs():
    get_objects("fvCtx", "VRF")


def get_bridge_domains():
    get_objects("fvBD", "Bridge Domain")


def get_application_profiles():
    get_objects("fvAp", "Application Profile")


def get_epgs():
    get_objects("fvAEPg", "EPG")



