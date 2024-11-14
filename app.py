import streamlit as st
import os
import numpy as np
from sklearn.decomposition import PCA
from skimage import io, color
from skimage.util import img_as_ubyte

# Directory for saving uploads and compressed files
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

def reduce_image(file_name, accuracy, output_path):
    """Compresses the image using PCA."""
    image = io.imread(file_name)
    gray_image = color.rgb2gray(image)

    # Apply PCA
    pca = PCA(n_components=accuracy)
    transformed_image = pca.fit_transform(gray_image)
    reconstructed_image = pca.inverse_transform(transformed_image)

    # Normalize and save the compressed image
    compressed_image_normalized = (reconstructed_image - reconstructed_image.min()) / (
        reconstructed_image.max() - reconstructed_image.min()
    )
    compressed_image_uint8 = img_as_ubyte(compressed_image_normalized)
    io.imsave(output_path, compressed_image_uint8)

# Inject custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(-45deg, #d3d3d3, #ffffff, #a9a9a9, #f5f5f5);
            background-size: 400% 400%;
            animation: gradientShift 10s ease infinite;
            font-family: 'Arial', sans-serif;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .title {
            font-size: 3rem;
            font-weight: bold;
            color: #ff4d4d;
            text-shadow: 0 0 10px #ff4d4d, 0 0 20px #ff1a1a;
            text-align: center;
            margin-bottom: 1rem;
        }

        .description {
            text-align: center;
            font-size: 1.2rem;
            color: #ffffff;
            margin-bottom: 2rem;
        }

        .neon-button {
            background: linear-gradient(145deg, #ff4d4d, #ff1a1a);
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-shadow: 0 0 5px white;
            transition: all 0.3s ease;
            box-shadow: 0px 8px 0px #b30000;
        }

        .neon-button:hover {
            transform: scale(1.1);
            box-shadow: 0px 15px 20px #ff1a1a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Description
st.markdown('<div class="title"> Image Compression </div>', unsafe_allow_html=True)
st.markdown('<div class="description">Upload an image</div>', unsafe_allow_html=True)

# File uploader widget
uploaded_file = st.file_uploader("Choose an Image File", type=["png", "jpg", "jpeg"])

# Dropdown for accuracy selection
accuracy = st.selectbox("Select Compression Accuracy", [0.8, 0.9, 0.95, 0.99], index=2)

if uploaded_file is not None:
    # Save the uploaded file to the UPLOAD_FOLDER
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    # Define compressed file path
    compressed_filename = f"compressed_{uploaded_file.name}"
    compressed_path = os.path.join(COMPLEssED_FOLDER, compressed_filename)

    # Compress the image
    reduce_image(image_path, accuracy, compressed_path)
    st.success("✅ Image compressed successfully!")

    # Display the compressed image
    st.image(compressed_path, caption="Compressed Image", use_column_width=True)

    # Provide a download button for the compressed image
    with open(compressed_path, "rb") as file:
        st.markdown(
            f"""
            <a href="data:file/jpeg;base64,{file.read().decode('latin1')}" download="{compressed_filename}">
                <button class="neon-button">📥 Download Compressed Image</button>
            </a>
            """,
            unsafe_allow_html=True,
        )

