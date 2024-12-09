import streamlit as st
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession
import pandas as pd
import datetime

# Step 1: Initialize Spark Session
spark = SparkSession.builder \
    .appName("Product Recommendation") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

# Step 2: Load Trained Model
MODEL_PATH = "/app/recommendation_model"
model = ALSModel.load(MODEL_PATH)

# Mapping Marital Status dan Product Category
marital_status_map = {0: "Single", 1: "Married"}
product_category_map = {
    1: "Beauty",
    2: "Health",
    3: "Electronics",
    4: "Groceries",
    5: "Clothing",
    6: "Toys",
    7: "Furniture",
    8: "Books",
    9: "Sports",
    10: "Automotive",
    11: "Home Improvement",
    12: "Gardening",
    13: "Music",
    14: "Movies",
    15: "Software",
    16: "Jewelry",
    17: "Pet Supplies",
    18: "Office Supplies",
    19: "Baby Products",
    20: "Shoes",
}

# Streamlit App Title
st.title("Walmart Product Recommendation System")

# Dropdown untuk Memilih Fungsi Sistem
action = st.selectbox(
    "Pilih Fitur",
    [
        "Product Recommendation by Gender and Age",
        "Product Promo Recommendation",
    ],
)

# Fitur 1: Product Recommendation by Gender and Age
if action == "Product Recommendation by Gender and Age":
    st.subheader("Rekomendasi Produk Berdasarkan Gender dan Umur")
    
    # Input Form
    with st.form("product_recommendation_form"):
        name = st.text_input("Nama Anda")
        phone_number = st.text_input("Nomor HP Anda")
        gender = st.selectbox("Pilih Gender", options=["Male", "Female"])
        age = st.number_input("Masukkan Umur", min_value=0, max_value=120, step=1)
        marital_status = st.selectbox(
            "Status Pernikahan", options=["Single", "Married"]
        )
        

        submit_button = st.form_submit_button("Dapatkan Rekomendasi")

        if submit_button:
            if not name or not phone_number:
                st.warning("Mohon isi Nama dan Nomor HP.")
            else:
                marital_status_value = 0 if marital_status == "Single" else 1
                filtered_data = model[
                    (model["Gender"] == gender) &
                    (model["Age"] == age) &
                    (model["Marital Status"] == marital_status_value)
                ]
                if not filtered_data.empty:
                    filtered_data["Product Category"] = filtered_data[
                        "Product Category"
                    ].map(product_category_map)
                    st.write(f"Terima kasih, {name}!")
                    st.write("Rekomendasi Produk:")
                    st.dataframe(filtered_data[["Product ID", "Product Category"]])
                else:
                    st.warning("Tidak ada rekomendasi yang ditemukan untuk input ini.")

# Fitur 2: Product Promo Recommendation
elif action == "Product Promo Recommendation":
    st.subheader("Rekomendasi Promo Produk")
    
    # Input Form
    with st.form("promo_recommendation_form"):
        name = st.text_input("Nama Anda")
        phone_number = st.text_input("Nomor HP Anda")
        product_category = st.selectbox(
            "Pilih Kategori Produk", options=list(product_category_map.values())
        )
        
        # Rencana Pembelian: Tanggal Pembelian
        purchase_date = st.date_input("Pilih Tanggal Pembelian")
        
        # Tentukan apakah hari libur atau tidak berdasarkan tanggal
        is_holiday = "Yes" if purchase_date.weekday() >= 5 else "No"  # 5=Sabtu, 6=Minggu
        
        # Tampilkan otomatis status libur
        st.write(f"IsHoliday: {is_holiday}")

        submit_button = st.form_submit_button("Dapatkan Rekomendasi Promo")

        if submit_button:
            if not name or not phone_number:
                st.warning("Mohon isi Nama dan Nomor HP.")
            else:
                product_category_value = {
                    v: k for k, v in product_category_map.items()
                }[product_category]
                filtered_data = model[
                    (model["Product Category"] == product_category_value) &
                    (model["IsHoliday"] == (is_holiday == "Yes"))
                ]
                if not filtered_data.empty:
                    st.write(f"Terima kasih, {name}!")
                    st.write("Promo Produk yang Direkomendasikan:")
                    st.dataframe(
                        filtered_data[["Product ID", "Weekly Sales", "Purchase"]]
                    )
                else:
                    st.warning("Tidak ada promo yang ditemukan untuk input ini.")

