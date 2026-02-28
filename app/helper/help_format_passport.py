def format_passport(data):

    if(not data):
        return {}

    output = {
        "passport_no": data.passport_no,
        "type" : data.type,
        "country_code" : data.country_code,
        "name_th": f"{data.prefix_name_th} {data.first_name_th} {data.surname_th}",

        "name_eng": f"{data.prefix_name_eng} {data.first_name_eng} {data.surname_eng}",
        "nationality": data.nationality,
        "place_of_birth": data.place_of_birth,

        "citizen_id" : data.citizen_id,
        "sex" : data.sex,
        "height" : data.height,
        "birthday" : data.birthday,

        "issue_date": data.issue_date,
        "expiry_date": data.expiry_date
    }

    return output

