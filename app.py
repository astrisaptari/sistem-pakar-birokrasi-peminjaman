import streamlit as st

st.set_page_config(page_title="Sistem Pakar Birokrasi Surat", page_icon="📝", layout="centered")

st.title("📝 Sistem Pakar Penentuan Alur Surat & Disposisi")
st.markdown("Aplikasi membantu **Sekretaris Organisasi** menentukan alur pengajuan surat dan berkas lampiran dengan **Forward Chaining**.")

# MEMBUAT TABS UNTUK MEMISAHKAN APLIKASI UTAMA DAN TEORI/BACKWARD CHAINING
tab1, tab2 = st.tabs(["🚀 Demo Sistem (Forward Chaining)", "🌲 Backward Chaining & Teori CF"])

# MAP PERINGKAT ITEM LENGKAP DENGAN LABEL TINGKATAN
ITEM_INFO_MAP = {
    # Fakultas
    "Aula Wiswakarma [Fakultas]": {"nama": "Aula Wiswakarma", "tingkat": "Fakultas", "jenis": "Tempat / Ruangan"},
    "Gedung Undagi Graha [Fakultas]": {"nama": "Gedung Undagi Graha", "tingkat": "Fakultas", "jenis": "Tempat / Ruangan"},
    "Sofa Fakultas [Fakultas]": {"nama": "Sofa Fakultas", "tingkat": "Fakultas", "jenis": "Barang / Inventaris"},
    "Mixer Fakultas [Fakultas]": {"nama": "Mixer Fakultas", "tingkat": "Fakultas", "jenis": "Barang / Inventaris"},
    
    # Universitas
    "Aula Nusantara [Universitas]": {"nama": "Aula Nusantara", "tingkat": "Universitas", "jenis": "Tempat / Ruangan"},
    
    # Prodi
    "Aula Suastika [Prodi]": {"nama": "Aula Suastika", "tingkat": "Prodi", "jenis": "Tempat / Ruangan"},
    "Ruang TI 101 [Prodi]": {"nama": "Ruang TI 101", "tingkat": "Prodi", "jenis": "Tempat / Ruangan"},
    "Proyektor Prodi [Prodi]": {"nama": "Proyektor Prodi", "tingkat": "Prodi", "jenis": "Barang / Inventaris"},
    "Kabel HDMI Prodi [Prodi]": {"nama": "Kabel HDMI Prodi", "tingkat": "Prodi", "jenis": "Barang / Inventaris"}
}

# MESIN INFERENSI (FORWARD CHAINING)
def run_forward_chaining(kategori, items_terpilih_label):
    log_aturan = []
    
    # Extract nama bersih dan tingkatan
    items_nama = [ITEM_INFO_MAP[item]["nama"] for item in items_terpilih_label]
    tingkat_set = {ITEM_INFO_MAP[item]["tingkat"] for item in items_terpilih_label}

    # Validasi 1 Tingkatan
    if len(tingkat_set) > 1:
        return None, ["⚠️ ERROR: Item yang dipilih berasal dari tingkatan yang berbeda! Harap pilih item dari tingkatan kewenangan yang sama."]
    
    tingkat_terpilih = list(tingkat_set)[0]
    
    # Phase 1: Penentuan Tingkat Birokrasi (R1 - R3)
    if tingkat_terpilih == "Fakultas":
        log_aturan.append(f"Aturan R1 Terpicu: Item {items_nama} berada di bawah wewenang Fakultas")
    elif tingkat_terpilih == "Universitas":
        log_aturan.append(f"Aturan R2 Terpicu: Item {items_nama} berada di bawah wewenang Universitas")
    elif tingkat_terpilih == "Prodi":
        log_aturan.append(f"Aturan R3 Terpicu: Item {items_nama} berada di bawah wewenang Prodi")

    working_memory = {
        'kategori': kategori,
        'items': items_nama,
        'tingkat': tingkat_terpilih
    }

    # Phase 2: Penentuan Alur Surat (R4 - R6)
    if tingkat_terpilih == "Prodi":
        working_memory['alur'] = "Himpunan ➔ Koprodi"
        log_aturan.append("Aturan R4 Terpicu: Alur surat diproses hingga Koprodi")
    elif tingkat_terpilih == "Fakultas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2"
        log_aturan.append("Aturan R5 Terpicu: Alur surat diproses hingga Dekanat/WD2")
    elif tingkat_terpilih == "Universitas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2 ➔ Biro Umum"
        log_aturan.append("Aturan R6 Terpicu: Alur surat diproses hingga Biro Umum")

    # Phase 3: Penentuan Lampiran (R7 - R8)
    if "Barang / Inventaris" in kategori and "Tempat / Ruangan" in kategori:
        working_memory['lampiran'] = ["Rundown Acara", "Daftar Detail Barang yang Dipinjam", "Daftar Ruangan yang Dipinjam"]
        log_aturan.append("Aturan R7 & R8 Terpicu: Membutuhkan Rundown, Detail Barang, dan Detail Ruangan")
    elif "Barang / Inventaris" in kategori:
        working_memory['lampiran'] = ["Rundown Acara", "Daftar Detail Barang yang Dipinjam"]
        log_aturan.append("Aturan R7 Terpicu: Kategori Barang membutuhkan Rundown & Detail Barang")
    else:
        working_memory['lampiran'] = ["Rundown Acara", "Daftar Ruangan yang Dipinjam"]
        log_aturan.append("Aturan R8 Terpicu: Kategori Tempat membutuhkan Rundown & Daftar Ruangan")

    return working_memory, log_aturan

# ==========================================
# TAB 1: DEMO APLIKASI INTERAKTIF
# ==========================================
with tab1:
    kategori_pilihan = st.multiselect(
        "1. Pilih Kategori Peminjaman (Bisa pilih keduanya):", 
        ["Tempat / Ruangan", "Barang / Inventaris"],
        default=["Tempat / Ruangan"]
    )

    # Filter daftar item berdasarkan kategori yang dipilih
    opsi_item = [
        label for label, info in ITEM_INFO_MAP.items() 
        if info["jenis"] in kategori_pilihan
    ]

    items_terpilih = st.multiselect(
        "2. Pilih Item (Bisa lebih dari 1, wajib 1 tingkatan):", 
        opsi_item
    )

    btn_proses = st.button("🔍 Analisis Alur & Syarat", type="primary", use_container_width=True)

    if btn_proses:
        if not items_terpilih:
            st.warning("⚠️ Silakan pilih minimal 1 item terlebih dahulu!")
        else:
            working_memory, log_aturan = run_forward_chaining(kategori_pilihan, items_terpilih)

            if working_memory is None:
                st.error(log_aturan[0])
            else:
                st.divider()
                st.success("✅ Analisis Berhasil Dilakukan!")
                st.info(f"**Tingkat Kewenangan:** {working_memory.get('tingkat')}")
                st.markdown(f"**📍 Alur Pengajuan Surat:**\n### {working_memory.get('alur')}")
                
                st.markdown("**📄 Checklist Berkas Lampiran Wajib:**")
                for doc in working_memory.get('lampiran', []):
                    st.checkbox(doc, value=True, disabled=True)

                with st.expander("⚙️ Lihat Log Penalaran (Forward Chaining)"):
                    st.write("Fakta awal yang dimasukkan:", working_memory)
                    st.write("Aturan yang terpicu secara berurutan:")
                    for log in log_aturan:
                        st.code(log, language="text")

# ==========================================
# TAB 2: BACKWARD CHAINING, CF, & LIMITATIONS
# ==========================================
with tab2:
    st.header("🌲 1. Pohon Backward Chaining (Goal-Driven)")
    st.write("Backward Chaining bekerja secara terbalik, yaitu dari **Goal (Tujuan/Hipotesis Akhir)** menuju **Fakta Awal**.")

    st.markdown("""
    **Struktur Pohon Pembuktian:**

    - **GOAL UTAMA:** `Alur Birokrasi Surat Terkonfirmasi?`
    - **SUB-GOAL 1:** Membuktikan `Tingkat Kewenangan`
        - *Misal Hipotesis:* `Tingkat = Fakultas`
        - **Aturan R1:** Membutuhkan `Item` = "Aula Wiswakarma" / "Gedung Undagi Graha" / "Sofa Fakultas" / "Mixer Fakultas"
        - **Cek Fakta Awal:** Apakah pengguna memilih salah satu item tersebut? $\\rightarrow$ **YA (Terbukti)**

    - **SUB-GOAL 2:** Membuktikan `Alur Pengajuan`
        - **Aturan R5:** `IF` Tingkat = Fakultas `THEN` Alur = "Himpunan $\\rightarrow$ Koprodi $\\rightarrow$ Dekanat/WD2"
        - **Cek Fakta:** `Tingkat = Fakultas` sudah terbukti di SUB-GOAL 1 $\\rightarrow$ **YA (Terbukti)**

    - **SUB-GOAL 3:** Membuktikan `Persyaratan Lampiran`
        - **Aturan R8:** `IF` Kategori = Tempat / Ruangan `THEN` Lampiran = "Rundown Acara + Daftar Ruangan"
        - **Cek Fakta Awal:** Apakah pengguna memilih kategori "Tempat / Ruangan"? $\\rightarrow$ **YA (Terbukti)**

    **Kesimpulan Backward Chaining:** Goal `Alur Birokrasi Surat Terkonfirmasi` berhasil dibuktikan secara berantai dari bawah ke atas (*bottom-up verification*).
    """)

    st.divider()

    st.header("🧮 2. Perhitungan Certainty Factor (CF)")
    st.write("Misalkan pada aturan penentuan tingkat birokrasi (R1):")

    st.markdown("""
    - **CF Pengguna / Fakta 1** ($CF(E_1)$) = $0.80$ (Tingkat keyakinan pengguna bahwa ruangan sedang kosong/dapat dipinjam)
    - **CF Pengguna / Fakta 2** ($CF(E_2)$) = $0.90$ (Tingkat keyakinan keberadaan penanggung jawab tempat)
    - **CF Aturan Pakar** ($CF_{aturan}$) = $0.85$ (Kekuatan aturan pakar)

    **Langkah Perhitungan:**
    1. **Kombinasi Premis (Operasi AND):**
       $$CF_{premis} = \\min(CF(E_1); CF(E_2)) = \\min(0.80; 0.90) = 0.80$$

    2. **Perhitungan CF Kesimpulan Tunggal:**
       $$CF_{hipotesis} = CF_{premis} \\times CF_{aturan} = 0.80 \\times 0.85 = 0.68$$

    **Hasil Akhir:** Tingkat keyakinan (*Certainty Factor*) sistem terhadap rekomendasi birokrasi tersebut adalah **$0.68$** atau **$68\\%$**.
    """)

    st.divider()

    st.header("⚠️ 3. Batas Kesimpulan Sistem (Limitations)")
    st.markdown("""
    Sistem pakar berbasis aturan *Forward/Backward Chaining* ini memiliki beberapa keterbatasan utama:

    - **Sifat Aturan yang Kaku (*Rigid Rules*):** Sistem hanya dapat mengambil keputusan dari daftar aturan (*Rule Base*) R1–R8 yang telah terprogram. Jika pengguna memasukkan item/lokasi di luar basis pengetahuan, sistem tidak dapat memberikan rekomendasi.
    - **Tidak Mempertimbangkan Jadwal Bentrok (*Real-Time Availability*):** Sistem hanya menyimpulkan **alur birokrasi dan syarat surat**, namun tidak mengetahui apakah pada tanggal tersebut ruangan/barang sebenarnya sudah dibooking oleh organisasi lain.
    - **Penanganan Ketidakpastian yang Terbatas:** Tanpa integrasi algoritma *Fuzzy Logic* atau *Bayes*, sistem menganggap status tempat/barang bernilai mutlak (tersedia atau tidak), sehingga tidak fleksibel terhadap kondisi khusus (seperti izin lisan mendadak dari dekan/pejabat).
    """)