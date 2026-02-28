def format_house_registration(data):

    if(not data):
        return []

    output = []

    for d in data:

        format_data = {

            "house_no" : d.house_no,
            "address": f"{d.address_rest} แขวง{d.sub_district_th} เขต{d.district_th} {d.province_th}",
            "registry_office" : d.registry_office,
            "village_name" : d.village_name,
            "house_type" : d.house_type,
            "house_name" : d.house_name,
            "house_specification" : d.house_specification,
            "date_of_registration" : d.date_of_registration,
            "date_of_print_house_registration" : d.date_of_print_house_registration
        }

        output.append(format_data)
    
    return output