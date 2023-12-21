import streamlit as st
import numpy as np
from PIL import Image

def text_to_binary(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def encode_lsb(image, secret_text):
    binary_secret_text = text_to_binary(secret_text)
    binary_secret_text += '1111111111111110'  # Menambahkan delimiter akhir

    data_index = 0
    image_data = np.array(image)

    for row in range(image_data.shape[0]):
        for col in range(image_data.shape[1]):
            for color_channel in range(image_data.shape[2]):
                if data_index < len(binary_secret_text):
                    pixel_value = image_data[row, col, color_channel]
                    new_pixel_value = pixel_value & 0b11111110 | int(binary_secret_text[data_index])
                    image_data[row, col, color_channel] = new_pixel_value
                    data_index += 1

    return Image.fromarray(image_data.astype('uint8'))

def decode_lsb(image):
    binary_secret_text = ''
    image_data = np.array(image)

    for row in range(image_data.shape[0]):
        for col in range(image_data.shape[1]):
            for color_channel in range(image_data.shape[2]):
                pixel_value = image_data[row, col, color_channel]
                binary_secret_text += str(pixel_value & 1)

    delimiter_index = binary_secret_text.find('1111111111111110')
    binary_secret_text = binary_secret_text[:delimiter_index]

    # Convert binary to text
    secret_text = ''.join(chr(int(binary_secret_text[i:i+8], 2)) for i in range(0, len(binary_secret_text), 8))
    return secret_text

def main():
    st.title("LSB Steganography for Text in RGB Image")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        secret_text = st.text_area("Enter the secret text:")
        encode_button = st.button("Encode")

        if encode_button:
            original_image = Image.open(uploaded_image)
            st.image(original_image, caption="Original Image", use_column_width=True)

            encoded_image = encode_lsb(original_image, secret_text)
            st.image(encoded_image, caption="Encoded Image", use_column_width=True)

            st.success("Image encoded successfully!")

        st.header("Decode Secret Text from Image")
        uploaded_encoded_image = st.file_uploader("Upload the encoded image", type=["jpg", "jpeg", "png"])

        if uploaded_encoded_image is not None:
            decode_button = st.button("Decode")

            if decode_button:
                encoded_image = Image.open(uploaded_encoded_image)
                st.image(encoded_image, caption="Encoded Image", use_column_width=True)

                decoded_text = decode_lsb(encoded_image)
                st.success(f"Decoded Secret Text: {decoded_text}")

if __name__ == "__main__":
    main()
