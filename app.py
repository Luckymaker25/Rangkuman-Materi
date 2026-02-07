import streamlit as st
import pandas as pd

# Judul Aplikasi
st.set_page_config(page_title="Rangkuman Materi", page_icon="📚")
st.title("📚 Dashboard Materi")

# 1. Koneksi ke GSheet (Ganti dengan link CSV kamu)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHsSznI1DtoHsc4Te0kG6CeG_GtWMpJLbb5v2IFF35066sOpj9irgpqYvdZfbpXyfePvatgNX8b_Ad/pub?gid=0&single=true&output=csv"

# Fungsi untuk mengambil data (cache agar cepat)
@st.cache_data
def load_data():
    return pd.read_csv(SHEET_URL)

df = load_data()
st.write("Nama kolom yang terdeteksi:", df.columns.tolist())

# 2. Fitur Pencarian di Bagian Atas
search_query = st.text_input("🔍 Cari materi atau kategori...", "")

# 3. Logika Filter
if search_query:
    # Mencari di seluruh kolom (Case Insensitive)
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
else:
    filtered_df = df

# 4. Tampilan di HP (Menggunakan Container agar rapi)
st.write(f"Menampilkan {len(filtered_df)} materi")

for index, row in filtered_df.iterrows():
    with st.expander(f"📖 {row['Judul']}"): # Judul yang bisa diklik/drop-down
        st.write(f"**Kategori:** {row['Kategori']}")
        st.write(f"**Sub-Kategori:** {row['Sub-Kategori']}")
        st.markdown("---")

        st.write(row['Isi_Materi']) # Detail isi materi

