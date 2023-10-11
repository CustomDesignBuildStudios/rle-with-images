from console_gfx import ConsoleGfx
#RLE image encoder gives the user multiple options to load images and display those images

hex_num_to_string_array = {
    10:"a",
    11:"b",
    12:"c",
    13:"d",
    14:"e",
    15:"f"
}
hex_string_to_num_array = {
    "a":10,
    "b":11,
    "c":12,
    "d":13,
    "e":14,
    "f":15
}
#Takes a hex string and returns the number
def hex_string_to_number(hex_str):
    if hex_str in hex_string_to_num_array:
        return hex_string_to_num_array[hex_str]
    else:
        return str(hex_str)
#Takes a number and returns as a hex string   
def number_to_hex_string(num):
    if num in hex_num_to_string_array:
        return hex_num_to_string_array[num]
    else:
        return str(num)
#Translates data (RLE or raw) a hexadecimal string (without delimiters).
def to_hex_string(data):
    hex_string = ""
    for item in data:
        hex_string += number_to_hex_string(item)
    return hex_string

def to_flat_string(rle_data):
    hex_string = ""
    for i in range(0,len(rle_data),2):
        hex_string += number_to_hex_string(rle_data[i+1]) * int(rle_data[i]) 
    return hex_string

#Returns number of runs of data in an image data set; double this result for length of encoded (RLE) list
def count_runs(flat_data):
    count = 0
    previous_item = ""
    num_count = 0
    for item in flat_data:
        if previous_item != item:
            previous_item = item
            count += 1
            num_count += 1
        else:
            if num_count >= 15:
                count += 1
                num_count = 1
            else:
                num_count += 1

    return count


#Returns encoding (in RLE) of the raw data passed in; used to generate RLE representation of a data.
def encode_rle(flat_data):
    count = 0
    previous_item = ""

    new_data = []

    for item in flat_data:
        if previous_item != item:
            previous_item = item
            new_data.append([1,item])
        else:
            if new_data[-1][0] >= 15:
                previous_item = item
                new_data.append([1,item])
            else:
                new_data[-1][0] += 1

    new_array = []
    for item in new_data:
        new_array.append(item[0])
        new_array.append(item[1])
    return new_array
#Returns decompressed size RLE data; used to generate flat data from RLE encoding.
def get_decoded_length(rle_data):
    count = 0
    for i in range(0,len(rle_data),2):
        count += rle_data[i]
    return count
#Returns the decoded data set from RLE encoded data. This decompresses RLE data for use
def decode_rle(rle_data):
    decoded_data = []
    for i in range(0,len(rle_data),2):
        num_of_data = rle_data[i]
        data_item = rle_data[i+1]
        decoded_data.extend([data_item] * num_of_data)
    return decoded_data

#Translates a string in hexadecimal format into byte data (can be raw or RLE).
def string_to_data(data_string):
    data_string = data_string.lower()
    new_array = []
    for item in data_string:
        if item.isnumeric():
            new_array.append(int(item))
        else:
            new_array.append(hex_string_to_num_array[item])
    return new_array
#Translates RLE data into a human-readable representation. Displays the run length in decimal and the run value in hax with a : between runs
def to_rle_string(rle_data):
    rle_string = ""
    for i in range(0,len(rle_data),2):
        if i != 0:
            rle_string += ":"
        rle_string += str(rle_data[i])
        rle_string += number_to_hex_string(rle_data[i+1])
    return rle_string
#Translates a string in human-readable RLE format (with delimiters) into RLE byte data
def string_to_rle(rle_string):
    rle_array = rle_string.lower().split(":")

    data_array = []
    for str_item in rle_array:
        if len(str_item) == 2 and str_item[1].isnumeric():
            data_array.append(int(str_item[0]))
            data_array.append(int(str_item[1]))
        elif len(str_item) == 2 and str_item[1].isnumeric() == False:
            data_array.append(int(str_item[0]))
            data_array.append(int(hex_string_to_number(str_item[1])))
        else:
            data_array.append(int(str_item[:2]))
            data_array.append(hex_string_to_number(str_item[2]))
    return data_array

#print the main menu
def display_menu():
    print("\n\nRLE Menu\n--------\n0. Exit\n1. Load File\n2. Load Test Image\n3. Read RLE String\n4. Read RLE Hex String\n5. Read Data Hex String\n6. Display Image\n7. Display RLE String\n8. Display Hex RLE Data\n9. Display Hex Flat Data")

#process users input
def process_user_menu_input(user_input):
    #Exit Program option selected
    if user_input == 0:
        return False
    #Load file by file path
    if user_input == 1:
        file_name = input("Enter name of file to load: ")
        new_data = ConsoleGfx.load_file(file_name)
        #make sure the file exists and returns data
        if len(new_data) == 0:
            print("File does not exist!")
        else:
            image_data = ConsoleGfx.load_file(file_name)
    #Load test file from ConsoleGFX
    elif(user_input == 2):
        image_data = ConsoleGfx.test_image
        print("Test image data loaded.")
    #Reads RLE data from the user in decimal notation with delimiters
    elif(user_input == 3):
        rle_string = input("Enter an RLE string to be decoded: ")
        image_data = string_to_rle(rle_string)
    #Reads RLE data from the user in hexadecimal notation without delimiters
    elif(user_input == 4):
        rle_string = input("Enter the hex string holding RLE data: ")
        image_data = string_to_data(rle_string)
    #Reads raw (flat) data from the user in hexadecimal notation
    elif(user_input == 5):
        rle_string = input("Enter the hex string holding flat data: ")
        image_data = string_to_data(rle_string)
    #Display loaded file in console
    elif user_input == 6:
        print("Displaying image...")
        ConsoleGfx.display_image(image_data)
    #Converts the current data into RLE hexadecimal representation (without delimiters)
    elif(user_input == 7):
        print(f"RLE representation: {to_rle_string(image_data)}")
    #Converts the current data into RLE hexadecimal representation (without delimiters)
    elif(user_input == 8):
        print(f"RLE hex values: {to_hex_string(image_data)}")
    #Displays the current raw (flat) data in hexadecimal representation (without delimiters):
    elif(user_input == 9):
        print(f"Flat hex values: {to_flat_string(image_data)}")
    #Incorrect option selcted
    else:
        print("\n\nIncorrect Menu Input Selected")



def main():
    print("Welcome to the RLE image encoder!")
    print("\nDisplaying Spectrum Image:")
    #display test rainbow image
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)

    image_data = None
    while True:
        #display main menu
        display_menu()
        user_input = int(input("\nSelect a Menu Option: "))
        process_user_menu_input(user_input)

if __name__ == '__main__':
    main()