import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==========================================
# 1. KONFIGURASI & HELPER
# ==========================================
st.set_page_config(layout="centered", page_title="WRC Auction House", page_icon="💰")

# Fungsi format angka ke Rupiah (Titik setiap 3 digit)
def format_rupiah(nominal):
    return f"Rp {nominal:,.0f}".replace(",", ".")

# --- CSS TAMPILAN ---
st.markdown("""
<style>
    .stButton button {width: 100%; border-radius: 10px; font-weight: bold;}
    div[data-testid="stImage"] img {border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE MANUAL (Semua 8 Mobil)
# ==========================================
if 'gallery_data' not in st.session_state:
    st.session_state.gallery_data = {
        "Mitsubishi Lancer Evolution VI GSR": {
            "images": [
                "images/Mitsubishi Lancer Evolution VI GSR View_A.avif", "images/Mitsubishi Lancer Evolution VI GSR View_B.avif", 
                "images/Mitsubishi Lancer Evolution VI GSR View_C.avif", "images/Mitsubishi Lancer Evolution VI GSR View_D.avif", 
                "images/Mitsubishi Lancer Evolution VI GSR View_E.avif", "images/Mitsubishi Lancer Evolution VI GSR View_F.avif", 
                "images/Mitsubishi Lancer Evolution VI GSR View_G.avif", "images/Mitsubishi Lancer Evolution VI GSR View_H.avif"
            ],
            "tahun": "1999 (Special Edition)", "specs": "4G63 2.0L Turbo, 280 PS", "driver": "Tommi Mäkinen 🇫🇮",
            "price": 1500000000, "highest_bidder": "Belum ada"
        },
        "Audi Quattro S1 E2": {
            "images": [
                "images/Audi Quattro S1 E2 View_A.avif", "images/Audi Quattro S1 E2 View_B.avif", "images/Audi Quattro S1 E2 View_C.avif", 
                "images/Audi Quattro S1 E2 View_D.avif", "images/Audi Quattro S1 E2 View_E.avif", "images/Audi Quattro S1 E2 View_F.avif", 
                "images/Audi Quattro S1 E2 View_G.avif", "images/Audi Quattro S1 E2 View_H.avif"
            ],
            "tahun": "1985 (Group B)", "specs": "2.1L I5 Turbo, 591 HP", "driver": "Walter Röhrl 🇩🇪 / Stig Blomqvist 🇸🇪",
            "price": 5000000000, "highest_bidder": "Museum Jerman"
        },
        "Lancia Delta HF Integrale": {
            "images": [
                "images/Lancia Delta HF Integrale View_A.avif", "images/Lancia Delta HF Integrale View_B.avif", "images/Lancia Delta HF Integrale View_C.avif", 
                "images/Lancia Delta HF Integrale View_D.avif", "images/Lancia Delta HF Integrale View_Z.avif", "images/Lancia Delta HF Integrale View_F.avif", 
                "images/Lancia Delta HF Integrale View_G.avif", "images/Lancia Delta HF Integrale View_H.avif"
            ],
            "tahun": "1992 (Evo)", "specs": "2.0L Turbo 16V, 210 HP", "driver": "Juha Kankkunen 🇫🇮 / Miki Biasion 🇮🇹",
            "price": 2800000000, "highest_bidder": "Kolektor Italia"
        },
        "Mitsubishi Lancer Evolution V GSR": {
            "images": [
                "images/Mitsubishi Lancer Evolution V GSR View_A.avif", "images/Mitsubishi Lancer Evolution V GSR View_B.avif", "images/Mitsubishi Lancer Evolution V GSR View_C.avif", 
                "images/Mitsubishi Lancer Evolution V GSR View_D.avif", "images/Mitsubishi Lancer Evolution V GSR View_E.avif", "images/Mitsubishi Lancer Evolution V GSR View_F.avif", 
                "images/Mitsubishi Lancer Evolution V GSR View_G.avif", "images/Mitsubishi Lancer Evolution V GSR View_H.avif"
            ],
            "tahun": "1998", "specs": "4G63 Turbo, 276 HP", "driver": "Tommi Mäkinen 🇫🇮",
            "price": 1200000000, "highest_bidder": "Belum ada"
        },
        "Mitsubishi Lancer Evolution X": {
            "images": [
                "images/Mitsubishi Lancer Evolution X View_A.avif", "images/Mitsubishi Lancer Evolution X View_B.avif", "images/Mitsubishi Lancer Evolution X View_C.avif", 
                "images/Mitsubishi Lancer Evolution X View_D.avif", "images/Mitsubishi Lancer Evolution X View_E.avif", "images/Mitsubishi Lancer Evolution X View_F.avif", 
                "images/Mitsubishi Lancer Evolution X View_G.avif", "images/Mitsubishi Lancer Evolution X View_H.avif"
            ],
            "tahun": "2007 - 2016", "specs": "4B11T 2.0L Turbo, 291 HP", "driver": "Fumio Nutahara 🇯🇵",
            "price": 950000000, "highest_bidder": "blm ada"
        },
        "Mitsubishi Lancer Evolution X Kaela Kovalskia": {
            "images": [
                "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_A.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_B.avif", 
                "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_C.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_D.avif", 
                "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_E.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_F.avif", 
                "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_G.avif", "images/Mitsubishi Lancer Evolution X Kaela Kovalskia View_H.avif"
            ],
            "tahun": "2023 (Hololive Edition)", "specs": "Custom Tuned 4B11T, 400+ HP", "driver": "Kaela Kovalskia 🔨",
            "price": 999999999, "highest_bidder": "Simp No. 1"
        },
        "Subaru Impreza 1995 555": {
            "images": [
                "images/Subaru Impreza 1995 555 View_A.avif", "images/Subaru Impreza 1995 555 View_B.avif", "images/Subaru Impreza 1995 555 View_C.avif", 
                "images/Subaru Impreza 1995 555 View_D.avif", "images/Subaru Impreza 1995 555 View_E.avif", "images/Subaru Impreza 1995 555 View_F.avif", 
                "images/Subaru Impreza 1995 555 View_G.avif", "images/Subaru Impreza 1995 555 View_H.avif"
            ],
            "tahun": "1995 (Group A)", "specs": "Ej20 Boxer Turbo, 300 HP", "driver": "Colin McRae 🏴󠁧󠁢󠁳󠁣󠁴󠁿",
            "price": 3500000000, "highest_bidder": "Colin McRae Fans"
        },
        "Subaru WRX STi NR4": {
            "images": [
                "images/Subaru WRX STi NR4 View_A.avif", "images/Subaru WRX STi NR4 View_B.avif", "images/Subaru WRX STi NR4 View_C.avif", 
                "images/Subaru WRX STi NR4 View_D.avif", "images/Subaru WRX STi NR4 View_E.avif", "images/Subaru WRX STi NR4 View_F.avif", 
                "images/Subaru WRX STi NR4 View_G.avif", "images/Subaru WRX STi NR4 View_H.avif"
            ],
            "tahun": "2015 (Production Cup)", "specs": "2.0L Boxer Turbo, 280 HP", "driver": "Mark Higgins 🇬🇧",
            "price": 1100000000, "highest_bidder": "Belum ada"
        }
    }

if 'bid_history' not in st.session_state:
    st.session_state.bid_history = []

# ==========================================
# 3. STATE MANAGEMENT & NAVIGASI
# ==========================================
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = list(st.session_state.gallery_data.keys())[0]
if 'img_index' not in st.session_state:
    st.session_state.img_index = 0

st.title("💰 WRC Championship Auction")
st.caption("Mode: Standalone System (Manual Pathing)")

pilihan_mobil = st.selectbox("📂 Pilih Unit Lelang:", list(st.session_state.gallery_data.keys()))

if pilihan_mobil != st.session_state.selected_car:
    st.session_state.selected_car = pilihan_mobil
    st.session_state.img_index = 0

st.divider()

# ==========================================
# 4. UI LELANG (GALLERY + BIDDING)
# ==========================================
@st.fragment
def show_auction_standalone():
    data_mobil = st.session_state.gallery_data[st.session_state.selected_car]
    list_gambar = data_mobil["images"]
    jumlah_gambar = len(list_gambar)
    
    # 📸 GALERI GAMBAR
    current_path = list_gambar[st.session_state.img_index]
    
    # Safety Check: Pastikan file gambar ada
    if os.path.exists(current_path):
        st.image(current_path, caption=f"Lot: {st.session_state.selected_car}", use_container_width=True)
    else:
        st.error(f"⚠️ Gambar tidak ditemukan: `{current_path}`")
        st.info("💡 Pastikan nama file di folder 'images' SAMA PERSIS dengan di kodingan.")
    
    col_prev, col_bar, col_next = st.columns([1, 4, 1], vertical_alignment="center")
    with col_prev:
        if st.button("◀️"):
            st.session_state.img_index = (st.session_state.img_index - 1) % jumlah_gambar
            st.rerun()
    with col_next:
        if st.button("▶️"):
            st.session_state.img_index = (st.session_state.img_index + 1) % jumlah_gambar
            st.rerun()
    with col_bar:
        st.progress((st.session_state.img_index + 1) / jumlah_gambar)
    
    # STATUS HARGA
    st.markdown("### 🔨 Status Lelang")
    c1, c2 = st.columns(2)
    c1.metric("Harga Tertinggi", format_rupiah(data_mobil['price']))
    c2.metric("Pemegang Bid", data_mobil['highest_bidder'])

    with st.expander("📄 Detail Spesifikasi"):
        st.write(f"**Tahun:** {data_mobil['tahun']}")
        st.write(f"**Driver:** {data_mobil['driver']}")
        st.write(f"**Specs:** {data_mobil['specs']}")

    # INPUT BIDDING
    st.markdown("### 💸 Masukkan Tawaran")
    with st.container(border=True):
        nama = st.text_input("Nama Anda:", placeholder="Contoh: Sultan Jogja")
        harga_input = st.number_input(
            "Nominal Tawaran (Rp):", 
            min_value=data_mobil['price'] + 1000000, 
            value=data_mobil['price'] + 10000000,
            step=10000000
        )
        
        # ✨ LIVE PREVIEW (TITIK OTOMATIS)
        st.info(f"Konfirmasi Angka: **{format_rupiah(harga_input)}**")
        
        if st.button("🔥 KIRIM BID SEKARANG", type="primary"):
            if not nama:
                st.warning("Nama wajib diisi!")
            else:
                st.session_state.gallery_data[st.session_state.selected_car]["price"] = harga_input
                st.session_state.gallery_data[st.session_state.selected_car]["highest_bidder"] = nama
                
                log = {
                    "Waktu": datetime.now().strftime("%H:%M:%S"),
                    "Mobil": st.session_state.selected_car,
                    "Penawar": nama,
                    "Nominal": format_rupiah(harga_input)
                }
                st.session_state.bid_history.insert(0, log)
                st.success(f"Tawaran {format_rupiah(harga_input)} diterima!")
                st.rerun()

show_auction_standalone()

# ==========================================
# 5. TABEL RIWAYAT
# ==========================================
st.divider()
st.subheader("📜 Log Riwayat Penawaran")
if st.session_state.bid_history:
    st.table(pd.DataFrame(st.session_state.bid_history))
else:
    st.info("Belum ada aktivitas lelang.")
