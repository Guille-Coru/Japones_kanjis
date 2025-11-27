import tkinter as tk
import random
import time
from PIL import Image, ImageTk  # <-- Solo para las imágenes

# --- DICCIONARIO DE KANJI 49 ELEMENTOS ---
kanji_dict = {
    "午":"ご　mediodía, caballo",
    "道": "みち calle, districto, senda",
    "不": "ぶ negativo, no",
    "世": "セイ, よ Mundo, generación",
    "主": "ぬし シュ Lord, jefe, master",
    "事": "こと, ジ Cosa, aspecto, nominalizador",
    "書": "かく, ショ escribir",
    "仕": "シ、ジ　(つか menos usado) atender, hacer, oficial",
    "代": "かわる, ダイ　substituto, cambio, tasa(fee), generación",
    "以": "もって, イ, Debido a, a través de, comparado con",
    "低": "ひくい、テイ corto, bajo, humilde",
    "住": "すむ、ジュウ vivir, residir (dwell)",
    "体": "からだ、タイ cuerpo, substancia, objeto, realidad",
    "作": "つく・る、サク crear, producir, preparar",
    "使": "つか・る、シ usar, mandar",
    "借": "か・りる、Prestar, alquilar",
    "便": "ベン、ビン、たよ・りConveniente, instalación, pis, caca",
    "働": "はたらく、trabajo",
    "元": "もと、ゲン、ガン　inicio, tiempo pasado, origen",
    "生": "う・まれる、セイ、ショウ vida / nacer",
    "先": "セン　ま・ず、さき　antes / previo",
    "文": "ぶん、Oracion",
    "教": "おし、キョウ　Enseñar",
    "室": "しつ　Sala",
    "習": "なら・う、シュウ、Aprender (con alguien)",
    "朝": "あさ、チョウ、Mañana (parte del día), dinastía",
    "夜": "よる、ヤ、Noche　",
    "卒": "ソツ　graduarse",
    "業": "ぎょう　Trabajo (va con graduación)",
    "試": "ため、シ　Probar, intento",
    "験": "ケン　Prueba, experimentar",
    "留": "リュウ、ル　Permanecer, (estudiar extranjero)",
    "級": "キュウ　Nivel",
    "初": "はじ・めて、ショ　Primero",
    "専": "セン　Exclusivo",
    "門": "もん　Puerta",
    "光": "ひか・る、コウ　Rayo, luz (optica en general)",
    "別": "ベツ　Separar, distinguir (betsuni)",
    "動": "おご・く、ドウ　Mover, movimiento, cambio confusión",
    "県": "ケン　Prefectura",
    "寒": "さむ・い、カン　Frío",
    "心": "こころ、シン　Corazón, mente (aparece abajo en el kanji de malo)",
    "思": "おも・う、シ　Pensar",
    "急": "いそ・ぐ、せ、キュウ　Repentino, emergencia, apurado",
    "悪": "わる。い、アク、　Malo, malvado, falso, maligno, erróneo",
    "意": "イ　Idea, mente, sabor, pensamiento, deseo, importancia",
    "説": "セツ、と・く　Rumor, opinión, explicación, teoría",
    "軽": "かる・い　Ligero, sin importancia, nimio, menor",
    "運": "はく・ぶ、ウン、Cargar, suerte, destino, transportar, progreso"
}

# Colores según resultado
COLOR_1 = "lightgreen"
COLOR_2 = "yellow"
COLOR_3 = "orange"
COLOR_FAIL = "red"

# --------------------------------------------------------------------------
# --------------------------- VENTANA EXTRA --------------------------------
# --------------------------------------------------------------------------
class ExtraWindow:
    def __init__(self, failed_list):
        self.failed = failed_list.copy()
        self.remaining = set(self.failed)
        self.intentos = {k: 0 for k in self.failed}
        self.root = tk.Toplevel()
        self.root.title("Repaso de fallos")
        self.start_time = time.time()
        self.timer_running = True

        # === Label del significado (solo, sin imágenes) ===
        self.meaning_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.meaning_label.pack(pady=15)

        # === Frame para timer con imágenes a los lados ===
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=5)

        try:
            img = Image.open("icon_left_demon.png").resize((100, 153), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(stats_frame, image=photo).pack(side="left", padx=20)
            self.root.image_left = photo
        except:
            pass

        self.timer_label = tk.Label(stats_frame, text="Tiempo: 00:00.0", font=("Arial", 16))
        self.timer_label.pack(side="left", padx=10)

        try:
            img = Image.open("icon_right_demon.png").resize((100, 126), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(stats_frame, image=photo).pack(side="right", padx=20)
            self.root.image_right = photo
        except:
            pass

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        self.buttons = {}
        idx = 0
        all_kanjis = list(kanji_dict.keys())
        for r in range(7):
            for c in range(7):
                k = all_kanjis[idx]
                if k in self.failed:
                    b = tk.Button(
                        self.grid_frame,
                        text=k,
                        font=("Arial", 24),
                        width=3,
                        height=1,
                        command=lambda x=k: self.check_answer(x)
                    )
                else:
                    b = tk.Button(
                        self.grid_frame,
                        text="",
                        font=("Arial", 24),
                        width=3,
                        height=1,
                        state="disabled"
                    )
                b.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[k] = b
                idx += 1

        self.update_timer()
        self.next_question()

    def update_timer(self):
        if not self.timer_running:
            return
        elapsed = time.time() - self.start_time
        m = int(elapsed // 60)
        s = elapsed % 60
        self.timer_label.config(text=f"Tiempo: {m:02}:{s:04.1f}")
        self.root.after(100, self.update_timer)

    def next_question(self):
        if not self.remaining:
            self.meaning_label.config(text="¡Extra completado!")
            self.timer_running = False
            return
        self.target = random.choice(list(self.remaining))
        self.meaning_label.config(text=kanji_dict[self.target])

    def check_answer(self, clicked):
        if clicked != self.target:
            self.intentos[self.target] += 1
            if self.intentos[self.target] == 3:
                self.buttons[self.target].config(bg=COLOR_FAIL)
                self.remaining.remove(self.target)
                self.next_question()
            return

        # Acierto
        self.intentos[self.target] += 1
        n = self.intentos[self.target]
        if n == 1:
            self.buttons[self.target].config(bg=COLOR_1)
        elif n == 2:
            self.buttons[self.target].config(bg=COLOR_2)
        else:
            self.buttons[self.target].config(bg=COLOR_3)
        self.remaining.remove(self.target)
        self.next_question()

# --------------------------------------------------------------------------
# --------------------------- JUEGO PRINCIPAL ------------------------------
# --------------------------------------------------------------------------
class KanjiQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Entrenador de Kanji")

        self.total_clicks = 0
        self.total_aciertos = 0
        self.intentos = {k: 0 for k in kanji_dict}
        self.remaining = set(kanji_dict.keys())
        self.failures = []

        self.start_time = time.time()
        self.timer_running = True

        # === Label del significado (solo, sin imágenes) ===
        self.meaning_label = tk.Label(root, text="", font=("Arial", 18))
        self.meaning_label.pack(pady=15)

        # === Frame para timer y score con imágenes a los lados ===
        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=5)

        try:
            img = Image.open("icon_left.png").resize((100, 144), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(stats_frame, image=photo).pack(side="left", padx=20)
            self.root.image_left = photo
        except:
            pass

        # Timer y Score juntos en el centro
        center_frame = tk.Frame(stats_frame)
        center_frame.pack(side="left")
        
        self.timer_label = tk.Label(center_frame, text="Tiempo: 00:00.0", font=("Arial", 16))
        self.timer_label.pack()
        
        self.score_label = tk.Label(center_frame, text="Acierto: 0%", font=("Arial", 16))
        self.score_label.pack(pady=5)

        try:
            img = Image.open("icon_right.png").resize((100, 144), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(stats_frame, image=photo).pack(side="right", padx=20)
            self.root.image_right = photo
        except:
            pass

        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)

        self.buttons = {}
        kanjis = list(kanji_dict.keys())
        idx = 0
        for r in range(7):
            for c in range(7):
                k = kanjis[idx]
                b = tk.Button(
                    self.grid_frame,
                    text=k,
                    font=("Arial", 24),
                    width=3,
                    height=1,
                    command=lambda x=k: self.check_answer(x)
                )
                b.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[k] = b
                idx += 1

        self.update_timer()
        self.next_question()

    def update_timer(self):
        if not self.timer_running:
            return
        elapsed = time.time() - self.start_time
        m = int(elapsed // 60)
        s = elapsed % 60
        self.timer_label.config(text=f"Tiempo: {m:02}:{s:04.1f}")
        self.root.after(100, self.update_timer)

    def update_score(self):
        pct = 0 if self.total_clicks == 0 else (100 * self.total_aciertos / self.total_clicks)
        self.score_label.config(text=f"Acierto: {pct:.1f}%")

    def next_question(self):
        if not self.remaining:
            self.meaning_label.config(text="¡Completado!")
            self.timer_running = False
            self.after_finished()
            return
        self.target = random.choice(list(self.remaining))
        self.meaning_label.config(text=kanji_dict[self.target])

    def after_finished(self):
        failed = [k for k in self.intentos if self.intentos[k] >= 3]
        if not failed:
            msg = tk.Label(self.root, text="No hubo fallos totales", font=("Arial", 18))
            msg.pack(pady=10)
        else:
            ExtraWindow(failed)

    def check_answer(self, clicked):
        self.total_clicks += 1

        if clicked == self.target:
            self.total_aciertos += 1
            self.intentos[self.target] += 1
            n = self.intentos[self.target]
            if n == 1:
                self.buttons[self.target].config(bg=COLOR_1)
            elif n == 2:
                self.buttons[self.target].config(bg=COLOR_2)
            else:
                self.buttons[self.target].config(bg=COLOR_3)
            self.intentos[self.target] = n
            self.remaining.remove(self.target)
            self.update_score()
            self.next_question()
            return

        # FALLO
        else:
            self.intentos[self.target] += 1
            if self.intentos[self.target] == 3:
                self.buttons[self.target].config(bg=COLOR_FAIL)
                self.remaining.remove(self.target)
                self.update_score()
                self.next_question()
                return
        self.update_score()

# ---------------- EJECUCIÓN ----------------
root = tk.Tk()
app = KanjiQuiz(root)
root.mainloop()