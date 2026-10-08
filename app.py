import streamlit as st
from engine import ITEM_INFO_MAP, run_forward_chaining, generate_backward_chaining_hypothesis

st.set_page_config(page_title="Sistem Pakar Birokrasi Surat", page_icon="📝", layout="centered")

st.title("📝 Sistem Pakar Penentuan Alur Surat & Disposisi")
st.markdown("Aplikasi membantu **Sekretaris Organisasi** menentukan alur pengajuan surat dan berkas lampiran dengan **Forward Chaining**.")

# MEMBUAT TABS UNTUK MEMISAHKAN APLIKASI UTAMA DAN TEORI/BACKWARD CHAINING
tab1, tab2 = st.tabs(["🚀 Demo Sistem (Forward Chaining)", "🌲 Backward Chaining & Teori CF"])

# Inisialisasi Session State
if 'working_memory' not in st.session_state:
    st.session_state.working_memory = None

# TAB 1: DEMO APLIKASI INTERAKTIF
with tab1:
    kategori_pilihan = st.multiselect(
        "1. Pilih Kategori Peminjaman (Bisa pilih keduanya):", 
        ["Tempat / Ruangan", "Barang / Inventaris"],
        default=["Tempat / Ruangan"]
    )

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
            st.session_state.working_memory = None
        else:
            wm, log_at = run_forward_chaining(kategori_pilihan, items_terpilih)
            if wm is None:
                st.error(log_at[0])
                st.session_state.working_memory = None
            else:
                st.session_state.working_memory = wm
                st.session_state.log_aturan = log_at

    if st.session_state.working_memory is not None:
        wm = st.session_state.working_memory
        st.divider()
        st.success("✅ Analisis Berhasil Dilakukan!")
        st.info(f"**Tingkat Kewenangan:** {wm.get('tingkat')}")
        st.markdown(f"**📍 Alur Pengajuan Surat:**\n### {wm.get('alur')}")
        
        st.markdown("**📄 Checklist Berkas Lampiran Wajib:**")
        for doc in wm.get('lampiran', []):
            st.checkbox(doc, value=True, disabled=True)

        with st.expander("⚙️ Lihat Log Penalaran (Forward Chaining)"):
            st.write("Fakta awal yang dimasukkan:", wm)
            st.write("Aturan yang terpicu secara berurutan:")
            for log in st.session_state.log_aturan:
                st.code(log, language="text")

# TAB 2: BACKWARD CHAINING, CF, & LIMITATIONS
with tab2:
    st.header("🌲 1. Pohon Backward Chaining Dinamis (Goal-Driven)")
    
    if st.session_state.working_memory is None:
        st.info("💡 **Silakan lakukan analisis di Tab 1 terlebih dahulu** untuk melihat Diagram Pohon Pembuktian Backward Chaining secara dinamis berdasarkan pilihanmu!")
    else:
        wm = st.session_state.working_memory
        items_str = ", ".join(wm['items'])
        tingkat = wm['tingkat']
        alur = wm['alur']
        lampiran_str = " + ".join(wm['lampiran'])

        st.markdown(f"**Pembuktian Hipotesis untuk Pilihan Pengguna:** `{items_str}`")

        # DIAGRAM POHON VISUAL (GRAPHVIZ)
        dot_code = f"""
        digraph G {{
            rankdir=BT;
            node [shape=box, style="filled,rounded", fontname="sans-serif", fontsize=10];
            
            Fakta1 [label="Fakta 1:\\nItem Terpilih", fillcolor="#e1f5fe"];
            Fakta2 [label="Fakta 2:\\nKategori Terpilih", fillcolor="#e1f5fe"];
            
            Sub1 [label="Sub-Goal 1:\\nTingkat = {tingkat}", fillcolor="#fff9c4"];
            Sub2 [label="Sub-Goal 2:\\nAlur Birokrasi", fillcolor="#fff9c4"];
            Sub3 [label="Sub-Goal 3:\\nBerkas Lampiran", fillcolor="#fff9c4"];
            
            Goal [label="GOAL UTAMA:\\nAlur & Berkas Surat Terkonfirmasi", fillcolor="#c8e6c9", shape=doubleoctagon];
            
            Fakta1 -> Sub1 [label="Terbukti dari Item"];
            Sub1 -> Sub2 [label="Memicu Alur"];
            Fakta2 -> Sub3 [label="Memicu Lampiran"];
            
            Sub2 -> Goal;
            Sub3 -> Goal;
        }}
        """
        st.graphviz_chart(dot_code)

        # MEMANGGIL TEKS HIPOTESIS DARI ENGINE
        hipotesis_text = generate_backward_chaining_hypothesis(tingkat, items_str)

        st.markdown("### 🔍 Proses Pencarian & Eliminasi Hipotesis (Goal-Driven):")
        st.write("Sistem menguji daftar hipotesis secara berurutan dari tingkat terendah hingga menemukan hipotesis yang cocok dengan fakta:")
        st.markdown(hipotesis_text)

        st.divider()

        st.markdown(f"""### 📋 Langkah Pembuktian Terbalik (Bottom-Up Verification):
1. **Goal Utama:** Membuktikan apakah rekomendasi alur & berkas surat dapat diterbitkan?
2. **Membuktikan Sub-Goal 1 (Tingkat Kewenangan):**
   - Terbukti **Tingkat = {tingkat}** berdasarkan hasil pengujian hipotesis di atas.
3. **Membuktikan Sub-Goal 2 (Alur Birokrasi):**
   - Cek Aturan: Karena Tingkat terbukti **{tingkat}**, alur surat ditetapkan ke: `{alur}`.
4. **Membuktikan Sub-Goal 3 (Syarat Lampiran):**
   - Cek Aturan: Berdasarkan Kategori yang dipilih, lampiran wajib adalah `{lampiran_str}`.
5. **Kesimpulan:** Goal utama **BERHASIL TERBUKTI**.
""")

    st.divider()

    st.header("🧮 2. Simulasi & Perhitungan Certainty Factor (CF)")
    st.write("Certainty Factor (CF) digunakan untuk mengukur tingkat kepastian/keyakinan sistem terhadap rekomendasi yang diberikan.")

    # Skenario Interaktif Slider CF
    col1, col2 = st.columns(2)
    with col1:
        cf_e1 = st.slider("1. Keyakinan Ketersediaan Tempat/Barang (CF User 1)", 0.0, 1.0, 0.80, 0.05)
        cf_e2 = st.slider("2. Keyakinan Adanya Penanggung Jawab (CF User 2)", 0.0, 1.0, 0.90, 0.05)
    with col2:
        cf_rule = st.slider("3. Kekuatan Aturan Pakar (CF Aturan)", 0.0, 1.0, 0.85, 0.05)

    # PERHITUNGAN STEP-BY-STEP
    cf_premis = min(cf_e1, cf_e2)
    cf_akhir = cf_premis * cf_rule

    st.subheader("Langkah Perhitungan Sederhana:")
    st.markdown(f"""
    * **Langkah 1 (Kombinasi Kondisi Input dengan Operasi AND):**  
      Ambil nilai terkecil (*minimum*) dari keyakinan user:  
      $$\\text{{CF}}_{{\\text{{premis}}}} = \\min({cf_e1:.2f}, {cf_e2:.2f}) = {cf_premis:.2f}$$

    * **Langkah 2 (Kalikan dengan Bobot Aturan Pakar):**  
      $$\\text{{CF}}_{{\\text{{akhir}}}} = \\text{{CF}}_{{\\text{{premis}}}} \\times \\text{{CF}}_{{\\text{{aturan}}}}$$  
      $$\\text{{CF}}_{{\\text{{akhir}}}} = {cf_premis:.2f} \\times {cf_rule:.2f} = \\mathbf{{{cf_akhir:.4f}}}$$
    """)

    st.success(f"🎯 **Hasil Akhir Certainty Factor:** `{cf_akhir:.4f}` atau **`{cf_akhir*100:.1f}%`** keyakinan bahwa alur surat ini siap diajukan.")

    st.divider()

    st.header("⚠️ 3. Batas Kesimpulan Sistem (Limitations)")
    st.markdown("""
    Sistem pakar berbasis aturan *Forward/Backward Chaining* ini memiliki beberapa keterbatasan utama:

    * Sistem hanya dapat mengambil keputusan dari daftar aturan (*Rule Base*) R1–R8 yang telah terprogram.
    * Tidak Mempertimbangkan Jadwal Bentrok
    """)