### Tugas 1

1. Ya, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen tersebut membantu saya membagi halaman berdasarkan fungsi dan jenis kontennya. Sebagai contoh, `<section>` digunakan untuk memisahkan bagian Profile, Skills, Projects, dan Education, sedangkan `<article>` digunakan untuk setiap item Skills, Projects, dan Education. Dengan struktur tersebut, kode HTML menjadi lebih terorganisir, mudah dibaca, dan lebih mudah dikembangkan ketika ingin menambahkan konten baru pada static web.

2. Tantangan utama saya saat membuat website responsive adalah menyesuaikan tata letak yang awalnya menggunakan beberapa kolom pada desktop agar tetap nyaman dibaca pada layar mobile. Saya mengevaluasi elemen berdasarkan prioritas informasi dan ukuran layar. Pada bagian Hero, layout diubah dari dua kolom menjadi satu kolom agar identitas, foto, dan informasi dapat ditampilkan secara vertikal. Pada bagian Skills, jumlah dan posisi kolom juga disederhanakan agar teks tidak terlalu sempit. Pada bagian Projects, kartu project juga diubah menjadi satu kolom pada mobile. Selain itu, saya menyesuaikan ukuran judul, jarak antar elemen, dan posisi timeline Education agar tetap rapi pada layar yang lebih kecil.

3. Batasan yang saya rasakan pada static web adalah seluruh informasi masih ditulis secara langsung di dalam HTML, sehingga setiap perubahan atau penambahan data harus dilakukan secara manual pada kode. Website juga belum dapat menampilkan konten yang berubah secara otomatis berdasarkan data atau interaksi pengguna yang lebih kompleks. Pada iterasi selanjutnya, saya ingin menambahkan fungsionalitas dinamis menggunakan Django, misalnya agar data Projects dapat disimpan dan ditampilkan dari database. Dengan demikian, saya dapat menambahkan atau mengubah project tanpa harus mengubah struktur HTML secara langsung.

### Tugas 2

1. **Jelaskan alur ketika pengguna membuka halaman portofolio baru.**  
   Ketika pengguna membuka halaman Education, request dari browser pertama kali diterima oleh `portofolio/urls.py`, yang meneruskan request ke `main/urls.py` melalui `include()`. Di `main/urls.py`, URL `/education/` diarahkan ke view `show_education`. View tersebut mengambil data Education dari model `Education` menggunakan `Education.objects.all()`, lalu memasukkan data tersebut ke dalam context. Context kemudian dikirim ke template `education.html` untuk dirender menjadi HTML dan dikembalikan sebagai response kepada pengguna.

2. **Mengapa data portofolio sebaiknya disimpan dalam model, bukan langsung di-template?**  
   Data portofolio sebaiknya disimpan dalam model karena data menjadi lebih mudah dikelola, diperbarui, dan digunakan kembali tanpa harus mengubah kode HTML. Template dapat berfokus pada tampilan, sedangkan model menyimpan data yang ditampilkan. Dengan pendekatan ini, ketika terdapat perubahan atau penambahan data seperti riwayat pendidikan, data dapat diperbarui melalui database tanpa mengubah struktur template. Hal ini membuat pengembangan dan pemeliharaan website menjadi lebih efisien.

3. **Apa perbedaan `makemigrations` dan `migrate`? Berikan contohnya.**  
   `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan pada model Django. Sementara itu, `migrate` digunakan untuk menerapkan migration tersebut ke database sehingga struktur database benar-benar diperbarui. Contohnya, ketika menambahkan model `Education` ke `main/models.py`, perintah `python manage.py makemigrations` akan membuat file migration seperti `0002_education.py`. Setelah itu, `python manage.py migrate` menerapkan perubahan tersebut sehingga tabel `Education` dibuat di database.

### Tugas 3

1. **Mengapa menggunakan `ModelForm` dan mengapa perlu `{% csrf_token %}`?**  
   `ModelForm` digunakan karena dapat membuat form berdasarkan model Django yang sudah ada, sehingga field pada form dapat disesuaikan dengan field yang terdapat pada model. Dengan menggunakan `ModelForm`, kita tidak perlu membuat setiap field form HTML secara manual dan proses validasi data juga dapat dibantu oleh Django. Hal ini membuat proses pembuatan dan pengelolaan form menjadi lebih sederhana.

   `{% csrf_token %}` diperlukan untuk memberikan perlindungan terhadap serangan Cross-Site Request Forgery (CSRF). Token tersebut digunakan Django untuk memastikan bahwa request POST yang dikirim melalui form berasal dari halaman yang memang dibuat oleh aplikasi kita.

2. **Mengapa JSON lebih disukai dibandingkan XML dalam pengembangan aplikasi web modern?**  
   JSON lebih disukai karena formatnya lebih sederhana dan lebih ringkas dibandingkan XML. Struktur JSON juga lebih mudah dibaca dan digunakan dalam aplikasi web karena bentuk datanya dekat dengan struktur data yang digunakan dalam pemrograman, seperti object dan array.

   Selain itu, JSON memiliki ukuran data yang cenderung lebih kecil sehingga lebih praktis digunakan untuk pertukaran data antara server dan client. JSON juga banyak digunakan dalam API modern sehingga lebih mudah diintegrasikan dengan berbagai aplikasi web.

3. **Bagaimana alur view mengembalikan data portofolio dalam bentuk JSON dan mengapa perlu serialization?**  
   Ketika view dipanggil untuk mengembalikan data portofolio dalam bentuk JSON, view terlebih dahulu mengambil data dari model Django menggunakan query ke database. Data dari model tersebut kemudian diproses menggunakan `serializers.serialize()` untuk mengubah objek Django menjadi format JSON.

   Setelah proses serialization selesai, data JSON dikembalikan oleh view menggunakan `HttpResponse` dengan `content_type = "application/json"`. Serialization diperlukan karena objek model Django tidak dapat langsung dikirim sebagai JSON. Proses ini mengubah data dan informasi dari objek Django menjadi format yang dapat dibaca dan digunakan oleh client.

### Tugas 4

Pada Tugas 4, saya menambahkan fitur authentication, session, cookies, dan authorization pada website portofolio. Pengguna dapat melakukan register, login, dan logout, serta informasi login terakhir disimpan menggunakan cookie.

Pada bagian Projects, saya menambahkan fitur star sehingga pengguna yang sudah login dapat memberikan atau menghapus star pada project. Saya juga menerapkan pembatasan akses berdasarkan role pengguna. Guest dapat melihat project tetapi harus login untuk melakukan aksi yang membutuhkan akun. User biasa dapat melihat dan memberikan star, sedangkan superuser dapat menambahkan dan menghapus project.

Selain itu, saya menambahkan role Editor menggunakan Django Group. Editor dapat melihat dan melakukan update pada project, tetapi tidak memiliki akses untuk menambahkan atau menghapus project. Pembatasan akses diterapkan pada view menggunakan pengecekan server-side, sementara tombol atau fitur yang tidak dapat digunakan juga disembunyikan pada template.

Saya melakukan pengujian secara manual menggunakan development server dengan mencoba fitur menggunakan user biasa, Editor, dan superuser untuk memastikan setiap role memiliki akses yang sesuai.

### AI Disclosure
Dalam pengerjaan tugas ini, saya menggunakan ChatGPT dan Claude sebagai alat bantu pembelajaran, pengembangan, dan debugging.

**ChatGPT** digunakan untuk:
- Membantu memahami konsep Django ModelForm, CRUD, URL routing, JSON data delivery, serialization, dan deserialization.
- Membantu mengimplementasikan dan melakukan debugging pada fitur Create, Update, Delete, serta JSON Data Delivery untuk bagian Education.
- Membantu memeriksa struktur kode dan alur implementasi agar sesuai dengan requirement tugas.
- Membantu memahami konsep authentication, session, cookies, authorization, Django Group, dan role-based access control pada Tugas 4.
- Membantu mengimplementasikan dan melakukan debugging pada fitur login, register, logout, project starring, serta pembatasan akses berdasarkan role pengguna.
- Membantu mengimplementasikan role Editor dan fitur update project, serta membantu menganalisis error yang ditemukan selama proses testing.

**ChatGPT dan Claude** juga digunakan sebagai bantuan dalam pengembangan tampilan website, terutama untuk:
- Membantu menyusun dan memperbaiki CSS, termasuk layout, card, button, responsive design, dan elemen visual lainnya.
- Membantu melakukan debugging terhadap tampilan CSS ketika hasil yang ditampilkan belum sesuai.

Strategi prompting yang digunakan berupa pemberian konteks proyek, potongan kode, screenshot hasil implementasi, serta pertanyaan spesifik mengenai error atau perubahan yang ingin dilakukan. Output dari AI tidak digunakan secara langsung tanpa pemeriksaan. Saya menyesuaikan kode yang diberikan dengan struktur project dan melakukan pengujian secara manual.

Implementasi akhir diuji dengan menjalankan aplikasi menggunakan `python manage.py runserver` serta melakukan pengujian terhadap fitur pada Tugas 1 hingga Tugas 4. Pada Tugas 4, saya menguji authentication, authorization, project starring, serta pembatasan akses untuk user biasa, Editor, dan superuser. Saya juga melakukan perubahan dan penyesuaian manual terhadap kode dan tampilan sesuai kebutuhan project.

### AI Limitations and Manual Verification

AI membantu saya dalam memahami requirement dan menyusun perubahan kode, tetapi hasil dari AI tidak selalu dapat langsung digunakan tanpa pemeriksaan. Pada Tugas 4, misalnya, variabel `is_editor` sempat digunakan pada template sebelum didefinisikan pada view `show_projects`, sehingga aplikasi menghasilkan `NameError`.

Error tersebut ditemukan melalui pengujian manual pada development server. Saya kemudian memeriksa kembali alur data dari view ke template dan menambahkan definisi `is_editor` pada context sebelum melakukan pengujian ulang.

Selain itu, konfigurasi Group Editor dan pemberian role kepada user dilakukan secara manual melalui Django Admin. Pengujian akses untuk user biasa, Editor, dan superuser juga dilakukan secara manual untuk memastikan pembatasan akses berjalan sesuai requirement.