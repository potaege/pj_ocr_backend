def format_thai_id(data):

    if(not data):
        return {}

    output = {
        "citizen_id": data.citizen_id,

        "name_th": f"{data.prefix_name_th} {data.first_name_th} {data.last_name_th}",

        "name_eng": f"{data.prefix_name_eng} {data.first_name_en} {data.last_name_en}",

        "birthday": data.birthday,
        "religion": data.religion,

        "address": f"{data.address_rest} แขวง{data.sub_district_th} เขต{data.district_th} {data.province_th}",

        "issue_date": data.issue_date,
        "expiry_date": data.expiry_date
    }

    return output
