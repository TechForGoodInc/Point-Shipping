import easypost
import json
#from modules import interface as inter

easypost.api_key = 'EZTK9374380ba203453bba337fb902362c35KLlDx9ThFtAW7n0jbDPtzQ'


# Takes in aspects of a package and returns rate options
# in the form of a dictionary containing the carriers and
# their corresponding prices
# length: inches, weight: ounces
def select_rate(origin_add1, origin_add2, origin_city, origin_state,
                origin_country, origin_zip, origin_phone, dest_add1, dest_add2,
                dest_city, dest_state, dest_country, dest_zip, dest_phone,
                weight, height, width, length):
    
    fromAddress = easypost.Address.create(verify=["delivery"],
                                          street1=origin_add1,
                                          street2=origin_add2,
                                          city=origin_city,
                                          state=origin_state,
                                          zip=origin_zip,
                                          country=origin_country,
                                          phone=origin_phone,
                                          residential=True)
    toAddress = easypost.Address.create(verify=["delivery"],
                                        street1=dest_add1,
                                        street2=dest_add2,
                                        city=dest_city,
                                        state=dest_state,
                                        zip=dest_zip,
                                        country=dest_country,
                                        phone=dest_phone,
                                        residential=True)
    parcel = easypost.Parcel.create(length=length, width=width, height=height,
                                    weight=weight)
    shipment = easypost.Shipment.create(to_address=toAddress,
                                        from_address=fromAddress,
                                        parcel=parcel)
    return shipment


resp = select_rate('8008 18th Ave NE', '', 'Seattle', 'WA',
                   'US', 98115, '206-491-3335', '1115 8th Ave', 'Box #4020',
                   'Grinnell', 'IA', 'US', '50112', '206-491-3335',
                   12, 3, 3, 6)
print(resp)


def get_package():
    parcel = easypost.Parcel.retrieve("prcl_...")
