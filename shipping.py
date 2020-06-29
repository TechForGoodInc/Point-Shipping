import easypost
from easypost import Address

easypost.api_key = "EZTK6acab147147b466d9f28b4b65e1b8191Q1a3j4lvc4HbVNU100jp8g"


def get_address(i_name, i_street, i_city, i_state, i_zip, i_country,
                i_company=''):
    # add: check if address is valid
    addr = easypost.Address.create(street=i_street, name=i_name,
                                   city=i_city, state=i_state, zip=i_zip,
                                   country=i_country, company=i_company)
    return addr


