#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Tebak Angka GUI Modern
Dibuat dengan Python Tkinter (Tanpa install library tambahan).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os

LEADERBOARD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leaderboard.json")

class GuessNumberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Tebak Angka Misteri - Game Python")
        self.root.geometry("540x700")
        self.root.resizable(False, False)
        
        # Tema Warna Modern Dark
        self.BG_MAIN    = "#181926"   # Background utama
        self.BG_CARD    = "#24273a"   # Card container
        self.BG_INPUT   = "#1e2030"   # Input background
        self.TEXT_COLOR = "#cad3f5"   # Teks utama
        self.TEXT_MUTED = "#8087a2"   # Teks sekunder
        self.ACCENT     = "#8aadf4"   # Biru pastel
        self.COLOR_WIN  = "#a6da95"   # Hijau pastel
        self.COLOR_WARN = "#eed49f"   # Kuning pastel
        self.COLOR_DANGER = "#ed8796" # Merah pastel
        self.COLOR_HOT  = "#f5a97f"   # Oranye panas
        self.COLOR_COLD = "#91d7e3"   # Cyan dingin
        
        self.root.configure(bg=self.BG_MAIN)
        
        # Status game
        self.target_number = 0
        self.min_val = 1
        self.max_val = 100
        self.max_attempts = 7
        self.remaining_attempts = 7
        self.attempts_used = 0
        self.game_active = False
        self.start_time = None
        self.history = []
        self.hint_used = False
        
        self._setup_ui()
        self.start_new_game()

    def _setup_ui(self):
        # 1. Header Banner
        header_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        header_frame.pack(fill="x", pady=(18, 10), padx=24)
        
        title_label = tk.Label(
            header_frame,
            text="🎯 TEBAK ANGKA MISTERI",
            font=("Segoe UI", 18, "bold"),
            fg=self.ACCENT,
            bg=self.BG_MAIN
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Tebak angka yang dipikirkan komputer dengan petunjuk interaktif!",
            font=("Segoe UI", 9),
            fg=self.TEXT_MUTED,
            bg=self.BG_MAIN
        )
        subtitle_label.pack(pady=(2, 0))

        # 2. Card Pengaturan Level
        diff_card = tk.Frame(self.root, bg=self.BG_CARD, padx=14, pady=10)
        diff_card.pack(fill="x", padx=24, pady=6)
        
        diff_title = tk.Label(
            diff_card,
            text="Tingkat Kesulitan:",
            font=("Segoe UI", 10, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_CARD
        )
        diff_title.pack(anchor="w", pady=(0, 6))
        
        self.diff_var = tk.StringVar(value="Sedang")
        btn_frame = tk.Frame(diff_card, bg=self.BG_CARD)
        btn_frame.pack(fill="x")
        
        levels = [
            ("Mudah (1-50, 10x)", "Mudah"),
            ("Sedang (1-100, 7x)", "Sedang"),
            ("Sulit (1-200, 5x)", "Sulit")
        ]
        
        for text, val in levels:
            rbtn = tk.Radiobutton(
                btn_frame,
                text=text,
                variable=self.diff_var,
                value=val,
                command=self.on_diff_change,
                font=("Segoe UI", 9),
                fg=self.TEXT_COLOR,
                bg=self.BG_CARD,
                selectcolor=self.BG_MAIN,
                activebackground=self.BG_CARD,
                activeforeground=self.ACCENT
            )
            rbtn.pack(side="left", expand=True)

        # 3. Card Status Permainan (Nyawa, Jangkauan)
        status_card = tk.Frame(self.root, bg=self.BG_CARD, padx=14, pady=12)
        status_card.pack(fill="x", padx=24, pady=8)
        
        top_status = tk.Frame(status_card, bg=self.BG_CARD)
        top_status.pack(fill="x")
        
        self.range_info = tk.Label(
            top_status,
            text="Rentang Angka: 1 - 100",
            font=("Segoe UI", 10, "bold"),
            fg=self.ACCENT,
            bg=self.BG_CARD
        )
        self.range_info.pack(side="left")
        
        self.attempt_info = tk.Label(
            top_status,
            text="Sisa: 7 / 7",
            font=("Segoe UI", 10, "bold"),
            fg=self.COLOR_WARN,
            bg=self.BG_CARD
        )
        self.attempt_info.pack(side="right")
        
        # Heart indicator
        self.heart_label = tk.Label(
            status_card,
            text="❤️❤️❤️❤️❤️❤️❤️",
            font=("Segoe UI", 14),
            bg=self.BG_CARD
        )
        self.heart_label.pack(pady=(6, 0))

        # 4. Box Feedback/Petunjuk Visual
        self.feedback_box = tk.Label(
            self.root,
            text="Silakan masukkan tebakan pertamamu!",
            font=("Segoe UI", 11, "bold"),
            fg=self.TEXT_COLOR,
            bg="#2a2d42",
            padx=12,
            pady=12,
            relief="flat",
            wraplength=480
        )
        self.feedback_box.pack(fill="x", padx=24, pady=6)

        # 5. Input Area
        input_card = tk.Frame(self.root, bg=self.BG_CARD, padx=16, pady=14)
        input_card.pack(fill="x", padx=24, pady=6)
        
        input_row = tk.Frame(input_card, bg=self.BG_CARD)
        input_row.pack()
        
        self.entry_guess = tk.Entry(
            input_row,
            font=("Segoe UI", 16, "bold"),
            width=8,
            justify="center",
            bg=self.BG_INPUT,
            fg=self.TEXT_COLOR,
            insertbackground=self.TEXT_COLOR,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#494d64",
            highlightcolor=self.ACCENT
        )
        self.entry_guess.pack(side="left", padx=(0, 10))
        self.entry_guess.bind("<Return>", lambda event: self.process_guess())
        
        self.btn_guess = tk.Button(
            input_row,
            text="Tebak! 🎲",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT,
            fg="#181926",
            activebackground="#b7bdf8",
            activeforeground="#181926",
            relief="flat",
            padx=16,
            pady=4,
            cursor="hand2",
            command=self.process_guess
        )
        self.btn_guess.pack(side="left", padx=4)
        
        self.btn_hint = tk.Button(
            input_row,
            text="💡 Hint",
            font=("Segoe UI", 10),
            bg="#363a4f",
            fg=self.COLOR_WARN,
            activebackground="#494d64",
            activeforeground=self.COLOR_WARN,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.request_hint
        )
        self.btn_hint.pack(side="left", padx=4)

        # 6. Card Riwayat Tebakan
        history_card = tk.Frame(self.root, bg=self.BG_CARD, padx=14, pady=10)
        history_card.pack(fill="both", expand=True, padx=24, pady=6)
        
        hist_title = tk.Label(
            history_card,
            text="Riwayat Tebakan Ronde Ini:",
            font=("Segoe UI", 9, "bold"),
            fg=self.TEXT_MUTED,
            bg=self.BG_CARD
        )
        hist_title.pack(anchor="w", pady=(0, 4))
        
        self.hist_listbox = tk.Listbox(
            history_card,
            font=("Consolas", 10),
            bg=self.BG_INPUT,
            fg=self.TEXT_COLOR,
            relief="flat",
            highlightthickness=0,
            selectbackground="#363a4f",
            height=6
        )
        self.hist_listbox.pack(fill="both", expand=True)

        # 7. Action Button Bar (Reset & Leaderboard)
        action_bar = tk.Frame(self.root, bg=self.BG_MAIN)
        action_bar.pack(fill="x", padx=24, pady=(8, 14))
        
        btn_reset = tk.Button(
            action_bar,
            text="🔄 Ronde Baru",
            font=("Segoe UI", 10, "bold"),
            bg="#363a4f",
            fg=self.TEXT_COLOR,
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.start_new_game
        )
        btn_reset.pack(side="left")
        
        btn_lb = tk.Button(
            action_bar,
            text="🏆 Papan Skor",
            font=("Segoe UI", 10),
            bg="#363a4f",
            fg=self.COLOR_WARN,
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.show_leaderboard_popup
        )
        btn_lb.pack(side="right")

    def on_diff_change(self):
        """Ketika pengguna mengubah pilihan kesulitan."""
        self.start_new_game()

    def start_new_game(self):
        """Memulai ronde baru."""
        diff = self.diff_var.get()
        if diff == "Mudah":
            self.min_val, self.max_val = 1, 50
            self.max_attempts = 10
        elif diff == "Sulit":
            self.min_val, self.max_val = 1, 200
            self.max_attempts = 5
        else: # Sedang
            self.min_val, self.max_val = 1, 100
            self.max_attempts = 7
            
        self.remaining_attempts = self.max_attempts
        self.attempts_used = 0
        self.target_number = random.randint(self.min_val, self.max_val)
        self.game_active = True
        self.start_time = time.time()
        self.history.clear()
        self.hint_used = False
        
        # Update display
        self.range_info.config(text=f"Rentang Angka: {self.min_val} - {self.max_val}")
        self.update_attempt_display()
        self.feedback_box.config(
            text="Ronde dimulai! Tebak angka yang dipilih komputer.",
            fg=self.TEXT_COLOR,
            bg="#2a2d42"
        )
        self.hist_listbox.delete(0, tk.END)
        self.entry_guess.config(state="normal")
        self.btn_guess.config(state="normal")
        self.entry_guess.delete(0, tk.END)
        self.entry_guess.focus()

    def update_attempt_display(self):
        self.attempt_info.config(
            text=f"Sisa: {self.remaining_attempts} / {self.max_attempts}"
        )
        self.heart_label.config(text="❤️" * self.remaining_attempts)

    def process_guess(self):
        if not self.game_active:
            self.start_new_game()
            return
            
        raw_val = self.entry_guess.get().strip()
        if not raw_val:
            return
            
        try:
            guess = int(raw_val)
        except ValueError:
            messagebox.showwarning("Input Salah", "Harap masukkan angka bulat yang valid!")
            self.entry_guess.delete(0, tk.END)
            return

        if guess < self.min_val or guess > self.max_val:
            messagebox.showinfo(
                "Di Luar Jangkauan",
                f"Angkamu di luar batas ({self.min_val} s/d {self.max_val})!\nNamun kesempatan tetap dihitung."
            )

        self.attempts_used += 1
        self.remaining_attempts -= 1
        self.update_attempt_display()
        
        diff = abs(self.target_number - guess)
        
        # Cek kondisi menang
        if guess == self.target_number:
            self.handle_win()
            return

        # Petunjuk & Feedback
        direction = "Lebih BESAR ⬆️" if guess < self.target_number else "Lebih KECIL ⬇️"
        
        if diff <= 3:
            heat = "🔥 MEMBARA! (Selisih ≤ 3)"
            box_bg = "#58303b"
            box_fg = self.COLOR_DANGER
        elif diff <= 8:
            heat = "♨️ SANGAT HANGAT!"
            box_bg = "#4d382c"
            box_fg = self.COLOR_HOT
        elif diff <= 20:
            heat = "🌤️ HANGAT"
            box_bg = "#2b3b4f"
            box_fg = self.COLOR_COLD
        else:
            heat = "❄️ DINGIN (Jauh)"
            box_bg = "#24273a"
            box_fg = self.TEXT_MUTED
            
        feedback_text = f"Tebakan: {guess} | Target {direction}\nStatus: {heat}"
        self.feedback_box.config(text=feedback_text, bg=box_bg, fg=box_fg)
        
        # Catat ke riwayat
        log_line = f"#{self.attempts_used:<2} Tebak: {guess:<4} -> {direction} ({heat})"
        self.hist_listbox.insert(0, log_line)
        
        # Bersihkan input
        self.entry_guess.delete(0, tk.END)
        self.entry_guess.focus()
        
        # Cek kondisi kalah
        if self.remaining_attempts <= 0:
            self.handle_game_over()

    def handle_win(self):
        self.game_active = False
        elapsed = time.time() - self.start_time
        base_score = (self.remaining_attempts + 1) * 150
        time_bonus = max(0, int(100 - elapsed * 2))
        hint_penalty = 50 if self.hint_used else 0
        total_score = max(50, base_score + time_bonus - hint_penalty)
        
        self.feedback_box.config(
            text=f"🎉 LUAR BIASA! BENAR: {self.target_number}!\n"
                 f"Tebakan: {self.attempts_used}x | Waktu: {elapsed:.1f}s | Skor: {total_score} Poin",
            bg="#2d4234",
            fg=self.COLOR_WIN
        )
        self.entry_guess.config(state="disabled")
        self.btn_guess.config(state="disabled")
        
        # Simpan skor popup
        self.prompt_save_score(total_score, elapsed)

    def handle_game_over(self):
        self.game_active = False
        self.feedback_box.config(
            text=f"💀 KESEMPATAN HABIS!\nAngka rahasia yang benar adalah: {self.target_number}",
            bg="#48242b",
            fg=self.COLOR_DANGER
        )
        self.entry_guess.config(state="disabled")
        self.btn_guess.config(state="disabled")
        
        messagebox.showinfo(
            "Game Over",
            f"Sayang sekali! Kesempatanmu habis.\nAngka rahasianya adalah {self.target_number}.\n\nKlik 'Ronde Baru' untuk mencoba lagi!"
        )

    def request_hint(self):
        if not self.game_active:
            return
        if self.hint_used:
            messagebox.showinfo("Hint", "Kamu sudah menggunakan hint pada ronde ini!")
            return
            
        if self.remaining_attempts > 3:
            messagebox.showinfo("Hint", f"Hint baru terbuka saat sisa kesempatan ≤ 3!\n(Sekarang tersisa {self.remaining_attempts})")
            return
            
        # Buat petunjuk
        hints = []
        if self.target_number % 2 == 0:
            hints.append("Angka rahasia adalah bilangan GENAP.")
        else:
            hints.append("Angka rahasia adalah bilangan GANJIL.")
            
        multiples = [3, 5, 7, 10]
        match = [m for m in multiples if self.target_number % m == 0]
        if match:
            hints.append(f"Angka ini adalah KELIPATAN {random.choice(match)}.")
        else:
            hints.append("Angka ini BUKAN kelipatan 3, 5, atau 10.")
            
        chosen_hint = "\n".join(hints)
        self.hint_used = True
        messagebox.showinfo("💡 Petunjuk Rahasia", f"Bocoran untukmu:\n\n{chosen_hint}\n\n(Pinalti 50 poin)")

    def prompt_save_score(self, score, elapsed):
        def save():
            name = entry_name.get().strip() or "Pemain"
            scores = []
            if os.path.exists(LEADERBOARD_FILE):
                try:
                    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                        scores = json.load(f)
                except Exception:
                    scores = []
            
            scores.append({
                "nama": name,
                "tingkat": self.diff_var.get(),
                "skor": score,
                "tebakan": self.attempts_used,
                "waktu_detik": round(elapsed, 1),
                "tanggal": time.strftime("%d-%m-%Y %H:%M")
            })
            scores.sort(key=lambda x: (-x["skor"], x["waktu_detik"]))
            scores = scores[:15]
            
            try:
                with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                    json.dump(scores, f, indent=4)
            except Exception:
                pass
                
            win_dialog.destroy()
            self.show_leaderboard_popup()

        win_dialog = tk.Toplevel(self.root)
        win_dialog.title("🎉 Kemenangan!")
        win_dialog.geometry("340x220")
        win_dialog.configure(bg=self.BG_MAIN)
        win_dialog.transient(self.root)
        win_dialog.grab_set()
        
        lbl = tk.Label(
            win_dialog,
            text=f"SELAMAT!\nKamu menang dengan {score} Poin!",
            font=("Segoe UI", 11, "bold"),
            fg=self.COLOR_WIN,
            bg=self.BG_MAIN
        )
        lbl.pack(pady=(16, 8))
        
        lbl2 = tk.Label(
            win_dialog,
            text="Masukkan namamu untuk leaderboard:",
            font=("Segoe UI", 9),
            fg=self.TEXT_COLOR,
            bg=self.BG_MAIN
        )
        lbl2.pack(pady=(0, 6))
        
        entry_name = tk.Entry(
            win_dialog,
            font=("Segoe UI", 11),
            bg=self.BG_INPUT,
            fg=self.TEXT_COLOR,
            justify="center",
            relief="flat",
            highlightthickness=1,
            highlightcolor=self.ACCENT
        )
        entry_name.pack(pady=4, ipady=3)
        entry_name.focus()
        entry_name.bind("<Return>", lambda e: save())
        
        btn_save = tk.Button(
            win_dialog,
            text="Simpan Skor 🏅",
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT,
            fg="#181926",
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=save
        )
        btn_save.pack(pady=12)

    def show_leaderboard_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("🏆 Papan Peringkat (Leaderboard)")
        popup.geometry("480x420")
        popup.configure(bg=self.BG_MAIN)
        popup.transient(self.root)
        
        lbl = tk.Label(
            popup,
            text="🏆 PAPAN PERINGKAT TERTINGGI",
            font=("Segoe UI", 13, "bold"),
            fg=self.COLOR_WARN,
            bg=self.BG_MAIN
        )
        lbl.pack(pady=(14, 8))
        
        text_area = tk.Text(
            popup,
            font=("Consolas", 10),
            bg=self.BG_INPUT,
            fg=self.TEXT_COLOR,
            relief="flat",
            padx=10,
            pady=10
        )
        text_area.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        
        scores = []
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    scores = json.load(f)
            except Exception:
                scores = []
                
        if not scores:
            text_area.insert("end", "Belum ada riwayat skor.\nMainkan game dan jadilah nomor 1!")
        else:
            header = f"{'No':<3} {'Nama':<12} {'Level':<8} {'Skor':<6} {'Tebakan':<7} {'Waktu'}\n"
            divider = "─" * 46 + "\n"
            text_area.insert("end", header + divider)
            for i, s in enumerate(scores, 1):
                row = f"{i:<3} {s['nama']:<12} {s['tingkat']:<8} {s['skor']:<6} {s['tebakan']:<7} {s['waktu_detik']}s\n"
                text_area.insert("end", row)
                
        text_area.config(state="disabled")

def main():
    root = tk.Tk()
    app = GuessNumberGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
