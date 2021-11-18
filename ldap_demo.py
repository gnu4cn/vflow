import ldap, os


def authenticate(address, username, password):
    conn = ldap.initialize(address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)

    try:
        dn = "cn={0},ou=user,ou=Suzhou,ou=corp,dc=senscomm,dc=com".format(username)
        result = conn.simple_bind_s(dn, password)
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
