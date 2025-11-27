import streamlit as st
import random
import time

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

# --- CONFIGURACIÓN DE SESIÓN ---
if "remaining" not in st.session_state:
    st.session_state.remaining = list(kanji_dict.keys())
    st.session_state.intentos = {k: 0 for k in kanji_dict}
    st.session_state.total_clicks = 0
    st.session_state.total_aciertos = 0
    st.session_state.start_time = time.time()
    st.session_state.target = random.choice(st.session_state.remaining)

# --- FUNCIONES ---
def next_question():
    if not st.session_state.remaining:
        st.session_state.target = None
    else:
        st.session_state.target = random.choice(st.session_state.remaining)

def check_answer(clicked):
    st.session_state.total_clicks += 1
    if clicked == st.session_state.target:
        st.session_state.total_aciertos += 1
        st.session_state.intentos[st.session_state.target] += 1
        st.session_state.remaining.remove(st.session_state.target)
        next_question()
    else:
        st.session_state.intentos[st.session_state.target] += 1
        if st.session_state.intentos[st.session_state.target] >= 3:
            st.session_state.remaining.remove(st.session_state.target)
            next_question()

# --- INTERFAZ ---
st.title("Entrenador de Kanji (versión web)")

elapsed = time.time() - st.session_state.start_time
m = int(elapsed // 60)
s = elapsed % 60
st.write(f"⏱ Tiempo: {m:02}:{s:04.1f}")

if st.session_state.total_clicks > 0:
    pct = 100 * st.session_state.total_aciertos / st.session_state.total_clicks
else:
    pct = 0
st.write(f"✅ Acierto: {pct:.1f}%")

if st.session_state.target is None:
    st.success("¡Completado!")
else:
    st.subheader("Significado:")
    st.write(kanji_dict[st.session_state.target])

    cols = st.columns(7)
    kanjis = list(kanji_dict.keys())
    idx = 0
    for r in range(7):
        for c in range(7):
            k = kanjis[idx]
            if k in st.session_state.remaining or k == st.session_state.target:
                if cols[c].button(k, key=f"{r}-{c}"):
                    check_answer(k)
            else:
                cols[c].button(" ", key=f"{r}-{c}", disabled=True)
            idx += 1
