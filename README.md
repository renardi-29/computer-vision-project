# Sistem Deteksi Plat Kendaraan Genap Ganjil

Link Dataset: [Deteksi Lisensi Plat](https://universe.roboflow.com/smartproject/deteksi-lisensi-plat)  
Link PPT Canva: [Presentasi Sistem](https://www.canva.com/design/DAGmFxCjSLA/lAMJdL2S9gwEHipRu3azxA/edit?utm_content=DAGmFxCjSLA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

Aturan genap ganjil merupakan salah satu kebijakan yang diterapkan oleh Pemerintah Provinsi DKI Jakarta untuk mengurangi kemacetan dan menurunkan polusi di jalan-jalan utama kota Jakarta. Kebijakan ini mulai diberlakukan pada tahun 2016 dan diberlakukan secara bergiliran berdasarkan nomor plat kendaraan.

## Tujuan Sistem
- **Deteksi Pelanggaran:** Menangkap plat kendaraan yang melanggar aturan genap ganjil (misalnya, kendaraan dengan plat ganjil yang melintas pada hari genap).
- **Database Pelanggaran:** Mencatat kendaraan yang melanggar dalam sebuah database, termasuk plat nomor, tanggal, waktu, dan lokasi pelanggaran.
- **Pemantauan Real-time:** Sistem bisa digunakan dengan kamera pemantauan di jalan raya atau titik pemeriksaan tertentu.

## Langkah Pengembangan Sistem

### Kebutuhan Data Sistem
1. **Dataset Plat Nomor**  
   Link Dataset: [Deteksi Lisensi Plat](https://universe.roboflow.com/smartproject/deteksi-lisensi-plat)
   
2. **Data Hari Genap Ganjil**  
   Prinsip Dasar Aturan Genap Ganjil:
   - Kendaraan dengan plat nomor ganjil hanya diperbolehkan untuk melintas di Jakarta pada hari ganjil (misalnya, tanggal 1, 3, 5, 7, dst.).
   - Kendaraan dengan plat nomor genap hanya diperbolehkan untuk melintas di Jakarta pada hari genap (misalnya, tanggal 2, 4, 6, 8, dst.).

3. **Waktu Pemberlakuan**  
   Aturan ini diberlakukan pada jam-jam puncak di hari kerja, yaitu:
   - **Pagi:** 06.00 - 10.00 WIB
   - **Sore:** 16.00 - 20.00 WIB  
   Di luar jam tersebut, kendaraan bebas melintas di wilayah tersebut tanpa menghiraukan aturan plat nomor genap ganjil.

### Proses
1. Ambil digit terakhir dari nomor plat.
2. Tentukan hari (apakah genap atau ganjil).
3. Bandingkan apakah kendaraan yang memiliki plat nomor ganjil melintas pada hari genap, atau sebaliknya.

### Database Pelanggaran
- Plat nomor kendaraan.
- Tanggal dan waktu pelanggaran.
- Lokasi (bisa dengan koordinat GPS dari kamera).

## Tantangan
- **Kualitas Gambar:** Pencahayaan atau cuaca yang buruk dapat mempengaruhi akurasi pembacaan plat nomor.
- **Kecepatan Deteksi:** Sistem harus cukup cepat untuk memproses gambar dalam waktu nyata, terutama dengan volume kendaraan yang tinggi.
- **Akurasi OCR:** OCR harus cukup kuat untuk membaca plat nomor dengan jelas, meskipun ada gangguan atau distorsi pada gambar.
