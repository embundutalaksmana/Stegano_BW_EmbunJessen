import streamlit as st
from PIL import Image
import numpy as np

def text_to_binary(text):
    binary_result = ' '.join(format(ord(char), '08b') for char in text)
    return binary_result

def binary_to_text(binary_str):
    binary_values = binary_str.split(' ')
    ascii_characters = ''.join(chr(int(b, 2)) for b in binary_values)
    return ascii_characters

def encode_image(img, message):
    binary_message = text_to_binary(message)
    data_index = 0

    img_array = np.array(img)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(3):  # Loop through RGB channels
                if data_index < len(binary_message):
                    img_array[i, j, k] = img_array[i, j, k] & ~1 | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
            if data_index >= len(binary_message):
                break

    encoded_img = Image.fromarray(img_array)
    return encoded_img

def decode_image(img):
    binary_message = ''
    
    img_array = np.array(img)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            for k in range(3):  # Loop through RGB channels
                binary_message += str(img_array[i, j, k] & 1)
    
    return binary_to_text(binary_message)

# Streamlit App
def main():
    st.title("LSB Steganography with Streamlit")

    uploaded_image = st.file_uploader("Choose an image...", type="jpg")

    if uploaded_image is not None:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        operation = st.sidebar.radio("Select operation:", ("Encode", "Decode"))

        if operation == "Encode":
            message = st.text_area("Enter the message to encode:")
            if st.button("Encode"):
                if message:
                    encoded_image = encode_image(original_image, message)
                    st.image(encoded_image, caption="Encoded Image", use_column_width=True)
                else:
                    st.warning("Please enter a message to encode.")

        elif operation == "Decode":
            if st.button("Decode"):
                decoded_message = decode_image(original_image)
                st.success(f"Decoded Message: {decoded_message}")

if __name__ == "__main__":
    main()
