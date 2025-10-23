# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 11:49:48 2025

@author: Administrator
"""
import streamlit as st
import pandas as pd
from PIL import Image
import ast
import os
from rapidfuzz import process  # for fuzzy matching

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv(r"C:\Ghibli AI generated\unzipped_data\captions_large.csv")

# Extract path from 'image' column (dict-like string)
df['image_path'] = df['image'].apply(lambda x: ast.literal_eval(x)['path'])

# Create local path to images
df['local_image_path'] = df['image_path'].apply(
    lambda p: os.path.join(r"C:\Ghibli AI generated\unzipped_data\images", os.path.basename(p))
)

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(page_title="🎨 Ghibli AI Caption Search", layout="centered")

st.title("🎨 Ghibli AI Caption Search")
st.write("🔍 Type your caption below to find the most relevant Ghibli-style image!")

# User enters a caption
user_caption = st.text_input("Enter a caption:")

# Matching method
match_type = st.radio(
    "Choose matching type:",
    ("Exact Match", "Partial Match", "Fuzzy Match (Recommended)"),
    horizontal=True
)

# Button to show image
if st.button("Show Image"):
    if user_caption.strip() == "":
        st.warning("⚠️ Please enter a caption first.")
    else:
        img_path = None
        matched_caption = None

        # -------------------------
        # 1️⃣ Exact match
        # -------------------------
        if match_type == "Exact Match":
            match = df[df['caption'].str.lower() == user_caption.strip().lower()]
            if not match.empty:
                matched_caption = match.iloc[0]['caption']
                img_path = match.iloc[0]['local_image_path']

        # -------------------------
        # 2️⃣ Partial match
        # -------------------------
        elif match_type == "Partial Match":
            match = df[df['caption'].str.lower().str.contains(user_caption.strip().lower(), na=False)]
            if not match.empty:
                matched_caption = match.iloc[0]['caption']
                img_path = match.iloc[0]['local_image_path']

        # -------------------------
        # 3️⃣ Fuzzy match (handles typos)
        # -------------------------
        elif match_type == "Fuzzy Match (Recommended)":
            captions = df['caption'].dropna().tolist()
            result = process.extractOne(user_caption, captions, score_cutoff=60)
            if result:
                matched_caption, score, idx = result
                img_path = df.iloc[idx]['local_image_path']

        # -------------------------
        # Display result
        # -------------------------
        if img_path:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                st.image(img, caption=f"🖼️ Matched Caption: {matched_caption}")
                st.success("✅ Image found successfully!")
            else:
                st.error("⚠️ Image file not found at the specified path.")
        else:
            st.error("❌ No image found for this caption. Please try another one.")

# -------------------------
# Optional Debug Info
# -------------------------
# Uncomment below lines to check how many image files are missing in your dataset
# missing = df[~df['local_image_path'].apply(os.path.exists)]
# st.write(f"🗂️ Missing images in folder: {len(missing)}")
