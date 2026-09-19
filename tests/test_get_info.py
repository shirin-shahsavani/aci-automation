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