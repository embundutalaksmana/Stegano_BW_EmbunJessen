import streamlit as st
from PIL import Image

def encode_image(original_image, secret_message):
    img = Image.open(original_image)
    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)

    data_index = 0
    img_data = list(img.getdata())

    for i in range(len(img_data)):
        pixel = list(img_data[i])

        for j in range(3):
            if data_index < len(binary_secret_message):
                pixel[j] = pixel[j] & ~1 | int(binary_secret_message[data_index])
                data_index += 1

        img_data[i] = tuple(pixel)

    encoded_img = Image.new("RGB", img.size)
    encoded_img.putdata(img_data)

    return encoded_img


def decode_image(encoded_image):
    img = Image.open(encoded_image)
    binary_data = ''

    img_data = list(img.getdata())

    for i in range(len(img_data)):
        pixel = list(img_data[i])

        for j in range(3):
            binary_data += str(pixel[j] & 1)

    decoded_message = ''.join([chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)])
    return decoded_message

def main():
    st.title("Steganography Tool")

    menu = ["Encode", "Decode"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Encode":
        st.subheader("Encode Your Message")

        original_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if original_image is not None:
            secret_message = st.text_area("Enter your secret message")

            if st.button("Encode"):
                encoded_img = encode_image(original_image, secret_message)
                st.image(encoded_img, caption="Encoded Image", use_column_width=True, channels="RGB")
                st.write(f"Image Dimensions: {encoded_img.size[0]} x {encoded_img.size[1]}")

    elif choice == "Decode":
        st.subheader("Decode Message from Image")

        encoded_image = st.file_uploader("Upload Encoded Image", type=["jpg", "jpeg", "png"])
        if encoded_image is not None:
            if st.button("Decode"):
                decoded_message = decode_image(encoded_image)
                st.success(f"Decoded Message: {decoded_message}")

if __name__ == "__main__":
    main()
