import streamlit as st
from PIL import Image

def genData(data):
    newd = [format(ord(i), '08b') for i in data]
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                 imdata.__next__()[:3] +
                                 imdata.__next__()[:3]]

        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                pix[j] += 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def steganography_app():
    st.title("Steganography with Image B & W")

    operation = st.sidebar.selectbox("Select Operation", ["Encode", "Decode","About"])

    if operation == "Encode":
        st.subheader("Encode Data into Image")
        image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        data = st.text_area("Enter Data to be Encoded")

        if st.button("Encode"):
            if image_file is not None and data != "":
                image = Image.open(image_file)
                new_image = image.copy()
                encode_enc(new_image, data)

                st.image(new_image, caption="Encoded Image", use_column_width=True)
            else:
                st.warning("Please upload an image and enter data to be encoded.")

    elif operation == "Decode":
        st.subheader("Decode Data from Image")
        image_file = st.file_uploader("Upload Encoded Image", type=["jpg", "jpeg", "png"])

        if st.button("Decode"):
            if image_file is not None:
                image = Image.open(image_file)
                decoded_data = decode_enc(image)
                st.success(f"Decoded Data: {decoded_data}")
            else:
                st.warning("Please upload an encoded image.")

    elif operation == "About":
        st.subheader("Kelompok Sekian | 4 TI E")
        st.code(f"""
                    Embun Duta Laksmana

                    Jessen Wind Lim)
                    """)
       
def decode_enc(image):
    data = ''
    img_data = iter(image.getdata())

    while True:
        pixels = [value for value in img_data.__next__()[:3] +
                                  img_data.__next__()[:3] +
                                  img_data.__next__()[:3]]

        bin_str = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])
        data += chr(int(bin_str, 2))

        if pixels[-1] % 2 != 0:
            break

    return data

if __name__ == "__main__":
    steganography_app()
