def check_for_validity_of_file(FIELDS, row):
    if row and FIELDS[1] in row:
        for field in FIELDS:
            if field not in row:
                raise Exception(f"Unable to find column header {field}")
    else:
        raise Exception("Unable to find the header row")
