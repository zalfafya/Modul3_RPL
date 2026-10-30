# Sistem Manajemen Perpustakaan

Sistem Informasi Manajemen Perpustakaan Berbasis Desktop dibangun menggunakan bahasa pemrograman Python dengan antarmuka grafis CustomTkinter, arsitektur Model-View-Controller (MVC), basis data MySQL, serta dilengkapi otorisasi berbasis peran (RBAC) dan pengujian otomatis via CI/CD Pipeline.

---

## 🏗️ Arsitektur & Struktur Direktori (MVC)

Proyek ini menerapkan pola arsitektur **Model-View-Controller (MVC)** untuk memisahkan logika bisnis, tampilan antarmuka, dan pengontrol aplikasi:

```text
Modul3_RPL/
├── .github/
│   └── workflows/
│       └── ci_pipeline.yml    # Konfigurasi CI/CD Pipeline GitHub Actions
├── config/
│   └── database.py            # Koneksi basis data MySQL
├── controllers/
│   ├── auth_controller.py     # Logika autentikasi login & logout
│   └── buku_controller.py     # Logika CRUD data buku & proteksi RBAC
├── models/
│   ├── buku_model.py          # Kueri database untuk pengelolaan data buku
│   └── user_model.py          # Kueri database user & hashing password SHA-256
├── views/
│   ├── buku_view.py           # Antarmuka GUI utama (Buku & Tabel)
│   └── login_view.py          # Antarmuka GUI Form Login
├── tests/
│   ├── test_auth.py           # Unit testing fungsi autentikasi & hashing
│   └── test_buku.py           # Unit testing fungsi operasi buku
├── dist/
│   └── AplikasiPerpustakaan.exe # Berkas eksekusi mandiri (Executable)
├── main.py                    # Main Entry Point aplikasi
├── requirements.txt           # Daftar dependensi pustaka Python
└── README.md                  # Dokumentasi teknis proyek

⚙️ Konfigurasi Basis Data MySQL
1. Jalankan MySQL (Laragon/XAMPP).
2. Buat database dan tabel melalui terminal MySQL:
CREATE DATABASE perpustakaan;
USE perpustakaan;

CREATE TABLE users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'anggota') NOT NULL DEFAULT 'anggota'
);

CREATE TABLE buku (
    id_buku INT PRIMARY KEY AUTO_INCREMENT,
    judul VARCHAR(255) NOT NULL,
    penulis VARCHAR(255) NOT NULL,
    tahun_terbit INT NOT NULL
);

-- Akun Uji Coba (Hash SHA-256)
INSERT INTO users (username, password, role) VALUES
('petugas', SHA2('admin123', 256), 'admin'),
('mahasiswa', SHA2('user123', 256), 'anggota');

🚀 Cara Menjalankan Aplikasi
1. Clone & Install Dependensi:
git clone [https://github.com/USERNAME/Modul3_RPL.git](https://github.com/USERNAME/Modul3_RPL.git)
cd Modul3_RPL
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

2. Jalankan Aplikasi: python main.py

🔑 Akun Login
1. Admin (petugas / admin123): Akses penuh (Tambah, Edit, Hapus Buku)
2. Anggota (mahasiswa / user123): Read-only (Katalog Buku)