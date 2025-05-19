Judul Proyek: Sistem Deteksi Plat Kendaraan Genap Ganjil
<br>Link Dataset: https://universe.roboflow.com/smartproject/deteksi-lisensi-plat 
<br>Link PPT Canva: https://www.canva.com/design/DAGmFxCjSLA/lAMJdL2S9gwEHipRu3azxA/edit?utm_content=DAGmFxCjSLA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton 

Aturan genap ganjil merupakan salah satu kebijakan yang diterapkan oleh Pemerintah Provinsi DKI Jakarta untuk mengurangi kemacetan dan menurunkan polusi di jalan-jalan utama kota Jakarta. Kebijakan ini mulai diberlakukan pada tahun 2016 dan diberlakukan secara bergiliran berdasarkan nomor plat kendaraan.

Tujuan Sistem
<ul>
  <li>Deteksi Pelanggaran: Menangkap plat kendaraan yang melanggar aturan genap ganjil (misalnya, kendaraan dengan plat ganjil yang melintas pada hari genap).</li>
  <li>Database Pelanggaran: Mencatat kendaraan yang melanggar dalam sebuah database, termasuk plat nomor, tanggal, waktu, dan lokasi pelanggaran.</li>
  <li>Pemantauan Real-time: Sistem bisa digunakan dengan kamera pemantauan di jalan raya atau titik pemeriksaan tertentu.</li>
</ul>

<h1>Langkah Pengembangan Sistem</h1>
Kebutuhan Data Sistem
<ol>
  <li>Dataset Plat Nomor</li>
  Link Dataset	: https://universe.roboflow.com/smartproject/deteksi-lisensi-plat 
  <li>Data Hari Genap Ganjil</li>
  Prinsip Dasar Aturan Genap Ganjil
  <ul>
    <li>Kendaraan dengan plat nomor ganjil hanya diperbolehkan untuk melintas di Jakarta pada hari ganjil (misalnya, tanggal 1, 3, 5, 7, dst.)</li>
    <li>Kendaraan dengan plat nomor genap hanya diperbolehkan untuk melintas di Jakarta pada hari genap (misalnya, tanggal 2, 4, 6, 8, dst.)</li>
  </ul>
  <li>Waktu Pemberlakuan</li>
  Aturan ini diberlakukan pada jam-jam puncak di hari kerja, yaitu:
  <ul>
    <li>Pagi	: 06.00 - 10.00 WIB</li>
    <li>Sore	: 16.00 - 20.00 WIB</li>
    Di luar jam tersebut, kendaraan bebas melintas di wilayah tersebut tanpa menghiraukan aturan plat nomor genap ganjil
  </ul>
</ol>

Proses
<ul>
  <li>Ambil digit terakhir dari nomor plat.</li>
  <li>Tentukan hari (apakah genap atau ganjil).</li>
  <li>Bandingkan apakah kendaraan yang memiliki plat nomor ganjil melintas pada hari genap, atau sebaliknya.</li>
</ul>

Database Pelanggaran
<ul>
  <li>Plat nomor kendaraan.</li>
  <li>Tanggal dan waktu pelanggaran.</li>
  <li>Lokasi (bisa dengan koordinat GPS dari kamera).</li>
</ul>

Tantangan
<ul>
  <li>Kualitas Gambar: Pencahayaan atau cuaca yang buruk dapat mempengaruhi akurasi pembacaan plat nomor.</li>
  <li>Kecepatan Deteksi: Sistem harus cukup cepat untuk memproses gambar dalam waktu nyata, terutama dengan volume kendaraan yang tinggi.</li>
  <li>Akurasi OCR: OCR harus cukup kuat untuk membaca plat nomor dengan jelas, meskipun ada gangguan atau distorsi pada gambar.</li>
</ul>

