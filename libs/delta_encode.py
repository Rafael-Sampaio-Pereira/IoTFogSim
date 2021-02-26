
# Author: Rafael Sampaio
# email: rafaelsampaiop@hotmail.com
# created at: 24 fev 2021


# original_data = [17, 19, 24, 24, 24, 21, 15, 10, 89, 95, 96, 96, 96, 95, 94, 94, 95, 93, 90, 87, 86, 86]
# expected_data = [17, 2, 5, 0, 0, -3, -6, -5, 79, 6, 1, 0, 0, -1, -1, 0, 1, -2, -3, -3, -1, 0]

def delta_encoder(unencoded_data):
    first = unencoded_data[0]
    previous = first
    encoded_data = []
    encoded_data.append(first)
    for code in unencoded_data[1:]:
        encoded_data.append(code-previous)
        previous = code
    return encoded_data


def delta_decoder(encoded_data):
    first = encoded_data[0]
    previous = first
    decoded_data = []
    decoded_data.append(first)
    for code in encoded_data[1:]:
        decoded_data.append(code+previous)
        previous = code+previous
    return decoded_data

# usage:
# encoded_data = delta_encoder(original_data)
# print(encoded_data)
# decoded_data = delta_decoder(encoded_data)
# print(decoded_data)