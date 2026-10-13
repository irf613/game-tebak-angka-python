# 🎯 Game Tebak Angka (Number Guessing Game) Python

Game Tebak Angka seru dan interaktif dengan dua pilihan mode:
1. **Mode Terminal / CLI (`main.py`)**: Berjalan langsung di command prompt/terminal dengan teks berwarna (ANSI), ASCII banner, dan audio/visual text feedback.
2. **Mode Desktop GUI (`gui_game.py`)**: Aplikasi jendela desktop modern bertema *Dark Mode* menggunakan Tkinter bawaan Python.

---

## 🚀 Cara Menjalankan

Buka terminal / PowerShell di folder proyek ini (`c:\gametebakangka`), lalu jalankan salah satu perintah berikut:

### 1. Jalankan Versi Terminal (CLI)
```bash
python main.py
```

### 2. Jalankan Versi Desktop (GUI)
```bash
python gui_game.py
```

---

## ✨ Fitur-Fitur Unggulan

- **3 Tingkat Kesulitan + Mode Kustom**:
  - **Mudah**: Rentang 1 - 50 (10 Kesempatan)
  - **Sedang**: Rentang 1 - 100 (7 Kesempatan)
  - **Sulit**: Rentang 1 - 200 (5 Kesempatan)
  - **Kustom (CLI)**: Tentukan sendiri batas angka minimum, maksimum, dan jumlah kesempatan.
- **Deteksi Kedekatan (Panas/Dingin)**:
  - 🔥 **Membara**: Selisih tebakan sangat dekat (≤ 3).
  - ♨️ **Panas**: Selisih dekat (≤ 8).
  - 🌤️ **Hangat**: Mulai mendekati target (≤ 20).
  - ❄️ **Dingin**: Masih jauh dari target.
- **Fitur Hint Spesial 💡**:
  - Jika kesempatan tersisa $\le 3$, pemain bisa membuka bocoran apakah angka rahasia genap/ganjil atau kelipatan angka tertentu.
- **Sistem Papan Skor (Leaderboard)**:
  - Skor dihitung berdasarkan sisa nyawa, kecepatan waktu bermain, dan penggunaan hint.
  - Skor tersimpan otomatis ke file `leaderboard.json` untuk melihat peringkat pemain terbaik.
- **Validasi Input Kuat**:
  - Mencegah error jika pemain salah memasukkan huruf, simbol, atau angka di luar batas.
- **Tanpa Perlu Install Package Eksternal**:
  - Murni menggunakan modul bawaan Python (`random`, `time`, `json`, `tkinter`, `os`).
