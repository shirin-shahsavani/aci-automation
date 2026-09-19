import src.get_info as get_info

def test_get_tenants(mocker):
    mocker.patch(
        "src.get_info.get_apic_session",
        return_value="fake_session"
    )

    mocker.patch(
        "src.get_info.login",
        return_value="fake_token"
    )

    mocker.patch(
        "src.get_info.get_managed_objects_by_class",
        return_value={
            "imdata": [
                {
                    "fvTenant": {
                        "attributes": {
                            "name": "tenant-test",
                            "dn": "uni/tn-tenant-test"
                        }
                    }
                }
            ]
        }
    )

    mocker.patch("src.get_info.logout")

    result = get_info.get_tenants()

    assert result == [
        " tenant-test |   DN: uni/tn-tenant-test"
    ]


def test_get_vrfs(mocker):
    mocker.patch(
        "src.get_info.get_apic_session",
        return_value="fake_session"
    )

    mocker.patch(
        "src.get_info.login",
        return_value="fake_token"
    )

    mocker.patch(
        "src.get_info.get_managed_objects_by_class",
        return_value={
            "imdata": [
                {
                    "fvCtx": {
                        "attributes": {
                            "name": "vrf-test",
                            "dn": "uni/tn-tenant-test/ctx-vrf-test"
                        }
                    }
                }
            ]
        }
    )

    mocker.patch("src.get_info.logout")

    result = get_info.get_vrfs()

    assert result == [
        " vrf-test |   DN: uni/tn-tenant-test/ctx-vrf-test"
    ]


def test_get_bridge_domains(mocker):
    mocker.patch(
        "src.get_info.get_apic_session",
        return_value="fake_session"
    )

    mocker.patch(
        "src.get_info.login",
        return_value="fake_token"
    )

    mocker.patch(
        "src.get_info.get_managed_objects_by_class",
        return_value={
            "imdata": [
                {
                    "fvBD": {
                        "attributes": {
                            "name": "bd-test",
                            "dn": "uni/tn-tenant-test/BD-bd-test"
                        }
                    }
                }
            ]
        }
    )

    mocker.patch("src.get_info.logout")

    result = get_info.get_bridge_domains()

    assert result == [
        " bd-test |   DN: uni/tn-tenant-test/BD-bd-test"
    ]


def test_get_application_profiles(mocker):
    mocker.patch(
        "src.get_info.get_apic_session",
        return_value="fake_session"
    )

    mocker.patch(
        "src.get_info.login",
        return_value="fake_token"
    )

    mocker.patch(
        "src.get_info.get_managed_objects_by_class",
        return_value={
            "imdata": [
                {
                    "fvAp": {
                        "attributes": {
                            "name": "app-test",
                            "dn": "uni/tn-tenant-test/ap-app-test"
                        }
                    }
                }
            ]
        }
    )

    mocker.patch("src.get_info.logout")

    result = get_info.get_application_profiles()

    assert result == [
        " app-test |   DN: uni/tn-tenant-test/ap-app-test"
    ]


def test_get_epgs(mocker):
    mocker.patch(
        "src.get_info.get_apic_session",
        return_value="fake_session"
    )

    mocker.patch(
        "src.get_info.login",
        return_value="fake_token"
    )

    mocker.patch(
        "src.get_info.get_managed_objects_by_class",
        return_value={
            "imdata": [
                {
                    "fvAEPg": {
                        "attributes": {
                            "name": "epg-test",
                            "dn": "uni/tn-tenant-test/ap-app-test/epg-epg-test"
                        }
                    }
                }
            ]
        }
    )

    mocker.patch("src.get_info.logout")

    result = get_info.get_epgs()

    assert result == [
        " epg-test |   DN: uni/tn-tenant-test/ap-app-test/epg-epg-test"
    ]