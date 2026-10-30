import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        
        self.selected_id = None

        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol di View ke fungsi Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        
        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.update_data)
        if hasattr(self.view, 'btn_delete'):
            self.view.btn_delete.configure(command=self.hapus_data)
        if hasattr(self.view, 'btn_logout'):
            self.view.btn_logout.configure(command=self.proses_logout)
        
        # Event saat baris tabel diklik
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data_tabel)

        # Zalfa Afiah Syuhlah_037
        # OTORISASI (TUGAS): Jika bukan admin, nonaktifkan form input dan tombol
        if self.user_role != 'admin':
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            if hasattr(self.view, 'btn_update'):
                self.view.btn_update.configure(state="disabled")
            if hasattr(self.view, 'btn_delete'):
                self.view.btn_delete.configure(state="disabled")
                
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_buku = self.model.get_all_buku()

        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    # Zalfa Afiah Syuhlah_037
    def pilih_data_tabel(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            values = self.view.tabel.item(selected_item[0], "values")
            
            if values:
                self.selected_id = values[0]

                if self.user_role == 'admin':
                    self.view.entry_judul.delete(0, 'end')
                    self.view.entry_judul.insert(0, values[1])

                    self.view.entry_penulis.delete(0, 'end')
                    self.view.entry_penulis.insert(0, values[2])

                    self.view.entry_tahun.delete(0, 'end')
                    self.view.entry_tahun.insert(0, values[3])

    # Zalfa Afiah Syuhlah_037
    def simpan_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_buku(judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    # Zalfa Afiah Syuhlah_037
    def update_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(self.selected_id, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data buku.")

    # Zalfa Afiah Syuhlah_037
    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data buku dari tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if konfirmasi:
            berhasil = self.model.delete_buku(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data buku.")

    # Zalfa Afiah Syuhlah_037
    # Menutup jendela perpustakaan dan kembali ke halaman Login
    def proses_logout(self):
        from controllers.auth_controller import AuthController
        self.view.destroy()
        auth = AuthController()
        auth.run()

    def bersihkan_form(self):
        self.selected_id = None
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')

    def run(self):
        self.view.mainloop()