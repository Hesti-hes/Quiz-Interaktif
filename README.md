# Aplikasi Quiz Interaktif

---

## Identitas Mahasiswa

| Informasi | Keterangan |
| :--- | :--- |
| **Nama** | Hesti Febriyani |
| **NIM** | 24106050010 |
| **Mata Kuliah** | Pemrograman Platform Desktop |

---

## 📌 Deskripsi Singkat

Aplikasi **Quiz Interaktif** ini mengintegrasikan seluruh materi yang telah dipelajari:
1. **Event-Driven Architecture**: Berjalan di atas Tkinter `mainloop()`.
2. **Event Handling**: Dukungan mouse dan pintasan keyboard (`Enter`, `Esc`, dan angka `1-4`).
3. **State Management**: Pengelolaan data skor, soal aktif, dan opsi radiobutton (`tk.IntVar`).
4. **Timer Asinkron**: Countdown timer non-blocking menggunakan `root.after()` dan `root.after_cancel()`.
5. **Animasi Grafis & Visual**: Indikator timer ring pada `tk.Canvas` serta efek denyut visual (*pulse animation*) untuk umpan balik benar/salah.
6. **Validasi & Error Handling**: Peringatan visual jika submit tanpa memilih jawaban serta konfirmasi penutupan jendela (`WM_DELETE_WINDOW`).

---

## 🚀 Cara Menjalankan Aplikasi

Pastikan Python telah terpasang di komputer Anda, lalu buka terminal/command prompt pada direktori proyek ini dan jalankan perintah:

```powershell
python quiz_app.py
```

---

## ⌨️ Pintasan Keyboard (Shortcuts)

| Tombol Keyboard | Aksi |
| :--- | :--- |
| **1, 2, 3, 4** | Memilih opsi jawaban 1 sampai 4 secara cepat |
| **Enter** | Mengirimkan / submit jawaban yang dipilih |
| **Escape (Esc)** | Melewatkan soal saat ini (*Skip*) |

---