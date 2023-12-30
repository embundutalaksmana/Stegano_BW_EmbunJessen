import streamlit as st
import numpy as np
from PIL import Image

np.set_printoptions(threshold=np.inf)

# Encoding function
def encode(src, message, dest, password):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message += password
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > (total_pixels * 3):
        st.error("ERROR: Need larger file size")
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        st.success("Image Encoded Successfully")

# Decoding function
def decode(src, password):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    hiddenmessage = ""
    for i in range(len(hidden_bits)):
        x = len(password)
        if message[-x:] == password:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            message = f'{message}'
            hiddenmessage = message
    # verifying the password
    if password in message:
        st.success(f"Hidden Message: {hiddenmessage[:-x]}")
    else:
        st.error("You entered the wrong password: Please Try Again")

# Streamlit app
def main():
    st.title("$t3g0 - Image Steganography")
    st.sidebar.title("Options")

    options = ["Encode", "Decode"]
    func = st.sidebar.selectbox("Select Operation", options)

    if func == "Encode":
        st.subheader("Encode")
        src = st.file_uploader("Upload Source Image", type=["jpg", "jpeg", "png"])
        message = st.text_area("Enter Message to Hide")
        dest = st.text_input("Enter Destination Image Path")
        password = st.text_input("Enter Password", type="password")

        if st.button("Encode"):
            if src is not None and message and dest and password:
                encode(src, message, dest, password)
            else:
                st.error("Please fill in all the required fields.")

    elif func == "Decode":
        st.subheader("Decode")
        src = st.file_uploader("Upload Source Image", type=["jpg", "jpeg", "png"])
        password = st.text_input("Enter Password", type="password")

        if st.button("Decode"):
            if src is not None and password:
                decode(src, password)
            else:
                st.error("Please fill in all the required fields.")

if __name__ == "__main__":
    main()
