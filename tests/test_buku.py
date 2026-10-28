from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

# =========================================================
# TUGAS 3: Pengujian Fungsi get_all_buku()
# =========================================================
def test_get_all_buku_berhasil():
    # 1. Inisialisasi Model
    model = BukuModel()

    # 2. Mock koneksi database dan cursor
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # 3. Buat data tiruan yang seolah-olah dikembalikan oleh MySQL
    data_mock = [
        {'id_buku': 1, 'judul': 'Buku A', 'penulis': 'Penulis A', 'tahun_terbit': 2023},
        {'id_buku': 2, 'judul': 'Buku B', 'penulis': 'Penulis B', 'tahun_terbit': 2024}
    ]
    mock_cursor.fetchall.return_value = data_mock

    # 4. Jalankan fungsi get_all_buku()
    hasil = model.get_all_buku()

    # 5. Verifikasi pengujian (Assertion)
    assert hasil == data_mock  # Memastikan hasil sesuai dengan data mock
    assert len(hasil) == 2     # Memastikan jumlah data yang didapat sesuai
    mock_cursor.execute.assert_called_once()   # Memastikan perintah SQL dieksekusi
    mock_cursor.fetchall.assert_called_once()  # Memastikan fetchall dipanggil