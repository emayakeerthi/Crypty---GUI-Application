from PIL import Image           #from Pillow module import Image function
import numpy as np              #import numpy module in the name of np
from functools import reduce    #import reduce function


#converting password into matrix form
def generate_key_matrix(password, length):
    key = []                                        #generating array of ascii value of pswd

    for char in password:
        key.append(ord(char))                       #ord function return ascii value of given character

    #generating key matrix
    key_matrix = []
    index, password_length = 0,len(password)                #index = index of element in key list
    for row in range(length):
        temp = []
        for col in range(length):
            temp.append(key[index%password_length])         #index % pswd_length used for traversal the list again and again
            index+= 1
        key_matrix.append(temp)
    
    return key_matrix


#Perform multiplication two matrix
def multiply_matrix(submatrix, key):
    enmatrix = []
    if len(submatrix) == len(key[0]):
        multiplier, multiplicand = key, submatrix

    elif len(submatrix[0]) == len(key):
        multiplier, multiplicand = submatrix, key

    #multiply source and key matrix
    for row in range(len(multiplier)):
        #assigning zeros for entire row
        enmatrix.append([0 for _ in range(len(multiplicand[0]))])                 

        for col in range(len(multiplicand[0])):
            for i in range(len(multiplicand)):
                enmatrix[row][col] += multiplier[row][i] * multiplicand[i][col]
            
            #performing modulo 256 with values of matrix to generate rgb value
            enmatrix[row][col] %= 256                                                    

    return np.array(enmatrix)


#finding the factors of given number
def factors(n):    
    factors = set(reduce(list.__add__, 
                ([i, n//i] for i in range(4, int(n**0.5) + 1) if n % i == 0)))

    factors = list(filter(lambda fact: 4<=fact<=12, factors))

    return factors


#Performing encrption of given plane
def encrypt(matrix, key, width, height):
    width_factors = factors(width)
    height_factors = factors(height)

    print(f"Width factors - {width_factors} ; Height factors - {height_factors}")

    if 4 in width_factors:
        submatrix_width = 4
        submatrix_height = height_factors[len(height_factors)//2]

    elif 4 in height_factors:
        submatrix_height = 4
        submatrix_width = width_factors[len(width_factors)//2]

    else:
        if width<height:
            width = width + (width % 4)
            for i in range(height):
                for _ in range(width % 4):
                    matrix[i].append(0)

        else:
            height = height + (height % 4)
            for i in range(height%4):
                matrix.append([0 for __ in range(width)])

        return encrypt(matrix, key, width, height)

    print(f"Submatrix width - {submatrix_width}; Submatrix height - {submatrix_height} ")
    print(matrix)
    exit(0)

    for row_end in range(submatrix_height, (height + submatrix_height), submatrix_height):
        for col_end in range(submatrix_width, (width + submatrix_width), submatrix_width):
            matrix[row_end - submatrix_height:row_end, col_end - submatrix_width:col_end] = multiply_matrix(matrix[row_end - submatrix_height:row_end, col_end - submatrix_width:col_end], key)

    return matrix


#getting image input and display encrpted image
def main():
    #getting path of the image which will be encrypted
    path = input("Enter path of the image: ")   

    #getting password which will be used for encrption or decrption     
    password = input("Enter Encryption Key(Length 8 to 16) :  ")       

    #opening image file
    try:
        #converting image into image object
        image = Image.open(path)
                              
    except Exception as e:
        print(repr(e))
        exit()
        
    #converting image object into numpy ndarray    
    rgb_values = np.array(image)                  
    
    #extracting some details from image object
    format = image.format
    width, height = image.size
    mode = image.mode
    
    #Spliting red, green, blue values
    red = rgb_values[:,:,0]
    green = rgb_values[:,:,1]
    blue = rgb_values[:,:,2]

    #calling generate_key function for key matrix
    key = generate_key_matrix(password, length = 4)
    
    #encrpting three planes individually
    rgb_values[:,:,0] = encrypt(red, key, width, height)
    rgb_values[:,:,1] = encrypt(green, key, width, height)
    rgb_values[:,:,2] = encrypt(blue, key, width, height)
    
    #Generating encrpted image from rgb values and store locally
    image = Image.fromarray(rgb_values)
    image.show()
    image.save(f"EncrptedImage.{format}", quality = 95, subsampling = 0)


if __name__ == '__main__':
    main()