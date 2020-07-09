import easypost
from easypost import Address

easypost.api_key = "EZTK6acab147147b466d9f28b4b65e1b8191Q1a3j4lvc4HbVNU100jp8g"


def get_address(i_name, i_street, i_city, i_state, i_zip, i_country,
                i_company=''):
    # add: check if address is valid
    addr = easypost.Address.create(street1=i_street, name=i_name,
                                   city=i_city, state=i_state, zip=i_zip,
                                   country=i_country, verify=["delivery"])
    if not addr.verifications["delivery"]["success"]:
        return False
    return addr


def create_parcel(length, width, height, weight):
    parcel = easypost.Parcel.create(length=length, width=width,
                                    height=height, weight=weight)
    return parcel


def create_flat_rate_parcel(predef, weight):
    parcel = easypost.Parcel.create(predefined_package=predef,
                                    weight=weight)
    return parcel


def create_shipment(parcel, to_addr, sender_addr):
    shipment = easypost.Shipment.create(parcelObj=parcel,
                                        to_address=to_addr,
                                        from_address=sender_addr)
    return shipment
#will print shipping rates of carriers

def shippingRates(to_address,fromAddress,parcel):
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=fromAddress,
        parcel=parcel)

    for rate in shipment.rates:
        print(rate.carrier)
        print(rate.service)
        print(rate.rate)
        print(rate.id)
    return rate


# list all availabe carrier/ and user selects one favorable carrier.

def selectionOfCarrier():
    
    #will return value of readable, which is the name of the carrier
    
    carriers = easypost.CarrierAccount.get('readable')

    # print list of carriers' names

    print(carriers)
    
  #allows a user to select a carrier

    
    while True:
        readable=input()
        if readable in easypost.CarrierAccount.keys():
            print("You selected: "+ easypost.CarrierAccount.value())
        else:
            print('invalid choice')
    
    
