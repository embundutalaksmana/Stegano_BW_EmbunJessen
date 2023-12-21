import streamlit as st
from PIL import Image
import numpy as np

def encode_lsb(image_array, text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    binary_text += '1111111111111110'  # Adding a delimiter to mark the end of the message

    data_index = 0
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for k in range(image_array.shape[2]):
                if data_index < len(binary_text):
                    image_array[i, j, k] = int(format(image_array[i, j, k], '08b')[:-1] + binary_text[data_index], 2)
                    data_index += 1

    return image_array

def decode_lsb(image_array):
    binary_text = ''
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for k in range(image_array.shape[2]):
                binary_text += format(image_array[i, j, k], '08b')[-1]

    delimiter_index = binary_text.find('1111111111111110')
    text_binary = binary_text[:delimiter_index]

    decoded_text = ''
    for i in range(0, len(text_binary), 8):
        decoded_text += chr(int(text_binary[i:i+8], 2))

    return decoded_text

def main():
    st.title("LSB Steganography with Streamlit")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        image_array = np.array(image)

        action = st.radio("Select an action:", ("Encode", "Decode"))

        if action == "Encode":
            message = st.text_area("Enter the text to hide:")
            if st.button("Encode"):
                if message:
                    encoded_image_array = encode_lsb(image_array.copy(), message)
                    encoded_image = Image.fromarray(encoded_image_array)
                    st.image(encoded_image, caption="Encoded Image", use_column_width=True)
                else:
                    st.warning("Please enter a message to hide.")
        elif action == "Decode":
            if st.button("Decode"):
                decoded_text = decode_lsb(image_array.copy())
                st.success(f"Decoded Text: {decoded_text}")

if __name__ == "__main__":
    main()
