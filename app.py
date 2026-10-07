import streamlit as st

st.set_page_config(page_title="Sistem Pakar Birokrasi Surat", page_icon="📝", layout="centered")

st.title("📝 Sistem Pakar Penentuan Alur Surat & Disposisi")
st.markdown("Aplikasi membantu **Sekretaris Organisasi** menentukan alur pengajuan surat dan berkas lampiran dengan **Forward Chaining**.")

st.divider()

# MESIN INFERENSI (FORWARD CHAINING)
def run_forward_chaining(kategori, item_terpilih):
    working_memory = {'kategori': kategori, 'item': item_terpilih}
    log_aturan = []

    item = working_memory.get('item')
    if item in ["Aula Wiswakarma", "Gedung Undagi Graha", "Sofa Fakultas", "Mixer Fakultas"]:
        working_memory['tingkat'] = "Fakultas"
        log_aturan.append(f"Aturan R1 Terpicu: '{item}' berada di bawah wewenang Fakultas")
    elif item in ["Aula Nusantara"]:
        working_memory['tingkat'] = "Universitas"
        log_aturan.append(f"Aturan R2 Terpicu: '{item}' berada di bawah wewenang Universitas")
    elif item in ["Aula Suastika", "Ruang TI 101", "Proyektor Prodi", "Kabel HDMI Prodi"]:
        working_memory['tingkat'] = "Prodi"
        log_aturan.append(f"Aturan R3 Terpicu: '{item}' berada di bawah wewenang Prodi")

    tingkat = working_memory.get('tingkat')
    if tingkat == "Prodi":
        working_memory['alur'] = "Himpunan ➔ Koprodi"
        log_aturan.append("Aturan R4 Terpicu: Alur surat diproses hingga Koprodi")
    elif tingkat == "Fakultas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2"
        log_aturan.append("Aturan R5 Terpicu: Alur surat diproses hingga Dekanat/WD2")
    elif tingkat == "Universitas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2 ➔ Biro Umum"
        log_aturan.append("Aturan R6 Terpicu: Alur surat diproses hingga Biro Umum")

    kat = working_memory.get('kategori')
    if kat == "Barang / Inventaris":
        working_memory['lampiran'] = ["Rundown Acara", "Daftar Detail Barang yang Dipinjam"]
        log_aturan.append("Aturan R7 Terpicu: Kategori Barang membutuhkan Rundown & Detail Barang")
    elif kat == "Tempat / Ruangan":
        working_memory['lampiran'] = ["Rundown Acara", "Daftar Ruangan yang Dipinjam"]
        log_aturan.append("Aturan R8 Terpicu: Kategori Tempat membutuhkan Rundown & Daftar Ruangan")

    return working_memory, log_aturan

# INTERFACE STREAMLIT
kategori = st.radio("1. Pilih Kategori Peminjaman:", ["Tempat / Ruangan", "Barang / Inventaris"])

if kategori == "Tempat / Ruangan":
    item_terpilih = st.selectbox("2. Pilih Tempat / Ruangan:", [
        "Aula Wiswakarma", "Gedung Undagi Graha", "Aula Nusantara", "Aula Suastika", "Ruang TI 101"
    ])
else:
    item_terpilih = st.selectbox("2. Pilih Barang / Inventaris:", [
        "Sofa Fakultas", "Mixer Fakultas", "Proyektor Prodi", "Kabel HDMI Prodi"
    ])

btn_proses = st.button("🔍 Analisis Alur & Syarat", type="primary", use_container_width=True)

if btn_proses:
    working_memory, log_aturan = run_forward_chaining(kategori, item_terpilih)

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