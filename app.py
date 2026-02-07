import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rangkuman Materi", layout="centered")

st.title("📚 Dashboard Materi")

# 1. Ambil Data
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHsSznI1DtoHsc4Te0kG6CeG_GtWMpJLbb5v2IFF35066sOpj9irgpqYvdZfbpXyfePvatgNX8b_Ad/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_URL)
    # MEMBERSIHKAN NAMA KOLOM: Menghapus spasi di awal/akhir
    df.columns = [col.strip() for col in df.columns]
    return df

try:
    df = load_data()

    # --- BAGIAN FILTER ---
    search_query = st.text_input("🔍 Cari Kata Kunci Materi...", "")

    col1, col2 = st.columns(2)

    with col1:
        # Gunakan nama kolom sesuai gambar: 'Kategori'
        list_kategori = ["Semua"] + sorted([str(x) for x in df['Kategori'].dropna().unique()])
        kat_pilihan = st.selectbox("Pilih Kategori:", list_kategori)

    with col2:
        # Gunakan nama kolom sesuai gambar: 'Sub-Kategori'
        if kat_pilihan != "Semua":
            sub_df = df[df['Kategori'] == kat_pilihan]
            raw_sub = sub_df['Sub-Kategori'].dropna().unique()
        else:
            raw_sub = df['Sub-Kategori'].dropna().unique()
        
        list_sub = ["Semua"] + sorted([str(x) for x in raw_sub])
        sub_pilihan = st.selectbox("Pilih Sub-Kategori:", list_sub)

    # --- LOGIKA FILTERING ---
    df_display = df.fillna("")
    filtered_df = df_display.copy()

    if kat_pilihan != "Semua":
        filtered_df = filtered_df[filtered_df['Kategori'] == kat_pilihan]
    if sub_pilihan != "Semua":
        filtered_df = filtered_df[filtered_df['Sub-Kategori'] == sub_pilihan]
    if search_query:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    # --- TAMPILAN MATERI ---
    st.write(f"Menampilkan **{len(filtered_df)}** materi")

    for index, row in filtered_df.iterrows():
        # Menggunakan .get() agar jika kolom tidak ditemukan, aplikasi tidak crash
        judul = row.get('Judul', 'Tanpa Judul')
        isi = row.get('Isi Materi', 'Isi tidak ditemukan')
        study = row.get('Study kasus/SubMateri', '')

        with st.expander(f"📌 {judul}"):
            st.caption(f"Kategori: {row.get('Kategori')} | Sub: {row.get('Sub-Kategori')}")
            st.markdown("### 📖 Isi Materi")
            st.write(isi)
            
            if study != "":
                st.markdown("### 📝 Study Kasus / SubMateri")
                st.info(study)
            st.divider()

except Exception as e:
    st.error(f"Terjadi kesalahan pembacaan data: {e}")
    st.write("Daftar kolom yang ditemukan di GSheet kamu adalah:")
    if 'df' in locals():
        st.write(df.columns.tolist())
