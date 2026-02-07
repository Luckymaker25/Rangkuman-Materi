import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rangkuman Materi", layout="centered")

# Judul Utama
st.title("📚 Dashboard Materi")

# 1. Ambil Data
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHsSznI1DtoHsc4Te0kG6CeG_GtWMpJLbb5v2IFF35066sOpj9irgpqYvdZfbpXyfePvatgNX8b_Ad/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # Membersihkan spasi di nama kolom agar tidak error lagi
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# --- BAGIAN FILTER ---

# A. Search Bar (Global Search)
search_query = st.text_input("🔍 Cari Kata Kunci Materi...", "")

# B. Dropdown Kategori (Berjenjang)
col1, col2 = st.columns(2)

with col1:
    list_kategori = ["Semua"] + sorted(df['Kategori'].unique().tolist())
    kat_pilihan = st.selectbox("Pilih Kategori:", list_kategori)

with col2:
    # Filter Sub-Kategori berdasarkan Kategori yang dipilih
    if kat_pilihan != "Semua":
        sub_df = df[df['Kategori'] == kat_pilihan]
        list_sub = ["Semua"] + sorted(sub_df['Sub-Kategori'].unique().tolist())
    else:
        list_sub = ["Semua"] + sorted(df['Sub-Kategori'].unique().tolist())
    
    sub_pilihan = st.selectbox("Pilih Sub-Kategori:", list_sub)

# --- LOGIKA FILTERING ---
filtered_df = df.copy()

if kat_pilihan != "Semua":
    filtered_df = filtered_df[filtered_df['Kategori'] == kat_pilihan]

if sub_pilihan != "Semua":
    filtered_df = filtered_df[filtered_df['Sub-Kategori'] == sub_pilihan]

if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

# --- TAMPILAN MATERI ---
st.write(f"Menampilkan **{len(filtered_df)}** materi")

for index, row in filtered_df.iterrows():
    # Menampilkan Judul sebagai Header Card
    with st.expander(f"📌 {row['Judul']}"):
        st.caption(f"Kategori: {row['Kategori']} | Sub: {row['Sub-Kategori']}")
        
        st.markdown("### 📖 Isi Materi")
        st.write(row['Isi Materi'])
        
        # Menampilkan Study Kasus jika tidak kosong
        if pd.notna(row['Study kasus/SubMateri']):
            st.markdown("### 📝 Study Kasus / SubMateri")
            st.info(row['Study kasus/SubMateri'])
        
        st.divider()
