#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Tebak Angka Interaktif (Console / CLI)
Dibuat dengan Python 3 murni tanpa dependensi eksternal.
"""

import os
import sys
import random
import time
import json
from datetime import datetime

# Mengaktifkan dukungan UTF-8 dan ANSI Escape Color di terminal Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    os.system('')


class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    
    # Background
    BG_GREEN = "\033[42m"
    BG_RED   = "\033[41m"
    BG_CYAN  = "\033[46m"

LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")

def clear_screen():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{Color.CYAN}{Color.BOLD}
  ╔═════════════════════════════════════════════════════════════╗
  ║   🎯  G A M E   T E B A K   A N G K A   M I S T E R I  🎯  ║
  ╚═════════════════════════════════════════════════════════════╝{Color.RESET}
    {Color.YELLOW}Uji insting & logikamu untuk menebak angka rahasia!{Color.RESET}
    """
    print(banner)

def load_leaderboard():
    """Memuat data leaderboard dari file JSON."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_score(name, difficulty, score, attempts, elapsed_time):
    """Menyimpan skor baru ke file leaderboard."""
    scores = load_leaderboard()
    entry = {
        "nama": name,
        "tingkat": difficulty,
        "skor": score,
        "tebakan": attempts,
        "waktu_detik": round(elapsed_time, 1),
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M")
    }
    scores.append(entry)
    # Urutkan berdasarkan skor tertinggi, lalu waktu tersingkat
    scores.sort(key=lambda x: (-x["skor"], x["waktu_detik"]))
    # Simpan maksimal 15 skor teratas
    scores = scores[:15]
    
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=4)
    except Exception as e:
        print(f"{Color.RED}Gagal menyimpan skor: {e}{Color.RESET}")

def show_leaderboard():
    """Menampilkan papan peringkat skor tertinggi."""
    clear_screen()
    print_banner()
    print(f"\n{Color.YELLOW}{Color.BOLD}🏆 --- PAPAN PERINGKAT TERTINGGI (TOP SCORES) --- 🏆{Color.RESET}\n")
    
    scores = load_leaderboard()
    if not scores:
        print(f"  {Color.DIM}Belum ada riwayat permainan. Jadilah yang pertama!{Color.RESET}\n")
    else:
        print(f"  {Color.BOLD}{'No':<4} {'Nama':<15} {'Level':<10} {'Skor':<8} {'Tebakan':<10} {'Waktu':<10} {'Tanggal'}{Color.RESET}")
        print("  " + "─" * 70)
        for idx, item in enumerate(scores, 1):
            rank_color = Color.YELLOW if idx == 1 else (Color.WHITE if idx == 2 else (Color.MAGENTA if idx == 3 else Color.DIM))
            print(f"  {rank_color}{idx:<4} {item['nama']:<15} {item['tingkat']:<10} {item['skor']:<8} {item['tebakan']:<10} {item['waktu_detik']}s{'':<5} {item['tanggal']}{Color.RESET}")
    
    input(f"\n{Color.CYAN}Tekan [Enter] untuk kembali ke menu utama...{Color.RESET}")

def show_rules():
    """Menampilkan aturan bermain dan panduan petunjuk."""
    clear_screen()
    print_banner()
    print(f"""
{Color.YELLOW}{Color.BOLD}📖 --- PANDUAN & ATURAN BERMAIN --- 📖{Color.RESET}

1. Komputer akan memilih sebuah angka acak sesuai tingkat kesulitan:
   - {Color.GREEN}Mudah{Color.RESET}    : Rentang 1 - 50  (10 Kesempatan)
   - {Color.YELLOW}Sedang{Color.RESET}   : Rentang 1 - 100 (7 Kesempatan)
   - {Color.RED}Sulit{Color.RESET}    : Rentang 1 - 200 (5 Kesempatan)
   - {Color.CYAN}Kustom{Color.RESET}   : Tentukan sendiri rentang & kesempatan!

2. Setiap kali kamu menebak, komputer akan memberi petunjuk:
   - ⬆️  {Color.BLUE}Terlalu KECIL{Color.RESET} : Coba angka yang lebih besar!
   - ⬇️  {Color.MAGENTA}Terlalu BESAR{Color.RESET} : Coba angka yang lebih kecil!
   - 🔥 {Color.RED}Sangat Panas{Color.RESET}  : Selisih tebakan ≤ 5 dari angka target.
   - ♨️  {Color.YELLOW}Hangat{Color.RESET}        : Selisih tebakan ≤ 15 dari angka target.
   - ❄️  {Color.CYAN}Dingin{Color.RESET}        : Masih cukup jauh dari target.

3. {Color.BOLD}Fitur Hint Spesial:{Color.RESET}
   - Jika kesempatan tersisa tinggal 3 atau kurang, kamu bisa ketik {Color.BOLD}'hint'{Color.RESET} 
     untuk mendapatkan bocoran (apakah angka tersebut genap/ganjil atau kelipatannya).

4. {Color.BOLD}Sistem Skor:{Color.RESET}
   - Semakin sedikit tebakan dan semakin cepat kamu menyelesaikannya, 
     semakin tinggi skor yang kamu dapatkan!
""")
    input(f"{Color.CYAN}Tekan [Enter] untuk kembali ke menu utama...{Color.RESET}")

def get_proximity_hint(target, guess):
    """Memberikan feedback kedekatan (panas/hangat/dingin)."""
    diff = abs(target - guess)
    if diff == 0:
        return ""
    elif diff <= 3:
        return f"{Color.RED}{Color.BOLD}🔥 MEMBARA! Hampir kena banget! (Selisih ≤ 3){Color.RESET}"
    elif diff <= 8:
        return f"{Color.YELLOW}♨️  PANAS! Kamu sudah sangat dekat!{Color.RESET}"
    elif diff <= 20:
        return f"{Color.BLUE}🌤️  HANGAT! Arah tebakanmu mulai mendekat.{Color.RESET}"
    else:
        return f"{Color.CYAN}❄️  DINGIN! Masih jauh dari target.{Color.RESET}"

def generate_special_hint(target):
    """Menghasilkan petunjuk matematika cerdas untuk angka target."""
    hints = []
    # Genap / Ganjil
    if target % 2 == 0:
        hints.append("Angka ini adalah bilangan GENAP.")
    else:
        hints.append("Angka ini adalah bilangan GANJIL.")
        
    # Faktor / Kelipatan
    multiples = [3, 5, 7, 10]
    matched_multiples = [m for m in multiples if target % m == 0]
    if matched_multiples:
        chosen_m = random.choice(matched_multiples)
        hints.append(f"Angka ini adalah KELIPATAN dari {chosen_m}.")
    else:
        hints.append(f"Angka ini BUKAN kelipatan dari 3, 5, atau 10.")
        
    return random.choice(hints)

def play_game():
    """Fungsi utama jalannya ronde permainan."""
    clear_screen()
    print_banner()
    
    player_name = input(f"{Color.WHITE}Masukkan nama kamu: {Color.RESET}").strip()
    if not player_name:
        player_name = "Pemain"
        
    print(f"\n{Color.YELLOW}Pilih Tingkat Kesulitan:{Color.RESET}")
    print(f"  [{Color.GREEN}1{Color.RESET}] Mudah   (Angka 1 - 50,  10 Kesempatan)")
    print(f"  [{Color.YELLOW}2{Color.RESET}] Sedang   (Angka 1 - 100, 7 Kesempatan)")
    print(f"  [{Color.RED}3{Color.RESET}] Sulit    (Angka 1 - 200, 5 Kesempatan)")
    print(f"  [{Color.CYAN}4{Color.RESET}] Kustom   (Tentukan sendiri)")
    
    choice = input(f"\nPilihanmu (1-4) [Default 2]: ").strip()
    
    if choice == "1":
        diff_name = "Mudah"
        min_val, max_val = 1, 50
        max_attempts = 10
    elif choice == "3":
        diff_name = "Sulit"
        min_val, max_val = 1, 200
        max_attempts = 5
    elif choice == "4":
        diff_name = "Kustom"
        try:
            min_val = int(input("Nilai minimum: "))
            max_val = int(input("Nilai maksimum: "))
            if min_val >= max_val:
                print(f"{Color.RED}Nilai min harus lebih kecil dari max! Default ke 1 - 100.{Color.RESET}")
                min_val, max_val = 1, 100
            max_attempts = int(input("Jumlah kesempatan: "))
            if max_attempts <= 0:
                max_attempts = 7
        except ValueError:
            print(f"{Color.RED}Input salah, menggunakan pengaturan standar (1 - 100, 7x).{Color.RESET}")
            min_val, max_val = 1, 100
            max_attempts = 7
    else:
        diff_name = "Sedang"
        min_val, max_val = 1, 100
        max_attempts = 7

    target_number = random.randint(min_val, max_val)
    attempts_used = 0
    history = []
    hint_used = False
    
    clear_screen()
    print_banner()
    print(f"Halo {Color.CYAN}{Color.BOLD}{player_name}{Color.RESET}! Komputer telah memilih angka rahasia antara {Color.YELLOW}{min_val} s/d {max_val}{Color.RESET}.")
    print(f"Kamu memiliki {Color.GREEN}{Color.BOLD}{max_attempts} kali kesempatan{Color.RESET} untuk menebak.\n")
    
    start_time = time.time()
    won = False
    
    while attempts_used < max_attempts:
        remaining = max_attempts - attempts_used
        print("─" * 60)
        hearts = f"{Color.RED}❤️ {Color.RESET}" * remaining
        print(f"Kesempatan tersisa ({remaining}/{max_attempts}): {hearts}")
        
        if history:
            history_str = ", ".join(str(h) for h in history[-5:])
            print(f"{Color.DIM}Tebakan sebelumnya: [{history_str}]{Color.RESET}")
        
        # Opsi hint
        if remaining <= 3 and not hint_used:
            print(f"{Color.YELLOW}💡 Butuh bantuan? Ketik {Color.BOLD}'hint'{Color.RESET}{Color.YELLOW} untuk bocoran petunjuk.{Color.RESET}")
            
        user_input = input(f"{Color.WHITE}Tebakan #{attempts_used + 1}: {Color.RESET}").strip()
        
        if not user_input:
            print(f"{Color.RED}Harap masukkan angka!{Color.RESET}")
            continue
            
        if user_input.lower() == 'hint':
            if remaining > 3:
                print(f"{Color.YELLOW}Hint hanya tersedia saat sisa kesempatan ≤ 3!{Color.RESET}")
            elif hint_used:
                print(f"{Color.YELLOW}Kamu sudah menggunakan hint di ronde ini!{Color.RESET}")
            else:
                hint_clue = generate_special_hint(target_number)
                print(f"\n{Color.BG_CYAN}{Color.BOLD} 💡 BOCORAN PETUNJUK: {Color.RESET} {Color.CYAN}{hint_clue}{Color.RESET}\n")
                hint_used = True
            continue
            
        try:
            guess = int(user_input)
        except ValueError:
            print(f"{Color.RED}❌ Masukkan angka bulat yang valid (atau ketik 'hint')!{Color.RESET}")
            continue
            
        if guess < min_val or guess > max_val:
            print(f"{Color.YELLOW}⚠️  Perhatian: Angkamu di luar batas ({min_val} - {max_val})! Kesempatan tetap berkurang.{Color.RESET}")
            
        attempts_used += 1
        history.append(guess)
        
        if guess == target_number:
            won = True
            break
        elif guess < target_number:
            proximity = get_proximity_hint(target_number, guess)
            print(f"⬆️  {Color.BLUE}{Color.BOLD}TERLALU KECIL!{Color.RESET} Angka rahasia lebih BESAR dari {guess}.")
            if proximity:
                print(f"   {proximity}")
        else:
            proximity = get_proximity_hint(target_number, guess)
            print(f"⬇️  {Color.MAGENTA}{Color.BOLD}TERLALU BESAR!{Color.RESET} Angka rahasia lebih KECIL dari {guess}.")
            if proximity:
                print(f"   {proximity}")
        print()

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n" + "═" * 60)
    if won:
        # Perhitungan Skor: Sisa nyawa + bonus waktu
        remaining_lives = max_attempts - attempts_used
        base_score = (remaining_lives + 1) * 150
        time_bonus = max(0, int(100 - elapsed_time * 2))
        hint_penalty = 50 if hint_used else 0
        total_score = max(50, base_score + time_bonus - hint_penalty)
        
        print(f"{Color.GREEN}{Color.BOLD}🎉 SELAMAT {player_name.upper()}! TEBAKANMU BENAR! 🎉{Color.RESET}")
        print(f"Angka rahasianya memang: {Color.YELLOW}{Color.BOLD}{target_number}{Color.RESET}")
        print(f"• Tebakan berhasil dalam : {Color.BOLD}{attempts_used}{Color.RESET} kali percobaan")
        print(f"• Waktu yang dihabiskan  : {Color.BOLD}{elapsed_time:.1f}{Color.RESET} detik")
        print(f"• Total Skor             : {Color.YELLOW}{Color.BOLD}{total_score} Poin{Color.RESET}")
        
        save_score(player_name, diff_name, total_score, attempts_used, elapsed_time)
        print(f"{Color.GREEN}Skormu telah disimpan ke Leaderboard! 🏅{Color.RESET}")
    else:
        print(f"{Color.RED}{Color.BOLD}💀 YAAAH, KESEMPATANMU TELAH HABIS! 💀{Color.RESET}")
        print(f"Angka rahasia yang benar adalah: {Color.YELLOW}{Color.BOLD}{target_number}{Color.RESET}")
        print(f"Jangan patah semangat, coba lagi di ronde berikutnya!")
        
    print("═" * 60)
    
    replay = input(f"\nMau main lagi? ({Color.GREEN}y{Color.RESET}/{Color.RED}n{Color.RESET}) [y]: ").strip().lower()
    if replay in ('', 'y', 'ya', 'yes'):
        play_game()

def main():
    """Menu utama aplikasi."""
    while True:
        clear_screen()
        print_banner()
        print(f"{Color.BOLD}PILIH MENU:{Color.RESET}")
        print(f"  [{Color.GREEN}1{Color.RESET}] Mulai Permainan")
        print(f"  [{Color.YELLOW}2{Color.RESET}] Papan Peringkat (Leaderboard)")
        print(f"  [{Color.CYAN}3{Color.RESET}] Cara Bermain & Aturan")
        print(f"  [{Color.RED}4{Color.RESET}] Keluar")
        
        pilihan = input(f"\nMasukkan pilihanmu (1-4): ").strip()
        
        if pilihan == '1':
            play_game()
        elif pilihan == '2':
            show_leaderboard()
        elif pilihan == '3':
            show_rules()
        elif pilihan == '4':
            print(f"\n{Color.YELLOW}Terima kasih telah bermain! Sampai jumpa lagi! 👋{Color.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Color.RED}Pilihan tidak valid, silakan coba lagi.{Color.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{Color.YELLOW}Permainan dihentikan. Sampai jumpa lagi! 👋{Color.RESET}")
        sys.exit(0)

