import streamlit as st
from PIL import Image

def lsb_encode(cover_path, secret_path, output_path):
    cover = Image.open(cover_path).convert('RGB')
    secret = Image.open(secret_path).convert('RGB')

    cover_data = cover.getdata()
    secret_data = secret.getdata()

    stego_data = []
    for cover_pixel, secret_pixel in zip(cover_data, secret_data):
        stego_pixel = []
        for c, s in zip(cover_pixel, secret_pixel):
            stego_channel = (c & 0xFE) | ((s >> 7) & 1)
            stego_pixel.append(stego_channel)
        stego_data.append(tuple(stego_pixel))

    stego = Image.new('RGB', cover.size)
    stego.putdata(stego_data)
    stego.save(output_path)

def lsb_decode(stego_path):
    stego = Image.open(stego_path).convert('RGB')
    stego_data = stego.getdata()

    extracted_data = []
    for stego_pixel in stego_data:
        extracted_pixel = 0
        for channel in stego_pixel:
            extracted_pixel = (extracted_pixel << 1) | (channel & 1)
        extracted_data.append(extracted_pixel)

    extracted_info = bytes(extracted_data)
    return extracted_info

def main():
    st.title("LSB Steganography App")
    st.sidebar.header("Settings")

    # Upload cover image
    cover_image = st.sidebar.file_uploader("Upload Cover Image", type=["jpg", "jpeg", "png"])

    # Upload secret image
    secret_image = st.sidebar.file_uploader("Upload Secret Image", type=["jpg", "jpeg", "png"])

    if cover_image and secret_image:
        # Output path for stego image
        output_stego_path = "stego_image.png"

        # Sisipkan informasi
        lsb_encode(cover_image, secret_image, output_stego_path)
        st.success("Informasi telah disisipkan ke dalam gambar cover.")

        # Ekstrak informasi
        extracted_info = lsb_decode(output_stego_path)
        st.info("Informasi yang diekstrak: {}".format(extracted_info.decode('utf-8')))

        # Tampilkan gambar cover, secret, dan stego
        st.image([cover_image, secret_image, output_stego_path], caption=["Cover Image", "Secret Image", "Stego Image"])

if __name__ == "__main__":
    main()
