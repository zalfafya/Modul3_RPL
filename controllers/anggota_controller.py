import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView

class AnggotaController:
    def __init__(self):
        self.model = AnggotaModel()
        self.view = AnggotaView()
        self.selected_id = None

        # Bind tombol
        self.view.btn_simpan.configure(command=self.simpan_data)

        if hasattr(self.view, 'btn_update'):
            self.view.btn_update.configure(command=self.update_data)
        if hasattr(self.view, 'btn_delete'):
            self.view.btn_delete.configure(command=self.hapus_data)
        elif hasattr(self.view, 'btn_hapus'):
            self.view.btn_hapus.configure(command=self.hapus_data)

        # Event klik tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data_tabel)

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)

        data_anggota = self.model.get_all_anggota()

        for anggota in data_anggota:
            # Mengisi ID, nama, dan alamat ke tabel
            self.view.tabel.insert("", "end", values=(anggota['id_anggota'], anggota['nama'], anggota['alamat']))

    def pilih_data_tabel(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            values = self.view.tabel.item(selected_item[0], "values")
            if values:
                self.selected_id = values[0]  # id_anggota

                # Tampilkan ke form input
                self.view.entry_nama.delete(0, 'end')
                self.view.entry_nama.insert(0, values[1])

                self.view.entry_alamat.delete(0, 'end')
                self.view.entry_alamat.insert(0, values[2])

    def simpan_data(self):
        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.create_anggota(nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data anggota.")

    def update_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel!")
            return

        nama = self.view.entry_nama.get()
        alamat = self.view.entry_alamat.get()

        if not nama or not alamat:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_anggota(self.selected_id, nama, alamat)
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal memperbarui data anggota.")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data anggota dari tabel!")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            berhasil = self.model.delete_anggota(self.selected_id)
            if berhasil:
                messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
                self.bersihkan_form()
                self.muat_data_tabel()
            else:
                messagebox.showerror("Error", "Gagal menghapus data anggota.")

    def bersihkan_form(self):
        self.selected_id = None
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_alamat.delete(0, 'end')

    def run(self):
        self.view.mainloop()