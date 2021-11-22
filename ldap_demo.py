import ldap, os


def authenticate(address, username, password):
    conn = ldap.initialize(address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)

    try:
        result = conn.simple_bind_s(username, password)
    except ldap.INVALID_CREDENTIALS:
        return "Invalid credentials"
    except ldap.SERVER_DOWN:
        return "Server down"
    except ldap.LDAPError as e:
        return e
    finally:
            conn.unbind_s()

    return "Succesfully authenticated"

print(authenticate(os.getenv('LDAP_HOST'), os.getenv('LDAP_USERNAME'), os.getenv('LDAP_PASSWORD')))
