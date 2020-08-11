import easypost
import json
import interface as inter

easypost.api_key = 'EZAK9374380ba203453bba337fb902362c35cB0jw6UajWMU1eb0vMEsxw'

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
    rates_list = []
    for val in shipment["rates"]:
        item_aspects = []
        keys = ["carrier", "carrier_account_id", "delivery_date",
                "delivery_date_guaranteed", "delivery_days", "id",
                "list_rate", "shipment_id"]
        values = [val.carrier, val.carrier_account_id, val.delivery_date,
                  val.delivery_date_guaranteed, val.delivery_days,
                  val.id, val.list_rate, val.shipment_id]
        item_dict = dict(zip(keys, values))
        rates_list.append(item_dict)
    return rates_list


def buy_label(shipping_id, rate_id):
    shipment = easypost.Shipment.retrieve(shipping_id)
    rates = shipment.rates
    for rate in rates:
        if rate_id == rate.id:
            selected_rate = rate
    print(type(selected_rate))
    resp = shipment.buy(rate=selected_rate)
    return resp


def get_ship_dict(shipment):
    ship_dict = {}
    toAddress = shipment.to_address
    ship_dict["to_name"] = toAddress.name
    ship_dict["to_street1"] = toAddress.street1
    ship_dict["to_street2"] = toAddress.street2
    ship_dict["to_city"] = toAddress.city
    ship_dict["to_state"] = toAddress.state
    ship_dict["to_zip"] = toAddress.zip
    ship_dict["to_country"] = toAddress.country
    ship_dict["to_phone"] = toAddress.phone
    ship_dict["to_email"] = toAddress.email
    fromAddress = shipment.from_address
    ship_dict["from_name"] = fromAddress.name
    ship_dict["from_street1"] = fromAddress.street1
    ship_dict["from_street2"] = fromAddress.street2
    ship_dict["from_city"] = fromAddress.city
    ship_dict["from_state"] = fromAddress.state
    ship_dict["from_zip"] = fromAddress.zip
    ship_dict["from_country"] = fromAddress.country
    ship_dict["from_phone"] = fromAddress.phone
    ship_dict["from_email"] = fromAddress.email
    parcel = shipment.parcel
    ship_dict["length"] = parcel.length
    ship_dict["width"] = parcel.width
    ship_dict["height"] = parcel.height
    ship_dict["weight"] = parcel.weight
    rates = shipment.rates
    rate_list = []
    for rate in rates:
        rate_dict = {}
        rate_dict["price"] = rate.rate
        rate_dict["carrier"] = rate.carrier_account_id
        rate_dict["delivery_days"] = rate.delivery_days
        rate_list.append(rate_dict)
    ship_dict["rates"] = rate_list
    return ship_dict


def get_package(user_id):
    query = f"SELECT \'shipid\' FROM labels WHERE \"userid\" = {user_id}"
    packages = inter.execute_read_query(query)
    print(packages)
    resp = []
    for package in packages:
        shipment = easypost.Shipment.retrieve(package[0])
        ship_dict = get_ship_dict(shipment)
        resp.append(ship_dict)
    return resp

print(get_package(1))

def delete_package(package_id):
    query = f"DELETE FROM labels WHERE \'shipid\' IS \'{package_id}\'"
    return inter.execute_query(query)
