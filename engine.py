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

# MESIN INFERENSI FORWARD CHAINING
def run_forward_chaining(kategori, items_terpilih_label):
    log_aturan = []
    
    items_nama = [ITEM_INFO_MAP[item]["nama"] for item in items_terpilih_label]
    tingkat_set = {ITEM_INFO_MAP[item]["tingkat"] for item in items_terpilih_label}

    if len(tingkat_set) > 1:
        return None, ["⚠️ ERROR: Item yang dipilih berasal dari tingkatan yang berbeda! Harap pilih item dari tingkatan kewenangan yang sama."]
    
    tingkat_terpilih = list(tingkat_set)[0]
    
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

    if tingkat_terpilih == "Prodi":
        working_memory['alur'] = "Himpunan ➔ Koprodi"
        log_aturan.append("Aturan R4 Terpicu: Alur surat diproses hingga Koprodi")
    elif tingkat_terpilih == "Fakultas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2"
        log_aturan.append("Aturan R5 Terpicu: Alur surat diproses hingga Dekanat/WD2")
    elif tingkat_terpilih == "Universitas":
        working_memory['alur'] = "Himpunan ➔ Koprodi ➔ Dekanat/WD2 ➔ Biro Umum"
        log_aturan.append("Aturan R6 Terpicu: Alur surat diproses hingga Biro Umum")

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


# GENERATOR TEKS HIPOTESIS BACKWARD CHAINING
def generate_backward_chaining_hypothesis(tingkat, items_str):
    hipotesis_text = ""
    
    # 1. Uji Hipotesis Prodi (R3)
    if tingkat == "Prodi":
        hipotesis_text += f"1. ✅ **Pengujian Hipotesis 1:** `Tingkat = Prodi`\n"
        hipotesis_text += f"   - *Cek Aturan R3:* Membutuhkan item prodi (Aula Suastika, Ruang TI 101, Proyektor Prodi, Kabel HDMI).\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TERBUKTI COCOK! (Hipotesis Diterima)**.\n\n"
    else:
        hipotesis_text += f"1. ❌ **Pengujian Hipotesis 1:** `Tingkat = Prodi`\n"
        hipotesis_text += f"   - *Cek Aturan R3:* Membutuhkan item prodi.\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TIDAK COCOK (Hipotesis Ditolak)**.\n\n"

    # 2. Uji Hipotesis Fakultas (R1)
    if tingkat == "Fakultas":
        hipotesis_text += f"2. ✅ **Pengujian Hipotesis 2:** `Tingkat = Fakultas`\n"
        hipotesis_text += f"   - *Cek Aturan R1:* Membutuhkan item fakultas (Aula Wiswakarma, Gedung Undagi Graha, Sofa, Mixer).\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TERBUKTI COCOK! (Hipotesis Diterima)**.\n\n"
    else:
        hipotesis_text += f"2. ❌ **Pengujian Hipotesis 2:** `Tingkat = Fakultas`\n"
        hipotesis_text += f"   - *Cek Aturan R1:* Membutuhkan item fakultas.\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TIDAK COCOK (Hipotesis Ditolak)**.\n\n"

    # 3. Uji Hipotesis Universitas (R2)
    if tingkat == "Universitas":
        hipotesis_text += f"3. ✅ **Pengujian Hipotesis 3:** `Tingkat = Universitas`\n"
        hipotesis_text += f"   - *Cek Aturan R2:* Membutuhkan item universitas (Aula Nusantara).\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TERBUKTI COCOK! (Hipotesis Diterima)**.\n\n"
    else:
        hipotesis_text += f"3. ❌ **Pengujian Hipotesis 3:** `Tingkat = Universitas`\n"
        hipotesis_text += f"   - *Cek Aturan R2:* Membutuhkan item universitas.\n"
        hipotesis_text += f"   - *Cek Fakta Input:* User memilih `{items_str}`.\n"
        hipotesis_text += f"   - *Hasil:* **TIDAK COCOK (Hipotesis Ditolak)**.\n\n"

    return hipotesis_text