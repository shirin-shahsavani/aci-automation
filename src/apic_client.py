import os
import requests
import urllib3
from dotenv import load_dotenv

load_dotenv()

APIC_HOST = os.getenv("APIC_HOST")
APIC_USER = os.getenv("APIC_USER")
APIC_PASSWORD = os.getenv("APIC_PASSWORD")
APIC_VERIFY_SSL = os.getenv("APIC_VERIFY_SSL", "false").lower() == "true"

if not APIC_VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_apic_session() -> requests.Session:
    """Create and return a configured requests session."""
    session = requests.Session()
    session.verify = APIC_VERIFY_SSL
    return session


def login(session: requests.Session) -> str | None:
    """Authenticate with APIC and store the auth token in session headers."""
    url = f"https://{APIC_HOST}/api/aaaLogin.json"
    payload = {
        "aaaUser": {
            "attributes": {
                "name": APIC_USER,
                "pwd": APIC_PASSWORD
            }
        }
    }

    try:
        response = session.post(url, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        token = data["imdata"][0]["aaaLogin"]["attributes"]["token"]

        # APIC accepts the token via APIC-Challenge header or cookie
        session.headers.update({"APIC-Challenge": token})
        return token

    except requests.exceptions.RequestException as exc:
        return None


def logout(session: requests.Session) -> None:
    """Terminate the active session on APIC."""
    url = f"https://{APIC_HOST}/api/aaaLogout.json"
    payload = {
        "aaaUser": {
            "attributes": {
                "name": APIC_USER
            }
        }
    }

    try:
        session.post(url, json=payload, timeout=5)
        #print("[+] Session successfully terminated.")
    except requests.exceptions.RequestException as exc:
        print(f"[-] Logout warning: {exc}")
    finally:
        session.close()

def get_managed_object(
    session: requests.Session,
    dn: str
) -> dict:
    """Retrieve a managed object from APIC by its distinguished name."""
    url = f"https://{APIC_HOST}/api/mo/{dn}.json"

    response = session.get(url, timeout=10)
    response.raise_for_status()

    return response.json()

def get_managed_objects_by_class(
    session: requests.Session,
    class_name: str
) -> dict:
    """Retrieve all managed objects of a given class from APIC."""
    url = f"https://{APIC_HOST}/api/class/{class_name}.json"

    response = session.get(url, timeout=10)
    response.raise_for_status()

    return response.json()