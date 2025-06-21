import streamlit as st
import qrcode
import os
from PIL import Image
import json

# Directory to store items
ITEMS_DIR = "Items"
os.makedirs(ITEMS_DIR, exist_ok=True)

# Load or initialize locations
LOCATIONS_FILE = "locations.json"
if os.path.exists(LOCATIONS_FILE):
    with open(LOCATIONS_FILE, "r") as f:
        locations = json.load(f)
else:
    locations = {f"location{i}": [] for i in range(1, 7)}
    with open(LOCATIONS_FILE, "w") as f:
        json.dump(locations, f)

# Save updated locations
def save_locations():
    with open(LOCATIONS_FILE, "w") as f:
        json.dump(locations, f)

# UI
st.title("📦 Barcode & Picture Manager")

item_name = st.text_input("Enter Item Name")

st.subheader("1. Generate & View")

option = st.selectbox("Select to Display", ["", "item_barcode", "item_picture"])

if st.button("Generate"):
    if not item_name:
        st.error("Please enter item name.")
    elif option == "item_barcode":
        qr = qrcode.make(item_name)
        barcode_path = f"{item_name}_barcode.png"
        qr.save(barcode_path)
        st.image(barcode_path, caption="Barcode", use_column_width=True)
    elif option == "item_picture":
        picture_path = os.path.join(ITEMS_DIR, f"{item_name}.png")
        if os.path.exists(picture_path):
            st.image(picture_path, caption="Picture", use_column_width=True)
        else:
            st.error("No picture found.")

st.subheader("2. Upload & Save Picture")

uploaded_file = st.file_uploader("Upload item picture", type=["png", "jpg", "jpeg"])
if uploaded_file and item_name:
    picture_path = os.path.join(ITEMS_DIR, f"{item_name}.png")
    with open(picture_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success(f"Picture saved as {picture_path}")
    st.image(picture_path)

st.subheader("3. Assign Item to Location")

location = st.selectbox("Select Location to Save", list(locations.keys()))
if st.button("Save to Location"):
    if not item_name:
        st.error("Enter item name first.")
    elif len(locations[location]) >= 10:
        st.error("This location is full.")
    else:
        locations[location].append(item_name)
        save_locations()
        st.success(f"Saved '{item_name}' to {location}")

st.subheader("4. View Location Contents")

view_location = st.selectbox("Select Location to View", list(locations.keys()), key="view")
if st.button("Show Location"):
    items = locations[view_location]
    if items:
        st.info(f"Items in {view_location}: {', '.join(items)}")
    else:
        st.warning(f"No items in {view_location}")
