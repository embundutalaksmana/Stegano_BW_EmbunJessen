import streamlit as st
from PIL import Image
import io
def encode(img, message):
    pixels = list(img.getdata())
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
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
def decode(img):
    pixels = list(img.getdata())
    binary_message = ""
    for pixel in pixels:
        for color in pixel[:3]:
            binary_message += str(color & 1)
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if byte == '11111111':
            break
        message += chr(int(byte, 2))
    return message

# Streamlit App
st.title("Steganografi Gambar Hitam Putih dengan Algoritma LSB")
option = st.selectbox("Pilih Operasi", ["Encode", "Decode"])
if option == "Encode":
    st.subheader("Sisipkan Pesan ke dalam Gambar")
    image_file = st.file_uploader("Pilih Gambar", type=["jpg","png"])
    message = st.text_area("Masukkan Pesan yang Akan Disisipkan")
     # Pengecekan ukuran minimal 25KB
    if image_file is not None and image_file.size < 25 * 1024:  # 25 KB dalam byte
        st.warning("Ukuran gambar harus minimal 25KB.")
    
    if st.button("Encode"):
        
        if image_file is not None and message != "":
            img = Image.open(io.BytesIO(image_file.read()))
            
            encoded_img = encode(img, message)
            st.image(encoded_img, caption="Gambar Hasil Encode", use_column_width=True)
        else:
            st.warning("Silakan pilih gambar dan masukkan pesan terlebih dahulu.")
elif option == "Decode":
    st.subheader("Ekstrak Pesan dari Gambar")
    image_file = st.file_uploader("Pilih Gambar yang Telah Disisipkan Pesan", type=["png"])
    if st.button("Decode"):
        if image_file is not None:
            img = Image.open(io.BytesIO(image_file.read()))
            
            decoded_message = decode(img)
            st.success(f"Pesan yang diekstrak: {decoded_message}")
        else:
            st.warning("Silakan pilih gambar terlebih dahulu.")