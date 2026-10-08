## **STUDI KASUS & METODE PENALARAN**

#### **1. Ringkasan Studi Kasus**
Sekretaris organisasi mahasiswa sering mengalami penolakan atau keterlambatan izin akibat ketidakjelasan alur birokrasi dan ketidaklengkapan dokumen lampiran surat.

#### **2. Mengapa Memakai Forward Chaining?**
Metode Forward Chaining digunakan karena sistem secara otomatis mencocokkan fakta awal (lokasi/skala acara) maju ke depan hingga menghasilkan kesimpulan alur dan syarat surat.

#### 3. Basis Aturan (Rule Base R1 - R9)

| Rule ID | Kondisi (IF) | Kesimpulan / Fakta Baru (THEN) |
| :--- | :--- | :--- |
| **R1** | Item = "Aula Wiswakarma" **OR** "Gedung Undagi Graha" **OR** "Sofa Fakultas" **OR** "Mixer Fakultas" | Tingkat = "Fakultas" |
| **R2** | Item = "Aula Nusantara" | Tingkat = "Universitas" |
| **R3** | Item = "Aula Suastika" **OR** "Ruang TI 101" **OR** "Proyektor Prodi" **OR** "Kabel HDMI Prodi" | Tingkat = "Prodi" |
| **R4** | Tingkat = "Prodi" | Alur = "Himpunan ➔ Koprodi" |
| **R5** | Tingkat = "Fakultas" | Alur = "Himpunan ➔ Koprodi ➔ Dekanat/WD2" |
| **R6** | Tingkat = "Universitas" | Alur = "Himpunan ➔ Koprodi ➔ Dekanat/WD2 ➔ Biro Umum" |
| **R7** | Kategori = "Barang / Inventaris" | Lampiran = "Rundown Acara + Daftar Detail Barang yang Dipinjam" |
| **R8** | Kategori = "Tempat / Ruangan" | Lampiran = "Rundown Acara + Daftar Ruangan yang Dipinjam" |