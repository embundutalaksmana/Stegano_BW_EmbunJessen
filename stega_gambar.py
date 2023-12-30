import streamlit as st
import cv2
import numpy as np

def messageToBinary(message):
  if type(message) == str:
    return ''.join([ format(ord(i), "08b") for i in message ])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [ format(i, "08b") for i in message ]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, "08b")
  else:
    raise TypeError("Input type not supported")


# Function to hide the secret message into the image

def hideData(image, secret_message):

  # calculate the maximum bytes to encode
  n_bytes = image.shape[0] * image.shape[1] * 3 // 8
  print("Maximum bytes to encode:", n_bytes)

  #Check if the number of bytes to encode is less than the maximum bytes in the image
  if len(secret_message) > n_bytes:
      raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
  
  secret_message += "#####" # you can use any string as the delimeter

  data_index = 0
  # convert input data to binary format using messageToBinary() fucntion
  binary_secret_msg = messageToBinary(secret_message)

  data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
  for values in image:
      for pixel in values:
          # convert RGB values to binary format
          r, g, b = messageToBinary(pixel)
          # modify the least significant bit only if there is still data to store
          if data_index < data_len:
              # hide the data into least significant bit of red pixel
              pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of green pixel
              pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of  blue pixel
              pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          # if data is encoded, just break out of the loop
          if data_index >= data_len:
              break

  return image

def showData(image):

  binary_data = ""
  for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel) #convert the red,green and blue values into binary format
          binary_data += r[-1] #extracting data from the least significant bit of red pixel
          binary_data += g[-1] #extracting data from the least significant bit of red pixel
          binary_data += b[-1] #extracting data from the least significant bit of red pixel
  # split by 8-bits
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
  # convert from bits to characters
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == "#####": #check if we have reached the delimeter which is "#####"
          break
  #print(decoded_data)
  return decoded_data[:-5] #remove the delimeter to show the original hidden message

# Encode data into image 
def encode_text(image, data):
    encoded_image = hideData(image, data)
    return encoded_image

def decode_text(image):
    return showData(image)


# Image Steganography         
def main():
    st.title("Image Steganography App")

    user_input = st.radio("Select an option:", ["Encode the data", "Decode the data"])

    if user_input == "Encode the data":
        st.header("Encode Data")
        image_name = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if image_name is not None:
            image = cv2.imdecode(np.fromstring(image_name.read(), np.uint8), 1)
            st.image(image, caption="Original Image", use_column_width=True)

            data = st.text_input("Enter data to be encoded:", "")
            if st.button("Encode"):
                encoded_image = encode_text(image, data)
                st.image(encoded_image, caption="Encoded Image", use_column_width=True)

    elif user_input == "Decode the data":
        st.header("Decode Data")
        st.info("Upload the steganographed image for decoding.")
        st.warning("The uploaded image should be the one generated after encoding.")

        steganographed_image = st.file_uploader("Upload steganographed image", type=["jpg", "jpeg", "png"])
        if steganographed_image is not None:
            steg_image = cv2.imdecode(np.fromstring(steganographed_image.read(), np.uint8), 1)
            st.image(steg_image, caption="Steganographed Image", use_column_width=True)

            if st.button("Decode"):
                decoded_message = decode_text(steg_image)
                st.success(f"Decoded Message: {decoded_message}")

if __name__ == "__main__":
    main()