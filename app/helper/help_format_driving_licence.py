def format_driving_licence(data):

    if(not data):
        return []

    output = []

    for d in data:
        
        format_data = {
            "driving_licence_type" : d.driving_licence_type,
            "driving_licence_id" : d.driving_licence_id,
            "name_th": f"{d.prefix_name_th} {d.first_name_th} {d.surname_th}",
            "name_eng": f"{d.prefix_name_eng} {d.first_name_en} {d.surname_en}",
            "citizen_id": d.citizen_id,
            "birthday": d.birthday,
            "provinces" : d.provinces_th,
            "issue_date": d.issue_date,
            "expiry_date": d.expiry_date
        }
        output.append(format_data)

    return output 