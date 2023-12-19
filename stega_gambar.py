import streamlit as st
from PIL import Image

# Fungsi untuk menyisipkan pesan ke dalam gambar
def encode(image_path, message):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Menambahkan delimiter akhir pesan

    data_index = 0
    for i in range(len(pixels)):
        pixel = list(pixels[i])

        for j in range(3):
            if data_index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[data_index])
                data_index += 1

        pixels[i] = tuple(pixel)

    encoded_img = Image.new(img.mode, img.size)
    encoded_img.putdata(pixels)
    return encoded_img

# Fungsi untuk mengekstrak pesan dari gambar
def decode(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_message = ''
    data_index = 0

    for pixel in pixels:
        for value in pixel:
            binary_message += str(value & 1)
            data_index += 1

    delimiter_index = binary_message.find('1111111111111110')
    binary_message = binary_message[:delimiter_index]

    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return message

# Streamlit App
st.title("Steganografi Gambar dengan LSB")

option = st.selectbox("Pilih Operasi", ["Encode", "Decode"])

if option == "Encode":
    st.subheader("Sisipkan Pesan ke dalam Gambar")
    image_file = st.file_uploader("Pilih Gambar", type=["jpg", "jpeg", "png"])
    message = st.text_area("Masukkan Pesan yang Akan Disisipkan")

    if st.button("Encode"):
        if image_file is not None and message != "":
            encoded_img = encode(image_file, message)
            st.image(encoded_img, caption="Gambar Hasil Encode", use_column_width=True)
        else:
            st.warning("Silakan pilih gambar dan masukkan pesan terlebih dahulu.")

elif option == "Decode":
    st.subheader("Ekstrak Pesan dari Gambar")
    image_file = st.file_uploader("Pilih Gambar yang Telah Disisipkan Pesan", type=["jpg", "jpeg", "png"])

    if st.button("Decode"):
        if image_file is not None:
            decoded_message = decode(image_file)
            st.success(f"Pesan yang diekstrak: {decoded_message}")
        else:
            st.warning("Silakan pilih gambar terlebih dahulu.")
