from src.apic_client import get_apic_session, login, logout


def main():
    session = get_apic_session()
    token = login(session)

    if token:
        print("[+] Token acquired successfully.")
        logout(session)
    else:
        print("[-] Connection failed. Check .env values and network reachability.")


if __name__ == "__main__":
    main()