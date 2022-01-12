async def convert_string(string):
    converted_string = ''
    for char in string:
            if char == " ":
                    converted_string += ' '
            elif char == ":":
                    converted_string += '꞉'
            else: 
                    converted_string += char
    return converted_string