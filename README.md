# Oleh Bali

### Link Deployment : [Oleh Bali](http://ezar-akhdan-olehbali.pbp.cs.ui.ac.id/ 'Oleh Bali Website')

<details>
<summary>Anggota Kelompok B11</summary>

- Yemima Clara Nainggolan (2306245825)
- Nabilah Devina Mu'min (2306245876)
- Rogerio Geraldo Wibhowo (2306245623)
- Ezar Akhdan Shada Surahman (2306165894)
- Alya Rasheeda Yuvana (2306165641)
</details>

<details>
<summary>Oleh Bali at a glance..</summary>
OlehBali: Dari Bali, Bawa Pulang Pesona Bali

Bali selalu menjadi tujuan wisata favorit, baik bagi wisatawan lokal maupun mancanegara. Selain pantai dan pemandangannya yang menawan, Bali juga dikenal dengan kerajinan tangan dan produk khasnya yang menarik. Namun, tidak jarang wisatawan merasa kesulitan untuk menemukan souvenir yang autentik dan terjangkau di tengah banyaknya pilihan yang tersedia. OlehBali hadir untuk menjawab kebutuhan ini.

OlehBali adalah platform digital yang mempermudah wisatawan dalam menemukan dan membeli oleh-oleh khas Bali. Melalui fitur-fitur yang user-friendly, wisatawan dapat menelusuri berbagai pilihan souvenir yang dihasilkan langsung oleh pengrajin lokal. Dengan begitu, setiap produk yang ditawarkan bukan hanya barang, tapi juga mencerminkan nilai budaya dan tradisi Bali.

Beberapa fitur utama dari OlehBali adalah:
- Penjual: Penjual bisa menambahkan produk ke tokonya, mengedit harga, dan mengelola profil toko. Halaman My Products memungkinkan penjual untuk melihat dan mengedit produk, serta menambah atau menghapus produk.
- Profil dan Manajemen Toko: Pembeli bisa mengedit profil (foto, nama, kewarganegaraan). Penjual bisa mengedit informasi toko (foto, nama, alamat, lokasi). Pembeli dapat mencari toko dan memfilter berdasarkan lokasi (kecamatan/kelurahan).
- Katalog Produk (Pembeli): Pembeli bisa mencari dan memfilter produk berdasarkan harga, kategori, dan jumlah like. Setiap produk memiliki halaman detail dengan opsi like, wishlist, dan review.
Wishlist: Pembeli bisa menambah produk ke wishlist, melihat total harga range dari item wishlist, dan menghapus item yang tidak diinginkan.
- Review dan Like: Pembeli bisa memberikan like pada produk dan menulis review. Review akan ditampilkan dengan foto dan username, sementara like bisa digunakan sebagai filter katalog.

OlehBali memberikan manfaat nyata bagi dan pengrajin lokal Bali. Bagi wisatawan, platform ini memudahkan penelusuran dan pembelian souvenir autentik dengan harga yang transparan, sehingga mereka bisa membawa pulang oleh-oleh khas tanpa khawatir dengan harga yang berlebihan. Di sisi lain, pengrajin lokal mendapatkan eksposur lebih luas, memungkinkan produk mereka dikenal oleh pasar yang lebih besar. Dengan ini, OlehBali tidak hanya memfasilitasi transaksi, tetapi juga mendukung keberlangsungan ekonomi kreatif di Bali dan melestarikan warisan budaya melalui karya seni lokal.

</details>

<details>
<summary>Daftar Modul yang akan diimplementasikan</summary>
Berikut daftar modul yang akan kami gunakan dalam website OlehBali:
    - Penjual
        Dikerjakan oleh **Yemima Clara Nainggolan**, modul ini berfokus pada role user yaitu penjual yang dapat menambahkan produk untuk tokonya, penjual bisa memilih bisa menambahkan produk yang sudah ada di dataset ataupun menambahkan produknya sendiri.

        Modul ini juga menghandle halaman tersendiri yaitu halaman `My Products` yang dapat menampilkan produk-produk milik penjual. Di halaman ini penjual juga bisa mengedit harga serta menghapus produk yang tidak ingin ia jual lagi. Di halaman ini juga terdapat fitur `Add Product`, penjual bisa memilih antara button `Add New Product` dan button `Add Existing Product`. Jika button tersebut ditekan, akan menuju ke tampilan form yang berbeda. Setelah produk diadd, produk tersebut akan ditambahkan ke halaman `My Products`  dan otomatis memiliki "toko" tersebut di dalam attributenya.
    
    - User Profile + Profile Toko
        Dikerjakan oleh **Nabilah Devina Mu'min**, modul ini berurusan dengan edit profile pengguna dan penjual. Pada modul ini memiliki halaman edit profile yang dapat mengubah foto profil, display name, dan kewarganegaraan untuk pembeli dan edit details seperti logo, nama toko, kecamatan, kelurahan, nama jalan, dan link Google Maps toko bagi penjual.

        Pada modul ini juga terdapat halaman `lihat toko` untuk melihat pada satu toko menjual produk apasaja atau bisa dibilang profille suatu toko secara keseluruhan.

    - Katalog Produk
        Dikerjakan oleh **Ezar Akhdan Shada Surahman**, katalog produk akan menampilkan semua produk yang ada pada halaman katalog. Pada modul ini juga terdapat filter yang bisa menampilkan produk berdasarkan harga, kategori, dan like pada produk. Pengguna juga dapat mencari produk lewat `search bar` berdasarkan kata kunci.

        Saat suatu produk diklik, halaman akan menampilkan product details yang menyajikan produk secara lebih detail seperti kategori, nama, deskkripsi serta toko-toko yang menjual produk tersebut.

    - Wishlist + Katalog Toko
        Dikerjakan oleh **Alya Rasheeda Yuvana**, modul ini berfungsi untuk menambahkan suatu produk yang disukai oleh pelanggan ke halaman `My Wishlist`. Di setiap produk akan ada tombol untuk menambahkan produk tersebut ke dalam wishlist. Di halaman wishlist, pengguna bisa melihat semua produk yang dia masukkan ke dalam wishlist, menghapus produk dari wishlist, dan melihat total harga semua produk yang ada dalam wishlistnya.

        Katalog toko pada modul ini digunakan pembeli untuk melihat toko apa saja yang menjual satu produk. Misalnya, melihat toko apa saya yang menjual produk Pie Susu Bali.

    - Review + Like
        Dikerjakan oleh **Rogerio Geraldo Wibhowo**, modul ini bisa membuat pengguna mlakukan like kepada suatu produk, lalu total like pada produk tersebut akan ditampilkan pada card product. Like juga bisa dijadikan filter (sort) di dalam katalog produk.

        Di setiap product details akan ada section review produk yang akan menampilkan review-review dari produk tersebut, dan pengguna juga bisa menambahkan review untk produk tersebut. Display name dan foto profil pengguna akan terlihat jika menambahkan review ke suatu produk.
</details>

<details>
<summary>📊 Initial Dataset</summary>
Dataset diambil dari berbagai website, yaitu:

- [Oleh Bali](http://ezar-akhdan-olehbali.pbp.cs.ui.ac.id/ 'Oleh Bali Website')
- [Wonderful Indonesia](https://www.indonesia.travel/)
- [Travel Passionate](https://travelpassionate.com/)
- [Balipedia](https://balipedia.com/)
- [The Culture Trip](https://theculturetrip.com/)
- [Autentic Indonesia](https://authentic-indonesia.com/blog/10-best-indonesia-souvenirs-gifts/)
- [Laure Wanders](https://www.laurewanders.com/souvenirs-from-indonesia/)
- [Living Nomads](https://livingnomads.com/2024/04/what-to-buy-in-indonesia/)
- [Indonesia Tours](https://www.goindonesiatours.com/indonesia-souvenirs-top-10-souvenirs-buy-indonesia/)
- Google (untuk mencari image)
</details>

<details>
<summary>🧑‍💼 Role</summary>

🧑‍💼💰 **Penjual**
- Melihat _homepage_ yang berisi _product-product_ yang dijual.
- Menambahkan _product_ baru pada toko.
- Mengedit harga _product_ yang dijual.
- Menghapus _product_ yang tidak ingin dijual lagi.
- Mengedit logo toko, _display name_, kota, kecamatan, kelurahan, jalan, dan lokasi pada profil toko.

🧑‍💻🔓 **User Terautentikasi**
- Melihat _homepage_ yang berisi _souvenirs_ dan _wishlist_.
- Melakukan pencarian _product_ dengan filter berdasarkan harga, kategori, dan lokasi.
- Melakukan _sort_ pada product berdasarkan _like_ terbanyak.
- Melihat katalog berisi nama-nama _souvenir_ yang tersedia.
- Melihat _product details_ yang berisi kategori _product_, nama _product_, deskripsi _product_, beserta harga _product_.
- Melakukan _like_ atau _dislike_ pada _product card_.
- Menjadikan _wishlist_ suatu _product_.
- Menghapus suatu _product_ dari _wishlist_.
- Menambahkan _review_ pada suatu _product_.
- Melihat nama-nama toko, alamat toko, serta harga dari suatu product yang sedang dicari.
- Mengedit _profile picture_, _display name_, dan _nationality_ pada laman profil pembeli.

</details>