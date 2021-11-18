import os, ldap, sys

keyword = "Peng"

l = ldap.initialize(os.getenv('LDAP_HOST'))

def searchLDAP(l, keyword):
    base = ""
    scope = ldap.SCOPE_SUBTREE

    filter = "cn=" + "*" + keyword + "*"
    retrieve_attr = None
    count = 0
    result_set = []
    timeout = 0

    try:
        result_id = l.search(base, scope, filter, retrieve_attr)

        while l:
            result_type, result_data = l.result(result_id, timeout)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
                    
        if len(result_set) == 0:
            print("No Results.")
            return

        for i in range(len(result_set)):
            for entry in result_set[i]:
                try:
                    name = entry[1]['cn'][0]
                    email = entry[1]['mail'][0]
                    phone = entry[1]['telephonenumber'][0]
                    desc = entry[1]['description'][0]
                    count = count + 1

                    print("{count}.\nName: {name}\nDescription: {desc}\nE-mail: {email}\nPhone: {phone}\n"
                            .format(count, name, desc, email, phone))

                except:
                    print('\nData err.\n')
                    sys.exit()

    except ldap.LDAPError as err:
        print('\nSearching err.\n')
        print(err)
        sys.exit()
try:
    dn = "uid=lenny.peng@senscomm.com,ou=user,ou=Suzhou,ou=corp,dc=senscomm,dc=com"
    l.protocol_version = 3
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.bind_s(dn, os.getenv('LDAP_PASSWORD'))
    searchLDAP(l, keyword)

except ldap.INVALID_CREDENTIALS as e:
    print('\nYour username or password is incorrent.\n')
    print(e)
    sys.exit()

except ldap.LDAPError as e:
    print('\nConnection err.\n')
    print(e, type(e))
    sys.exit()
