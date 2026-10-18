import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math


class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Pemrograman Event-Driven Tkinter")
        self.window.geometry("780x630")
        self.window.minsize(740, 580)
        self.window.configure(bg="#F8FAFC")  # Light Slate 50 clean background

        # Data 10 Soal Berdasarkan Materi 1-6
        self.questions = [
            {
                "question": "1. Apa konsep fundamental dari paradigma Event-Driven Programming?",
                "options": [
                    "Program dieksekusi berurutan dari baris atas ke bawah secara linear",
                    "Program menunggu dan merespons kejadian (events) seperti klik atau tombol",
                    "Program berjalan tanpa antarmuka grafis (CLI) saja",
                    "Program wajib terhubung ke server web setiap saat"
                ],
                "correct": 1,
                "explanation": "Event-driven programming bekerja dalam event loop yang menunggu aksi/kejadian pengguna (Materi 1)."
            },
            {
                "question": "2. Method Tkinter manakah yang berfungsi menjalankan loop utama pendengar event (event loop)?",
                "options": [
                    "window.start_loop()",
                    "window.run_forever()",
                    "window.mainloop()",
                    "window.listen()"
                ],
                "correct": 2,
                "explanation": "mainloop() adalah infinite loop di Tkinter yang mendeteksi dan mendistribusikan semua event (Materi 1)."
            },
            {
                "question": "3. Method apa yang digunakan untuk menghubungkan event khusus (keyboard/mouse) ke fungsi handler?",
                "options": [
                    "widget.bind('<Event>', handler)",
                    "widget.connect(event, handler)",
                    "widget.trigger(event)",
                    "widget.add_listener(handler)"
                ],
                "correct": 0,
                "explanation": "Method .bind() digunakan untuk event handling fleksibel seperti keyboard dan mouse (Materi 2)."
            },
            {
                "question": "4. Mengapa pemanggilan time.sleep() dihindari dalam aplikasi GUI Tkinter?",
                "options": [
                    "Karena time.sleep() menghapus memori widget yang ada di layar",
                    "Karena time.sleep() bersifat blocking dan menyebabkan GUI 'Not Responding'",
                    "Karena fungsi tersebut hanya dapat digunakan pada sistem operasi Linux",
                    "Karena Tkinter tidak mendukung module bawaan 'time'"
                ],
                "correct": 1,
                "explanation": "time.sleep() memblokir thread GUI utama sehingga event loop terhenti dan GUI membeku (Materi 4)."
            },
            {
                "question": "5. Fungsi non-blocking apa yang disediakan Tkinter untuk timer rekursif / jeda waktu?",
                "options": [
                    "root.delay(milidetik, callback)",
                    "root.wait(milidetik, callback)",
                    "root.after(milidetik, callback)",
                    "root.timeout(milidetik, callback)"
                ],
                "correct": 2,
                "explanation": "root.after() menjadwalkan pemanggilan fungsi setelah jeda waktu tertentu tanpa memblokir GUI (Materi 4)."
            },
            {
                "question": "6. Method apa yang digunakan untuk membatalkan timer yang dijadwalkan oleh after()?",
                "options": [
                    "root.after_cancel(timer_id)",
                    "root.stop_timer(timer_id)",
                    "root.kill_job(timer_id)",
                    "root.cancel_timeout(timer_id)"
                ],
                "correct": 0,
                "explanation": "after_cancel() membatalkan eksekusi callback yang sebelumnya dijadwalkan dengan after() (Materi 4 & 5)."
            },
            {
                "question": "7. Tipe variabel kontrol Tkinter manakah yang tepat untuk mengikat opsi pilihan Radiobutton angka?",
                "options": [
                    "tk.StringVar",
                    "tk.IntVar",
                    "tk.DoubleVar",
                    "tk.BooleanVar"
                ],
                "correct": 1,
                "explanation": "tk.IntVar menyimpan data integer, sangat cocok untuk Radiobutton dengan indeks pilihan (Materi 3)."
            },
            {
                "question": "8. Widget Tkinter manakah yang digunakan untuk menggambar bentuk 2D dan animasi koordinat dinamis?",
                "options": [
                    "tk.Canvas",
                    "tk.Listbox",
                    "tk.Text",
                    "tk.Entry"
                ],
                "correct": 0,
                "explanation": "tk.Canvas menyediakan kemampuan manipulasi objek grafis seperti garis, lingkaran, dan animasi (Materi 2 & 5)."
            },
            {
                "question": "9. Validasi yang langsung mengevaluasi input ketika pengguna mengetik data dinamakan:",
                "options": [
                    "Submit-time validation",
                    "Offline validation",
                    "Real-time validation",
                    "Compile-time validation"
                ],
                "correct": 2,
                "explanation": "Real-time validation memberikan umpan balik seketika saat data dimasukkan atau diubah (Materi 6)."
            },
            {
                "question": "10. Protokol Tkinter apa yang digunakan untuk mencegat event saat tombol 'Close' (X) jendela diklik?",
                "options": [
                    "WM_CLOSE_EVENT",
                    "WM_DELETE_WINDOW",
                    "ON_WINDOW_QUIT",
                    "WINDOW_DESTROY"
                ],
                "correct": 1,
                "explanation": "protocol('WM_DELETE_WINDOW', handler) menangkap sinyal penutupan jendela dari window manager (Materi 2)."
            }
        ]

        # State Management (Materi 3)
        self.current_question = 0
        self.score = 0
        self.time_limit = 20  # 20 detik per soal
        self.time_left = self.time_limit
        self.selected_answer = tk.IntVar(value=-1)  # -1 berarti belum ada pilihan
        self.timer_job = None
        self.animation_job = None
        self.transition_job = None
        self.anim_step = 0
        self.is_reviewing = False  # Status jeda animasi feedback sebelum lanjut

        # Statistik Quiz
        self.correct_count = 0
        self.wrong_count = 0
        self.skipped_count = 0
        self.user_history = []

        # Setup Antarmuka & Event
        self.setup_styles()
        self.buat_interface()
        self.bind_events()

        # Inisialisasi Quiz
        self.load_question()
        self.start_timer()

    def setup_styles(self):
        """Mengatur styling ttk untuk progress bar modern dengan aksen Emerald Green (Materi 6)"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Quiz.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#16A34A",
            lightcolor="#22C55E",
            darkcolor="#15803D",
            bordercolor="#E2E8F0",
            thickness=10
        )

    def buat_interface(self):
        """Membangun seluruh komponen antarmuka GUI bertema Professional Light Mode (Materi 1, 3, 5, 6)"""
        # 1. Header Frame (Light Clean Theme)
        self.header_frame = tk.Frame(self.window, bg="#F8FAFC")
        self.header_frame.pack(fill=tk.X, padx=25, pady=(15, 5))

        title_box = tk.Frame(self.header_frame, bg="#F8FAFC")
        title_box.pack(side=tk.LEFT)

        self.lbl_title = tk.Label(
            title_box,
            text="QUIZ INTERAKTIF TKINTER",
            font=("Segoe UI", 16, "bold"),
            fg="#0F172A",
            bg="#F8FAFC"
        )
        self.lbl_title.pack(anchor="w")

        self.lbl_subtitle = tk.Label(
            title_box,
            text="Uji Pemahaman Konsep Event-Driven, State & Timer",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#F8FAFC"
        )
        self.lbl_subtitle.pack(anchor="w")

        # Badges Header: Soal & Skor (Primary Emerald Green Palette)
        badges_box = tk.Frame(self.header_frame, bg="#F8FAFC")
        badges_box.pack(side=tk.RIGHT)

        self.badge_soal = tk.Label(
            badges_box,
            text="Soal: 1 / 10",
            font=("Segoe UI", 10, "bold"),
            fg="#15803D",
            bg="#DCFCE7",
            padx=12,
            pady=5,
            relief=tk.FLAT
        )
        self.badge_soal.pack(side=tk.LEFT, padx=4)

        self.badge_skor = tk.Label(
            badges_box,
            text="Skor: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#FFFFFF",
            bg="#16A34A",
            padx=14,
            pady=5,
            relief=tk.FLAT
        )
        self.badge_skor.pack(side=tk.LEFT, padx=4)

        # 2. Progress Bar Frame (Materi 6 - Visual Progress)
        progress_box = tk.Frame(self.window, bg="#F8FAFC")
        progress_box.pack(fill=tk.X, padx=25, pady=(8, 10))

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            progress_box,
            style="Quiz.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)

        # 3. Main Question Container (Card Style: White background with subtle slate border)
        self.main_container = tk.Frame(
            self.window,
            bg="#FFFFFF",
            bd=0,
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        # Timer & Status Sub-header (Materi 4 & 5 - Canvas Animated Timer)
        timer_bar = tk.Frame(self.main_container, bg="#FFFFFF")
        timer_bar.pack(fill=tk.X, padx=20, pady=(12, 5))

        self.canvas_timer = tk.Canvas(timer_bar, width=36, height=36, bg="#FFFFFF", highlightthickness=0)
        self.canvas_timer.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_timer_text = tk.Label(
            timer_bar,
            text=f"Waktu Tersisa: {self.time_left}s",
            font=("Segoe UI", 11, "bold"),
            fg="#16A34A",
            bg="#FFFFFF"
        )
        self.lbl_timer_text.pack(side=tk.LEFT)

        # Status validasi umpan balik teks (Materi 6)
        self.lbl_validasi_status = tk.Label(
            timer_bar,
            text="Pilih salah satu jawaban [1-4]",
            font=("Segoe UI", 9, "italic"),
            fg="#64748B",
            bg="#FFFFFF"
        )
        self.lbl_validasi_status.pack(side=tk.RIGHT)

        # Feedback Canvas Banner (Materi 4 & 5: Visual animated feedback benar / salah)
        self.feedback_canvas = tk.Canvas(
            self.main_container,
            height=42,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.feedback_canvas.pack(fill=tk.X, padx=20, pady=(4, 6))
        self.feedback_text = self.feedback_canvas.create_text(
            350, 21,
            text="",
            fill="#1E293B",
            font=("Segoe UI", 11, "bold"),
            width=660,
            justify=tk.CENTER
        )
        self.feedback_canvas.bind("<Configure>", self.recenter_feedback_text)

        # Question Text Area
        self.lbl_question = tk.Label(
            self.main_container,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#0F172A",
            bg="#FFFFFF",
            wraplength=680,
            justify=tk.LEFT,
            anchor="w"
        )
        self.lbl_question.pack(fill=tk.X, padx=20, pady=(2, 12))

        # Radiobutton Options Frame (Materi 3: tk.IntVar & Radiobutton)
        self.options_frame = tk.Frame(self.main_container, bg="#FFFFFF")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 12))

        self.radio_buttons = []
        self.option_frames = []
        self.badge_labels = []

        for i in range(4):
            opt_card = tk.Frame(
                self.options_frame,
                bg="#F8FAFC",
                bd=1,
                relief=tk.SOLID,
                highlightthickness=1,
                highlightbackground="#E2E8F0",
                cursor="hand2"
            )
            opt_card.pack(fill=tk.X, pady=4)
            self.option_frames.append(opt_card)

            # Shortcut badge [1], [2], [3], [4]
            badge_key = tk.Label(
                opt_card,
                text=f"[{i+1}]",
                font=("Consolas", 10, "bold"),
                fg="#16A34A",
                bg="#E2E8F0",
                width=4,
                pady=6,
                cursor="hand2"
            )
            badge_key.pack(side=tk.LEFT, padx=6, pady=4)
            self.badge_labels.append(badge_key)

            # Radiobutton widget (Light styling)
            rb = tk.Radiobutton(
                opt_card,
                text="",
                variable=self.selected_answer,
                value=i,
                tristatevalue="x_none",
                font=("Segoe UI", 11),
                fg="#1E293B",
                bg="#F8FAFC",
                activebackground="#F8FAFC",
                activeforeground="#16A34A",
                selectcolor="#FFFFFF",
                anchor="w",
                padx=5,
                cursor="hand2",
                command=self.on_option_selected
            )
            rb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=6)
            self.radio_buttons.append(rb)

            # Event Mouse: Klik pada kartu atau badge juga memilih opsi
            opt_card.bind("<Button-1>", lambda event, idx=i: self.select_option_by_key(idx))
            badge_key.bind("<Button-1>", lambda event, idx=i: self.select_option_by_key(idx))

        # 4. Action Buttons & Shortcut Bar (Materi 2 - Event Handling & Interactivity)
        self.footer_frame = tk.Frame(self.window, bg="#F8FAFC")
        self.footer_frame.pack(fill=tk.X, padx=25, pady=(8, 14))

        shortcut_info = tk.Label(
            self.footer_frame,
            text="Pintasan Keyboard: [Enter] Submit  |  [Esc] Lewati  |  [1-4] Pilih Opsi",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#F8FAFC"
        )
        shortcut_info.pack(side=tk.LEFT, pady=5)

        btn_box = tk.Frame(self.footer_frame, bg="#F8FAFC")
        btn_box.pack(side=tk.RIGHT)

        # Tombol Lewati (Light Slate style)
        self.btn_skip = tk.Button(
            btn_box,
            text="Lewati (Esc)",
            font=("Segoe UI", 10, "bold"),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            activeforeground="#0F172A",
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            command=self.skip_question
        )
        self.btn_skip.pack(side=tk.LEFT, padx=6)

        # Tombol Submit (Primary Emerald Green)
        self.btn_submit = tk.Button(
            btn_box,
            text="Kirim Jawaban (Enter)",
            font=("Segoe UI", 10, "bold"),
            bg="#16A34A",
            fg="#FFFFFF",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=18,
            pady=7,
            cursor="hand2",
            command=self.submit_answer
        )
        self.btn_submit.pack(side=tk.LEFT, padx=6)

    def recenter_feedback_text(self, event):
        """Memastikan posisi teks banner feedback selalu berada tepat di tengah horizontal"""
        if hasattr(self, 'feedback_canvas') and hasattr(self, 'feedback_text'):
            self.feedback_canvas.coords(self.feedback_text, event.width // 2, 21)

    def bind_events(self):
        """Mendaftarkan keyboard shortcuts dan window event handling (Materi 2)"""
        self.window.bind("<Return>", lambda event: self.submit_answer())
        self.window.bind("<KP_Enter>", lambda event: self.submit_answer())
        self.window.bind("<Escape>", lambda event: self.skip_question())

        for num in range(1, 5):
            self.window.bind(str(num), lambda event, idx=num-1: self.select_option_by_key(idx))
            self.window.bind(f"<KP_{num}>", lambda event, idx=num-1: self.select_option_by_key(idx))

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handler saat jendela aplikasi ditutup oleh user (Materi 2 & 6)"""
        if self.current_question < len(self.questions):
            if messagebox.askyesno("Konfirmasi Keluar", "Quiz sedang berlangsung. Yakin ingin keluar dari aplikasi?"):
                self.stop_all_jobs()
                self.window.destroy()
        else:
            self.stop_all_jobs()
            self.window.destroy()

    def select_option_by_key(self, option_index):
        """Handler event untuk memilih radio button 1-4 via keyboard maupun klik kartu"""
        if not self.is_reviewing and self.current_question < len(self.questions):
            self.selected_answer.set(option_index)
            self.on_option_selected()

    def on_option_selected(self):
        """State listener saat opsi dipilih oleh pengguna (Materi 3 & 6 - Real-time Validation)"""
        val = self.selected_answer.get()
        if val != -1 and not self.is_reviewing:
            self.lbl_validasi_status.config(
                text="✓ Jawaban dipilih. Tekan [Enter] untuk submit",
                fg="#16A34A"
            )
            # Sinkronisasi warna visual kartu ke Emerald Green saat dipilih
            for i in range(4):
                if i == val:
                    self.option_frames[i].config(highlightbackground="#16A34A", bg="#F0FDF4")
                    self.radio_buttons[i].config(bg="#F0FDF4", fg="#14532D", selectcolor="#16A34A")
                    self.badge_labels[i].config(bg="#16A34A", fg="#FFFFFF")
                else:
                    self.option_frames[i].config(highlightbackground="#E2E8F0", bg="#F8FAFC")
                    self.radio_buttons[i].config(bg="#F8FAFC", fg="#1E293B", selectcolor="#FFFFFF")
                    self.badge_labels[i].config(bg="#E2E8F0", fg="#16A34A")

    def reset_option_styles(self):
        """Mereset seluruh styling visual kartu dan radio button ke status netral light mode"""
        for i in range(4):
            self.option_frames[i].config(
                highlightbackground="#E2E8F0",
                bg="#F8FAFC"
            )
            self.radio_buttons[i].config(
                bg="#F8FAFC",
                fg="#1E293B",
                activebackground="#F8FAFC",
                activeforeground="#16A34A",
                selectcolor="#FFFFFF",
                state=tk.NORMAL
            )
            self.badge_labels[i].config(
                bg="#E2E8F0",
                fg="#16A34A"
            )

    def load_question(self):
        """Memuat pertanyaan saat ini ke interface GUI dan membersihkan seluruh state soal lama (Materi 1, 3, 6)"""
        if self.current_question >= len(self.questions):
            self.show_result()
            return

        q_data = self.questions[self.current_question]

        # 1. Hentikan animasi/transisi sebelumnya
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None
        if self.transition_job:
            self.window.after_cancel(self.transition_job)
            self.transition_job = None

        # 2. Reset selection state & flag review
        self.selected_answer.set(-1)
        self.is_reviewing = False

        # 3. Bersihkan feedback banner dari soal sebelumnya
        self.clear_feedback_banner()

        # 4. Reset teks status validasi
        self.lbl_validasi_status.config(
            text="Pilih salah satu jawaban [1-4]",
            fg="#64748B"
        )

        # 5. Reset seluruh styling kartu & opsi agar tidak ada sisa warna hijau/merah
        self.reset_option_styles()

        # 6. Pasang teks soal dan teks pilihan baru
        self.lbl_question.config(text=q_data["question"])
        for i in range(4):
            self.radio_buttons[i].config(text=q_data["options"][i])

        # 7. Update Header Badges & Progress Bar (Materi 6)
        total_q = len(self.questions)
        self.badge_soal.config(text=f"Soal: {self.current_question + 1} / {total_q}")
        self.badge_skor.config(text=f"Skor: {self.score}")

        progress_pct = (self.current_question / total_q) * 100
        self.progress_var.set(progress_pct)

        # 8. Aktifkan kembali tombol submit & skip
        self.btn_submit.config(state=tk.NORMAL, bg="#16A34A", text="Kirim Jawaban (Enter)")
        self.btn_skip.config(state=tk.NORMAL)

        # 9. Reset timer per soal
        self.time_left = self.time_limit
        self.update_timer_display()

    def start_timer(self):
        """Memulai countdown timer menggunakan root.after non-blocking (Materi 4 & 5)"""
        self.stop_timer()
        self.countdown_loop()

    def countdown_loop(self):
        """Loop rekursif countdown timer per detik (Materi 4)"""
        if self.is_reviewing:
            return

        self.update_timer_display()

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_job = self.window.after(1000, self.countdown_loop)
        else:
            self.on_time_out()

    def stop_timer(self):
        """Membatalkan timer aktif dengan after_cancel (Materi 4 & 5)"""
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

    def stop_all_jobs(self):
        """Membatalkan seluruh scheduled task Tkinter aktif (Timer, Animasi, Transisi)"""
        self.stop_timer()
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None
        if self.transition_job:
            self.window.after_cancel(self.transition_job)
            self.transition_job = None

    def update_timer_display(self):
        """Menggambar animasi progress cincin timer pada Canvas (Materi 4 & 5)"""
        self.lbl_timer_text.config(text=f"Waktu Tersisa: {self.time_left:02d}s")

        if self.time_left <= 5:
            color = "#DC2626"  # Merah peringatan bahaya
            self.lbl_timer_text.config(fg="#DC2626")
        elif self.time_left <= 10:
            color = "#D97706"  # Oranye peringatan
            self.lbl_timer_text.config(fg="#D97706")
        else:
            color = "#16A34A"  # Emerald Green normal
            self.lbl_timer_text.config(fg="#16A34A")

        self.canvas_timer.delete("all")
        # Background ring outline
        self.canvas_timer.create_oval(3, 3, 33, 33, outline="#E2E8F0", width=3)

        extent_angle = (self.time_left / self.time_limit) * 360
        if extent_angle > 0:
            self.canvas_timer.create_arc(
                3, 3, 33, 33,
                start=90,
                extent=-extent_angle,
                outline=color,
                style=tk.ARC,
                width=3
            )

    def on_time_out(self):
        """Handler saat waktu soal habis (Materi 4 & 6)"""
        self.stop_timer()
        self.is_reviewing = True
        self.wrong_count += 1

        correct_idx = self.questions[self.current_question]["correct"]
        self.user_history.append({
            "question": self.questions[self.current_question]["question"],
            "selected": None,
            "correct": correct_idx,
            "status": "TIMEOUT"
        })

        self.animate_feedback(
            status="TIMEOUT",
            message=f"⏰ WAKTU HABIS! Jawaban yang benar: [{correct_idx + 1}] {self.questions[self.current_question]['options'][correct_idx]}"
        )

        self.highlight_answers(selected_idx=-1, correct_idx=correct_idx)
        self.transition_job = self.window.after(2200, self.next_question)

    def submit_answer(self):
        """Validasi dan proses jawaban yang dikirim (Materi 6 - Validasi & Error Handling)"""
        if self.is_reviewing or self.current_question >= len(self.questions):
            return

        chosen = self.selected_answer.get()

        # VALIDASI INPUT: Memastikan pengguna sudah memilih opsi (Materi 6)
        if chosen == -1:
            self.lbl_validasi_status.config(
                text="⚠ PERINGATAN: Silakan pilih salah satu jawaban sebelum submit!",
                fg="#DC2626"
            )
            self.shake_validation_warning()
            return

        self.stop_timer()
        self.is_reviewing = True

        correct_idx = self.questions[self.current_question]["correct"]
        q_data = self.questions[self.current_question]

        # Nonaktifkan interaksi saat proses evaluasi
        for rb in self.radio_buttons:
            rb.config(state=tk.DISABLED)
        self.btn_submit.config(state=tk.DISABLED)
        self.btn_skip.config(state=tk.DISABLED)

        if chosen == correct_idx:
            self.score += 10
            self.correct_count += 1
            self.user_history.append({
                "question": q_data["question"],
                "selected": chosen,
                "correct": correct_idx,
                "status": "CORRECT"
            })
            self.badge_skor.config(text=f"Skor: {self.score}")

            self.animate_feedback(
                status="CORRECT",
                message="✓ HEBAT! JAWABAN ANDA BENAR (+10 POIN)"
            )
        else:
            self.wrong_count += 1
            self.user_history.append({
                "question": q_data["question"],
                "selected": chosen,
                "correct": correct_idx,
                "status": "WRONG"
            })

            self.animate_feedback(
                status="WRONG",
                message=f"✗ JAWABAN SALAH! Yang benar adalah [{correct_idx + 1}] {q_data['options'][correct_idx]}"
            )

        self.highlight_answers(selected_idx=chosen, correct_idx=correct_idx)
        self.transition_job = self.window.after(2200, self.next_question)

    def skip_question(self):
        """Handler untuk melewatkan pertanyaan saat ini (Materi 2 - Esc Key)"""
        if self.is_reviewing or self.current_question >= len(self.questions):
            return

        self.stop_timer()
        self.is_reviewing = True
        self.skipped_count += 1

        correct_idx = self.questions[self.current_question]["correct"]
        self.user_history.append({
            "question": self.questions[self.current_question]["question"],
            "selected": None,
            "correct": correct_idx,
            "status": "SKIPPED"
        })

        self.animate_feedback(
            status="SKIPPED",
            message=f"↷ SOAL DILEWATI. Jawaban benar: [{correct_idx + 1}] {self.questions[self.current_question]['options'][correct_idx]}"
        )
        self.highlight_answers(selected_idx=-1, correct_idx=correct_idx)

        self.transition_job = self.window.after(1800, self.next_question)

    def highlight_answers(self, selected_idx, correct_idx):
        """Memberi warna visual pada opsi jawaban untuk feedback (Materi 6)"""
        for i in range(4):
            if i == correct_idx:
                # Opsi Benar -> Light Emerald Green Background
                self.option_frames[i].config(highlightbackground="#16A34A", bg="#DCFCE7")
                self.radio_buttons[i].config(bg="#DCFCE7", fg="#14532D", selectcolor="#16A34A")
                self.badge_labels[i].config(bg="#16A34A", fg="#FFFFFF")
            elif i == selected_idx and selected_idx != correct_idx:
                # Opsi Salah Pilihan User -> Light Rose Red Background
                self.option_frames[i].config(highlightbackground="#DC2626", bg="#FEE2E2")
                self.radio_buttons[i].config(bg="#FEE2E2", fg="#991B1B", selectcolor="#DC2626")
                self.badge_labels[i].config(bg="#DC2626", fg="#FFFFFF")
            else:
                # Opsi Netral Lainnya -> Redupkan sedikit agar fokus ke jawaban
                self.option_frames[i].config(highlightbackground="#E2E8F0", bg="#F8FAFC")
                self.radio_buttons[i].config(bg="#F8FAFC", fg="#94A3B8", selectcolor="#FFFFFF")
                self.badge_labels[i].config(bg="#F1F5F9", fg="#94A3B8")

    def animate_feedback(self, status, message):
        """Animasi visual berdenyut pada Canvas Feedback bertema Light Mode (Materi 4 & 5)"""
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None

        color_map = {
            "CORRECT": ("#DCFCE7", "#16A34A", "#14532D"),   # Light Green BG, Emerald Border, Dark Green Text
            "WRONG": ("#FEE2E2", "#DC2626", "#991B1B"),     # Light Red BG, Red Border, Dark Red Text
            "TIMEOUT": ("#FEF3C7", "#D97706", "#92400E"),   # Light Amber BG, Amber Border, Dark Amber Text
            "SKIPPED": ("#F1F5F9", "#94A3B8", "#334155")    # Light Slate BG, Slate Border, Slate Text
        }
        bg_col, border_col, fg_col = color_map.get(status, ("#F8FAFC", "#16A34A", "#1E293B"))

        self.anim_step = 0
        self.run_pulse_animation(bg_col, border_col, fg_col, message)

    def run_pulse_animation(self, bg_col, border_col, fg_col, message):
        """Membuat efek denyutan visual dengan root.after (Materi 4)"""
        if self.anim_step < 6:
            cur_bg = border_col if self.anim_step % 2 == 0 else bg_col
            cur_fg = "#FFFFFF" if self.anim_step % 2 == 0 else fg_col
            self.feedback_canvas.config(bg=cur_bg)
            self.feedback_canvas.itemconfig(self.feedback_text, text=message, fill=cur_fg)
            self.anim_step += 1
            self.animation_job = self.window.after(120, lambda: self.run_pulse_animation(bg_col, border_col, fg_col, message))
        else:
            self.feedback_canvas.config(bg=bg_col)
            self.feedback_canvas.itemconfig(self.feedback_text, text=message, fill=fg_col)

    def clear_feedback_banner(self):
        """Membersihkan banner animasi feedback secara menyeluruh"""
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None
        self.feedback_canvas.config(bg="#FFFFFF")
        self.feedback_canvas.itemconfig(self.feedback_text, text="", fill="#1E293B")

    def shake_validation_warning(self):
        """Animasi visual bergetar saat submit kosong ditekan (Materi 4 & 6)"""
        for f in self.option_frames:
            f.config(highlightbackground="#DC2626")

        def reset_highlight():
            if not self.is_reviewing:
                val = self.selected_answer.get()
                for i, f in enumerate(self.option_frames):
                    if i == val:
                        f.config(highlightbackground="#16A34A")
                    else:
                        f.config(highlightbackground="#E2E8F0")

        self.window.after(350, reset_highlight)

    def next_question(self):
        """Transisi state ke soal berikutnya (Materi 3 - State Management)"""
        self.current_question += 1
        self.load_question()
        if self.current_question < len(self.questions):
            self.start_timer()

    def show_result(self):
        """Menampilkan kartu hasil akhir evaluasi quiz bergaya Light Card (Materi 1, 3, 6)"""
        self.stop_all_jobs()
        total_q = len(self.questions)
        pct = (self.score / (total_q * 10)) * 100
        self.progress_var.set(100)

        # Sembunyikan main container quiz
        self.main_container.pack_forget()
        self.footer_frame.pack_forget()

        # Buat Frame Hasil Akhir (White Card Style)
        self.result_frame = tk.Frame(
            self.window,
            bg="#FFFFFF",
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        tk.Label(
            self.result_frame,
            text="HASIL AKHIR QUIZ INTERAKTIF",
            font=("Segoe UI", 18, "bold"),
            fg="#0F172A",
            bg="#FFFFFF"
        ).pack(pady=(25, 10))

        if pct >= 80:
            predikat = "LUAR BIASA! PEMAHAMAN SANGAT BAIK"
            predikat_col = "#16A34A"
        elif pct >= 60:
            predikat = "BAGUS! PEMAHAMAN CUKUP BAIK"
            predikat_col = "#059669"
        else:
            predikat = "PERLU BELAJAR LAGI TENTANG TKINTER"
            predikat_col = "#DC2626"

        tk.Label(
            self.result_frame,
            text=predikat,
            font=("Segoe UI", 12, "bold"),
            fg=predikat_col,
            bg="#FFFFFF"
        ).pack(pady=(0, 15))

        # Big Score Box (Emerald Tint Background)
        skor_box = tk.Frame(
            self.result_frame,
            bg="#F0FDF4",
            padx=32,
            pady=16,
            relief=tk.SOLID,
            bd=1,
            highlightthickness=1,
            highlightbackground="#BBF7D0"
        )
        skor_box.pack(pady=10)

        tk.Label(
            skor_box,
            text=f"{self.score}",
            font=("Segoe UI", 48, "bold"),
            fg="#16A34A",
            bg="#F0FDF4"
        ).pack()

        tk.Label(
            skor_box,
            text=f"Total Nilai: {pct:.1f}% (Maksimal 100)",
            font=("Segoe UI", 11, "bold"),
            fg="#15803D",
            bg="#F0FDF4"
        ).pack()

        stats_frame = tk.Frame(self.result_frame, bg="#FFFFFF")
        stats_frame.pack(pady=15)

        self.create_stat_badge(stats_frame, "Benar", f"{self.correct_count}", "#16A34A", "#DCFCE7", "#BBF7D0")
        self.create_stat_badge(stats_frame, "Salah", f"{self.wrong_count}", "#DC2626", "#FEE2E2", "#FECACA")
        self.create_stat_badge(stats_frame, "Dilewati", f"{self.skipped_count}", "#D97706", "#FEF3C7", "#FDE68A")

        btn_action_box = tk.Frame(self.result_frame, bg="#FFFFFF")
        btn_action_box.pack(pady=20)

        # Tombol Restart (Emerald Green)
        btn_restart = tk.Button(
            btn_action_box,
            text="Ulangi Quiz (Restart)",
            font=("Segoe UI", 11, "bold"),
            bg="#16A34A",
            fg="#FFFFFF",
            activebackground="#15803D",
            activeforeground="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.restart_quiz
        )
        btn_restart.pack(side=tk.LEFT, padx=10)

        # Tombol Tutup (Light Slate)
        btn_quit = tk.Button(
            btn_action_box,
            text="Tutup Aplikasi",
            font=("Segoe UI", 11, "bold"),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            activeforeground="#0F172A",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )
        btn_quit.pack(side=tk.LEFT, padx=10)

    def create_stat_badge(self, parent, label, value, text_color, bg_color, border_color):
        """Helper untuk membuat kartu ringkasan skor bertema clean light badge"""
        box = tk.Frame(
            parent,
            bg=bg_color,
            padx=18,
            pady=8,
            highlightthickness=1,
            highlightbackground=border_color
        )
        box.pack(side=tk.LEFT, padx=8)

        tk.Label(box, text=value, font=("Segoe UI", 16, "bold"), fg=text_color, bg=bg_color).pack()
        tk.Label(box, text=label, font=("Segoe UI", 9, "bold"), fg=text_color, bg=bg_color).pack()

    def restart_quiz(self):
        """Mereset state aplikasi untuk mengulang quiz dari awal (Materi 3 & 6)"""
        if hasattr(self, 'result_frame') and self.result_frame:
            self.result_frame.destroy()

        self.stop_all_jobs()
        self.current_question = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.skipped_count = 0
        self.user_history.clear()

        self.main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)
        self.footer_frame.pack(fill=tk.X, padx=25, pady=(8, 14))

        self.load_question()
        self.start_timer()

    def jalankan(self):
        """Method untuk menjalankan event loop utama Tkinter (Materi 1)"""
        self.window.update_idletasks()
        width = 780
        height = 630
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
