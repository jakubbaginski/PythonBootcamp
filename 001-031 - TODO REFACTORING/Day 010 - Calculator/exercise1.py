def format_name (f_name, l_name):
    """
    Format first and last name:
    first letter will be upper and the rest lower-case
    """
    f_name = f_name[0].upper() + f_name[1:].lower()
    l_name = l_name[0].upper() + l_name[1:].lower()

    return f"{f_name} {l_name}"

print(format_name("jakUB", "BagiŃski"))