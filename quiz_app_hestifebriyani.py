import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import math


class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Pemrograman Event-Driven Tkinter")
        self.window.geometry("780x620")
        self.window.minsize(720, 560)
        self.window.configure(bg="#0F172A")  # Slate 900 dark theme modern

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

        # State Management
        self.current_question = 0
        self.score = 0
        self.time_limit = 20  # 20 detik per soal
        self.time_left = self.time_limit
        self.selected_answer = tk.IntVar(value=-1)  # -1 berarti belum ada pilihan
        self.timer_job = None
        self.animation_job = None
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
        """Mengatur styling ttk untuk progress bar dan widget modern"""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Custom ttk progressbar
        self.style.configure(
            "Quiz.Horizontal.TProgressbar",
            troughcolor="#1E293B",
            background="#38BDF8",
            lightcolor="#38BDF8",
            darkcolor="#0284C7",
            bordercolor="#1E293B",
            thickness=10
        )

    def buat_interface(self):
        """Membangun seluruh komponen antarmuka GUI (Materi 1, 3, 5, 6)"""
        # 1. Header Frame
        self.header_frame = tk.Frame(self.window, bg="#0F172A")
        self.header_frame.pack(fill=tk.X, padx=25, pady=(15, 5))

        # Title & Subtitle
        title_box = tk.Frame(self.header_frame, bg="#0F172A")
        title_box.pack(side=tk.LEFT)

        self.lbl_title = tk.Label(
            title_box,
            text="QUIZ INTERAKTIF TKINTER",
            font=("Segoe UI", 16, "bold"),
            fg="#F8FAFC",
            bg="#0F172A"
        )
        self.lbl_title.pack(anchor="w")

        self.lbl_subtitle = tk.Label(
            title_box,
            text="Uji Pemahaman Konsep Event-Driven, State & Timer",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A"
        )
        self.lbl_subtitle.pack(anchor="w")

        # Score & Question Counter Badges
        badges_box = tk.Frame(self.header_frame, bg="#0F172A")
        badges_box.pack(side=tk.RIGHT)

        self.badge_soal = tk.Label(
            badges_box,
            text="Soal: 1 / 10",
            font=("Segoe UI", 10, "bold"),
            fg="#38BDF8",
            bg="#1E293B",
            padx=12,
            pady=4,
            relief=tk.FLAT
        )
        self.badge_soal.pack(side=tk.LEFT, padx=4)

        self.badge_skor = tk.Label(
            badges_box,
            text="Skor: 0",
            font=("Segoe UI", 10, "bold"),
            fg="#4ADE80",
            bg="#1E293B",
            padx=12,
            pady=4,
            relief=tk.FLAT
        )
        self.badge_skor.pack(side=tk.LEFT, padx=4)

        # 2. Progress Bar Frame (Materi 6 - Visual Progress)
        progress_box = tk.Frame(self.window, bg="#0F172A")
        progress_box.pack(fill=tk.X, padx=25, pady=(8, 12))

        self.progress_var = tk.DoubleVar(value=0.0)
        self.progress_bar = ttk.Progressbar(
            progress_box,
            style="Quiz.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X)

        # 3. Main Question & Timer Container
        self.main_container = tk.Frame(self.window, bg="#1E293B", bd=0, highlightthickness=1, highlightbackground="#334155")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        # Timer & Status Sub-header inside container (Materi 4 & 5 - Canvas Animated Timer)
        timer_bar = tk.Frame(self.main_container, bg="#1E293B")
        timer_bar.pack(fill=tk.X, padx=20, pady=(15, 5))

        self.canvas_timer = tk.Canvas(timer_bar, width=36, height=36, bg="#1E293B", highlightthickness=0)
        self.canvas_timer.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_timer_text = tk.Label(
            timer_bar,
            text=f"Waktu Tersisa: {self.time_left}s",
            font=("Segoe UI", 11, "bold"),
            fg="#FACC15",
            bg="#1E293B"
        )
        self.lbl_timer_text.pack(side=tk.LEFT)

        # Visual indicator status validasi (Materi 6)
        self.lbl_validasi_status = tk.Label(
            timer_bar,
            text="Pilih salah satu jawaban",
            font=("Segoe UI", 9, "italic"),
            fg="#94A3B8",
            bg="#1E293B"
        )
        self.lbl_validasi_status.pack(side=tk.RIGHT)

        # Feedback Canvas Banner (Materi 4 & 5: Visual animation feedback benar / salah)
        self.feedback_canvas = tk.Canvas(
            self.main_container,
            height=34,
            bg="#1E293B",
            highlightthickness=0
        )
        self.feedback_canvas.pack(fill=tk.X, padx=20, pady=(5, 5))
        self.feedback_text = self.feedback_canvas.create_text(
            350, 17,
            text="",
            fill="#F8FAFC",
            font=("Segoe UI", 11, "bold")
        )

        # Question Text Area
        self.lbl_question = tk.Label(
            self.main_container,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#F8FAFC",
            bg="#1E293B",
            wraplength=680,
            justify=tk.LEFT,
            anchor="w"
        )
        self.lbl_question.pack(fill=tk.X, padx=20, pady=(5, 15))

        # Radiobutton Options Frame (Materi 3: tk.IntVar & Radiobutton)
        self.options_frame = tk.Frame(self.main_container, bg="#1E293B")
        self.options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        self.radio_buttons = []
        self.option_frames = []

        for i in range(4):
            opt_card = tk.Frame(
                self.options_frame,
                bg="#0F172A",
                bd=1,
                relief=tk.SOLID,
                highlightthickness=1,
                highlightbackground="#334155"
            )
            opt_card.pack(fill=tk.X, pady=4)
            self.option_frames.append(opt_card)

            # Shortcut badge (1, 2, 3, 4)
            badge_key = tk.Label(
                opt_card,
                text=f"[{i+1}]",
                font=("Consolas", 10, "bold"),
                fg="#38BDF8",
                bg="#1E293B",
                width=4,
                pady=6
            )
            badge_key.pack(side=tk.LEFT, padx=6, pady=4)

            # Radiobutton widget
            rb = tk.Radiobutton(
                opt_card,
                text="",
                variable=self.selected_answer,
                value=i,
                font=("Segoe UI", 11),
                fg="#E2E8F0",
                bg="#0F172A",
                activebackground="#0F172A",
                activeforeground="#38BDF8",
                selectcolor="#1E293B",
                anchor="w",
                padx=5,
                command=self.on_option_selected
            )
            rb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=6)
            self.radio_buttons.append(rb)

        # 4. Action Buttons & Shortcut Bar (Materi 2 - Event Handling & Interactivity)
        self.footer_frame = tk.Frame(self.window, bg="#0F172A")
        self.footer_frame.pack(fill=tk.X, padx=25, pady=(10, 15))

        # Shortcut hints on bottom left
        shortcut_info = tk.Label(
            self.footer_frame,
            text="Pintasan Keyboard: [Enter] Submit  |  [Esc] Lewati  |  [1-4] Pilih Opsi",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#0F172A"
        )
        shortcut_info.pack(side=tk.LEFT, pady=5)

        # Action Buttons on bottom right
        btn_box = tk.Frame(self.footer_frame, bg="#0F172A")
        btn_box.pack(side=tk.RIGHT)

        self.btn_skip = tk.Button(
            btn_box,
            text="Lewati (Esc)",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            bd=0,
            padx=16,
            pady=7,
            cursor="hand2",
            command=self.skip_question
        )
        self.btn_skip.pack(side=tk.LEFT, padx=6)

        self.btn_submit = tk.Button(
            btn_box,
            text="Kirim Jawaban (Enter)",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            bd=0,
            padx=18,
            pady=7,
            cursor="hand2",
            command=self.submit_answer
        )
        self.btn_submit.pack(side=tk.LEFT, padx=6)

    def bind_events(self):
        """Mendaftarkan keyboard shortcuts dan window event handling (Materi 2)"""
        # Keyboard Event: Enter untuk submit jawaban
        self.window.bind("<Return>", lambda event: self.submit_answer())
        self.window.bind("<KP_Enter>", lambda event: self.submit_answer())

        # Keyboard Event: Escape untuk skip soal
        self.window.bind("<Escape>", lambda event: self.skip_question())

        # Keyboard Event: Angka 1-4 untuk memilih opsi secara cepat
        for num in range(1, 5):
            self.window.bind(str(num), lambda event, idx=num-1: self.select_option_by_key(idx))
            self.window.bind(f"<KP_{num}>", lambda event, idx=num-1: self.select_option_by_key(idx))

        # Window Event: Konfirmasi saat jendela akan ditutup (Materi 2 - protocol)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handler saat jendela aplikasi ditutup oleh user (Materi 2 & 6)"""
        if self.current_question < len(self.questions):
            if messagebox.askyesno("Konfirmasi Keluar", "Quiz sedang berlangsung. Yakin ingin keluar dari aplikasi?"):
                self.stop_timer()
                self.window.destroy()
        else:
            self.window.destroy()

    def select_option_by_key(self, option_index):
        """Handler keyboard event untuk memilih radio button 1-4"""
        if not self.is_reviewing and self.current_question < len(self.questions):
            self.selected_answer.set(option_index)
            self.on_option_selected()

    def on_option_selected(self):
        """State listener saat opsi dipilih oleh pengguna (Materi 3 & 6 - Real-time Validation)"""
        val = self.selected_answer.get()
        if val != -1:
            self.lbl_validasi_status.config(
                text="✓ Jawaban dipilih. Tekan [Enter] untuk submit",
                fg="#4ADE80"
            )
            # Highlight selected frame visually
            for i, frame in enumerate(self.option_frames):
                if i == val:
                    frame.config(highlightbackground="#38BDF8", bg="#1E293B")
                else:
                    frame.config(highlightbackground="#334155", bg="#0F172A")

    def load_question(self):
        """Memuat pertanyaan saat ini ke interface GUI (Materi 1, 3, 6)"""
        if self.current_question >= len(self.questions):
            self.show_result()
            return

        q_data = self.questions[self.current_question]

        # Reset selection state
        self.selected_answer.set(-1)
        self.is_reviewing = False

        # Reset validation & feedback tampilan
        self.lbl_validasi_status.config(
            text="Pilih salah satu jawaban [1-4]",
            fg="#94A3B8"
        )
        self.clear_feedback_banner()

        # Update teks soal
        self.lbl_question.config(text=q_data["question"])

        # Update teks opsi radiobutton dan kembalikan warna normal
        for i in range(4):
            self.radio_buttons[i].config(
                text=q_data["options"][i],
                state=tk.NORMAL,
                fg="#E2E8F0"
            )
            self.option_frames[i].config(
                highlightbackground="#334155",
                bg="#0F172A"
            )

        # Update Badges & Progress Bar (Materi 6 - Progress Calculation)
        total_q = len(self.questions)
        self.badge_soal.config(text=f"Soal: {self.current_question + 1} / {total_q}")
        self.badge_skor.config(text=f"Skor: {self.score}")

        progress_pct = (self.current_question / total_q) * 100
        self.progress_var.set(progress_pct)

        # Aktifkan kembali tombol
        self.btn_submit.config(state=tk.NORMAL, bg="#2563EB", text="Kirim Jawaban (Enter)")
        self.btn_skip.config(state=tk.NORMAL)

        # Reset timer per soal
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
            # Jadwalkan eksekusi berikutnya setelah 1000 milidetik (1 detik)
            self.timer_job = self.window.after(1000, self.countdown_loop)
        else:
            # Waktu habis! Proses sebagai jawaban waktu habis otomatis
            self.on_time_out()

    def stop_timer(self):
        """Membatalkan timer aktif dengan after_cancel (Materi 4 & 5)"""
        if self.timer_job:
            self.window.after_cancel(self.timer_job)
            self.timer_job = None

    def update_timer_display(self):
        """Menggambar animasi progress cincin timer pada Canvas (Materi 4 & 5)"""
        self.lbl_timer_text.config(text=f"Waktu Tersisa: {self.time_left:02d}s")

        # Tentukan warna berdasarkan sisa waktu (Warning saat <= 5 detik)
        if self.time_left <= 5:
            color = "#EF4444"  # Merah peringatan
            self.lbl_timer_text.config(fg="#EF4444")
        elif self.time_left <= 10:
            color = "#F59E0B"  # Oranye
            self.lbl_timer_text.config(fg="#F59E0B")
        else:
            color = "#38BDF8"  # Biru normal
            self.lbl_timer_text.config(fg="#38BDF8")

        # Gambar indikator lingkaran jam pada Canvas (Materi 5)
        self.canvas_timer.delete("all")
        # Lingkaran background
        self.canvas_timer.create_oval(3, 3, 33, 33, outline="#334155", width=3)

        # Sudut lingkaran proporsional terhadap sisa waktu
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

        # Animasi feedback waktu habis
        self.animate_feedback(
            status="TIMEOUT",
            message=f"⏰ WAKTU HABIS! Jawaban yang benar: [{correct_idx + 1}] {self.questions[self.current_question]['options'][correct_idx]}"
        )

        # Highlight jawaban yang benar
        self.highlight_answers(selected_idx=-1, correct_idx=correct_idx)

        # Lanjut ke soal berikutnya setelah 2 detik
        self.window.after(2200, self.next_question)

    def submit_answer(self):
        """Validasi dan proses jawaban yang dikirim (Materi 6 - Validasi & Error Handling)"""
        if self.is_reviewing or self.current_question >= len(self.questions):
            return

        chosen = self.selected_answer.get()

        # VALIDASI INPUT: Memastikan pengguna sudah memilih opsi (Materi 6)
        if chosen == -1:
            self.lbl_validasi_status.config(
                text="⚠ PERINGATAN: Silakan pilih salah satu jawaban sebelum submit!",
                fg="#F87171"
            )
            # Shake animation kecil atau visual highlight pada opsi frame
            self.shake_validation_warning()
            return

        # Hentikan timer soal
        self.stop_timer()
        self.is_reviewing = True

        correct_idx = self.questions[self.current_question]["correct"]
        q_data = self.questions[self.current_question]

        # Nonaktifkan radio button agar tidak diubah saat animasi review
        for rb in self.radio_buttons:
            rb.config(state=tk.DISABLED)
        self.btn_submit.config(state=tk.DISABLED)
        self.btn_skip.config(state=tk.DISABLED)

        if chosen == correct_idx:
            # JAWABAN BENAR
            self.score += 10
            self.correct_count += 1
            self.user_history.append({
                "question": q_data["question"],
                "selected": chosen,
                "correct": correct_idx,
                "status": "CORRECT"
            })
            self.badge_skor.config(text=f"Skor: {self.score}")

            # Trigger Animasi Visual Feedback Benar (Materi 4 & 5)
            self.animate_feedback(
                status="CORRECT",
                message="✓ HEBAT! JAWABAN ANDA BENAR (+10 POIN)"
            )
        else:
            # JAWABAN SALAH
            self.wrong_count += 1
            self.user_history.append({
                "question": q_data["question"],
                "selected": chosen,
                "correct": correct_idx,
                "status": "WRONG"
            })

            # Trigger Animasi Visual Feedback Salah
            self.animate_feedback(
                status="WRONG",
                message=f"✗ JAWABAN SALAH! Yang benar adalah [{correct_idx + 1}] {q_data['options'][correct_idx]}"
            )

        # Highlight pilihan benar (hijau) & salah (merah)
        self.highlight_answers(selected_idx=chosen, correct_idx=correct_idx)

        # Jadwalkan transisi ke soal berikutnya setelah delay visual (2 detik)
        self.window.after(2200, self.next_question)

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

        self.window.after(1800, self.next_question)

    def highlight_answers(self, selected_idx, correct_idx):
        """Memberi warna visual pada opsi jawaban untuk feedback (Materi 6)"""
        for i in range(4):
            if i == correct_idx:
                self.option_frames[i].config(highlightbackground="#22C55E", bg="#14532D")
                self.radio_buttons[i].config(bg="#14532D", fg="#86EFAC")
            elif i == selected_idx and selected_idx != correct_idx:
                self.option_frames[i].config(highlightbackground="#EF4444", bg="#7F1D1D")
                self.radio_buttons[i].config(bg="#7F1D1D", fg="#FCA5A5")
            else:
                self.option_frames[i].config(highlightbackground="#334155", bg="#0F172A")
                self.radio_buttons[i].config(bg="#0F172A", fg="#64748B")

    def animate_feedback(self, status, message):
        """Animasi visual berdenyut/transisi warna pada Canvas Feedback (Materi 4 & 5)"""
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None

        color_map = {
            "CORRECT": ("#14532D", "#22C55E", "#86EFAC"),   # Dark green, Green, Light text
            "WRONG": ("#7F1D1D", "#EF4444", "#FCA5A5"),     # Dark red, Red, Light text
            "TIMEOUT": ("#78350F", "#F59E0B", "#FDE68A"),   # Dark amber, Amber, Light text
            "SKIPPED": ("#1E293B", "#64748B", "#E2E8F0")    # Slate
        }
        bg_col, border_col, fg_col = color_map.get(status, ("#1E293B", "#38BDF8", "#F8FAFC"))

        self.anim_step = 0
        self.run_pulse_animation(bg_col, border_col, fg_col, message)

    def run_pulse_animation(self, bg_col, border_col, fg_col, message):
        """Membuat efek denyutan visual dengan root.after (Materi 4)"""
        if self.anim_step < 6:
            # Efek kedip kontras
            cur_bg = border_col if self.anim_step % 2 == 0 else bg_col
            self.feedback_canvas.config(bg=cur_bg)
            self.feedback_canvas.itemconfig(self.feedback_text, text=message, fill="#FFFFFF")
            self.anim_step += 1
            self.animation_job = self.window.after(120, lambda: self.run_pulse_animation(bg_col, border_col, fg_col, message))
        else:
            self.feedback_canvas.config(bg=bg_col)
            self.feedback_canvas.itemconfig(self.feedback_text, text=message, fill=fg_col)

    def clear_feedback_banner(self):
        """Membersihkan banner animasi feedback"""
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
            self.animation_job = None
        self.feedback_canvas.config(bg="#1E293B")
        self.feedback_canvas.itemconfig(self.feedback_text, text="")

    def shake_validation_warning(self):
        """Animasi visual bergetar saat submit kosong ditekan (Materi 4 & 6)"""
        orig_colors = [f.cget("highlightbackground") for f in self.option_frames]
        for f in self.option_frames:
            f.config(highlightbackground="#EF4444")

        def reset_highlight():
            for f, col in zip(self.option_frames, orig_colors):
                f.config(highlightbackground=col)

        self.window.after(350, reset_highlight)

    def next_question(self):
        """Transisi state ke soal berikutnya (Materi 3 - State Management)"""
        self.current_question += 1
        self.load_question()
        if self.current_question < len(self.questions):
            self.start_timer()

    def show_result(self):
        """Menampilkan kartu hasil akhir evaluasi quiz (Materi 1, 3, 6)"""
        self.stop_timer()
        total_q = len(self.questions)
        pct = (self.score / (total_q * 10)) * 100
        self.progress_var.set(100)

        # Sembunyikan main container quiz
        self.main_container.pack_forget()
        self.footer_frame.pack_forget()

        # Buat Frame Hasil Akhir
        self.result_frame = tk.Frame(self.window, bg="#1E293B", highlightthickness=1, highlightbackground="#334155")
        self.result_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)

        # Header Hasil
        tk.Label(
            self.result_frame,
            text="HASIL AKHIR QUIZ INTERAKTIF",
            font=("Segoe UI", 18, "bold"),
            fg="#F8FAFC",
            bg="#1E293B"
        ).pack(pady=(25, 10))

        # Kategori Kelulusan
        if pct >= 80:
            predikat = "LUAR BIASA! PEMAHAMAN SANGAT BAIK"
            predikat_col = "#4ADE80"
        elif pct >= 60:
            predikat = "BAGUS! PEMAHAMAN CUKUP BAIK"
            predikat_col = "#38BDF8"
        else:
            predikat = "PERLU BELAJAR LAGI TENTANG TKINTER"
            predikat_col = "#F87171"

        tk.Label(
            self.result_frame,
            text=predikat,
            font=("Segoe UI", 12, "bold"),
            fg=predikat_col,
            bg="#1E293B"
        ).pack(pady=(0, 15))

        # Skor Besar Box
        skor_box = tk.Frame(self.result_frame, bg="#0F172A", padx=30, pady=15, relief=tk.RIDGE, bd=1)
        skor_box.pack(pady=10)

        tk.Label(
            skor_box,
            text=f"{self.score}",
            font=("Segoe UI", 48, "bold"),
            fg="#38BDF8",
            bg="#0F172A"
        ).pack()

        tk.Label(
            skor_box,
            text=f"Total Nilai: {pct:.1f}% (Maksimal 100)",
            font=("Segoe UI", 11),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack()

        # Rincian Statistik
        stats_frame = tk.Frame(self.result_frame, bg="#1E293B")
        stats_frame.pack(pady=15)

        self.create_stat_badge(stats_frame, "Benar", f"{self.correct_count}", "#22C55E")
        self.create_stat_badge(stats_frame, "Salah", f"{self.wrong_count}", "#EF4444")
        self.create_stat_badge(stats_frame, "Dilewati", f"{self.skipped_count}", "#F59E0B")

        # Tombol Aksi Akhir
        btn_action_box = tk.Frame(self.result_frame, bg="#1E293B")
        btn_action_box.pack(pady=20)

        btn_restart = tk.Button(
            btn_action_box,
            text="Ulangi Quiz (Restart)",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.restart_quiz
        )
        btn_restart.pack(side=tk.LEFT, padx=10)

        btn_quit = tk.Button(
            btn_action_box,
            text="Tutup Aplikasi",
            font=("Segoe UI", 11, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )
        btn_quit.pack(side=tk.LEFT, padx=10)

    def create_stat_badge(self, parent, label, value, color):
        """Helper untuk membuat kartu ringkasan skor"""
        box = tk.Frame(parent, bg="#0F172A", padx=18, pady=8, highlightthickness=1, highlightbackground="#334155")
        box.pack(side=tk.LEFT, padx=8)

        tk.Label(box, text=value, font=("Segoe UI", 16, "bold"), fg=color, bg="#0F172A").pack()
        tk.Label(box, text=label, font=("Segoe UI", 9), fg="#94A3B8", bg="#0F172A").pack()

    def restart_quiz(self):
        """Mereset state aplikasi untuk mengulang quiz dari awal (Materi 3 & 6)"""
        self.result_frame.destroy()
        self.current_question = 0
        self.score = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.skipped_count = 0
        self.user_history.clear()

        # Tampilkan kembali container utama
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)
        self.footer_frame.pack(fill=tk.X, padx=25, pady=(10, 15))

        self.load_question()
        self.start_timer()

    def jalankan(self):
        """Method untuk menjalankan event loop utama Tkinter (Materi 1)"""
        # Center window pada layar desktop
        self.window.update_idletasks()
        width = 780
        height = 620
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.window.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.jalankan()
