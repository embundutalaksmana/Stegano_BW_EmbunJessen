import streamlit as st
from PIL import Image
import numpy as np

def messageToBinary(pixel):
    if type(pixel) == str:
        return tuple(int(format(ord(i), "08b"), 2) for i in pixel)
    elif type(pixel) == bytes or type(pixel) == np.ndarray:
        return tuple(int(format(i, "08b"), 2) for i in pixel)
    elif type(pixel) == int or type(pixel) == np.uint8:
        return int(format(pixel, "08b"), 2),
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
        binary_values = messageToBinary(pixel)
        # modify the least significant bit only if there is still data to store
        if data_index < data_len:
            # hide the data into the least significant bit of red pixel
            pixel[0] = int(binary_values[0][:-1] + binary_secret_msg[data_index], 2)
            data_index += 1
        if data_index < data_len:
            # hide the data into the least significant bit of green pixel
            pixel[1] = int(binary_values[1][:-1] + binary_secret_msg[data_index], 2)
            data_index += 1
        if data_index < data_len:
            # hide the data into the least significant bit of blue pixel
            pixel[2] = int(binary_values[2][:-1] + binary_secret_msg[data_index], 2)
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
    # Convert PIL Image to numpy array
    image_np = np.array(image)
    encoded_image = hideData(image_np, data)
    # Convert the resulting numpy array back to PIL Image
    encoded_image = Image.fromarray(encoded_image)
    return encoded_image

def encode_text(image, data):
    # Convert PIL Image to numpy array
    image_np = np.array(image)
    encoded_image = hideData(image_np, data)
    # Convert the resulting numpy array back to PIL Image
    encoded_image = Image.fromarray(encoded_image)
    return encoded_image


def main():
    st.title("Image Steganography App")

    user_input = st.radio("Select an option:", ["Encode the data", "Decode the data"])

    if user_input == "Encode the data":
        st.header("Encode Data")
        image_name = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if image_name is not None:
            # Open the image using PIL
            image = Image.open(image_name)
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
            # Open the image using PIL
            steg_image = Image.open(steganographed_image)
            st.image(steg_image, caption="Steganographed Image", use_column_width=True)

            if st.button("Decode"):
                decoded_message = decode_text(steg_image)
                st.success(f"Decoded Message: {decoded_message}")

if __name__ == "__main__":
    main()