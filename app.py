import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rangkuman Materi", layout="centered")

st.title("📚 Dashboard Materi")

# 1. Ambil Data
# Pastikan link ini adalah link CSV dari "Publish to Web" GSheet kamu
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSHsSznI1DtoHsc4Te0kG6CeG_GtWMpJLbb5v2IFF35066sOpj9irgpqYvdZfbpXyfePvatgNX8b_Ad/pub?gid=0&single=true&output=csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None

df = load_data()

# Pastikan data berhasil dimuat sebelum lanjut
if df is not None:
    # --- BAGIAN FILTER ---
    search_query = st.text_input("🔍 Cari Kata Kunci Materi...", "")

    col1, col2 = st.columns(2)

    with col1:
        list_kategori = ["Semua"] + sorted([str(x) for x in df['Kategori'].dropna().unique()])
        kat_pilihan = st.selectbox("Pilih Kategori:", list_kategori)

    with col2:
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

    is_filtering = False

    if kat_pilihan != "Semua":
        filtered_df = filtered_df[filtered_df['Kategori'] == kat_pilihan]
        is_filtering = True

    if sub_pilihan != "Semua":
        filtered_df = filtered_df[filtered_df['Sub-Kategori'] == sub_pilihan]
        is_filtering = True

    if search_query:
        # Mencari di seluruh kolom (Judul, Isi, dll)
        mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]
        is_filtering = True

    # --- TAMPILAN MATERI ---
    if is_filtering:
        st.write(f"Menampilkan **{len(filtered_df)}** materi")
        
        # Batasi 50 hasil pertama agar HP tidak lag
        for index, row in filtered_df.head(50).iterrows():
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
        
        if len(filtered_df) > 50:
            st.warning("⚠️ Hasil terlalu banyak. Gunakan filter yang lebih spesifik.")
    else:
        st.info("👋 Silakan pilih **Kategori** atau ketik **Kata Kunci** untuk mulai mencari.")
        st.write(f"Total database: **{len(df)}** materi.")

else:
    st.warning("Data kosong atau gagal terhubung ke Google Sheets. Pastikan link CSV sudah benar.")
