import streamlit as st
import subprocess
import sys
import json
import os
import random

# Центрированный макет
st.set_page_config(page_title="Marvel Rivals Hub", page_icon="🎃️", layout="wide")

# Генерируем 40 светлячков со случайными параметрами
fireflies_html = ""
for i in range(45):  # Сделаем чуть побольше для густоты
    size = random.randint(4, 8)
    pos_left = random.randint(0, 98)
    pos_top = random.randint(0, 98)
    duration = random.randint(15, 30)
    delay = random.randint(0, 20)
    color = "#ff7518" if i % 2 == 0 else "#9400d3"

    fireflies_html += f'<div class="firefly" style="width:{size}px; height:{size}px; top:{pos_top}%; left:{pos_left}%; background:{color}; animation-duration:{duration}s; animation-delay:{delay}s;"></div>'


st.markdown(f"""
    <style>
    /* ГЛАВНЫЙ ФОН (Джефф-тыква) */
    .stApp {{
        background-image: url("https://github.com/Mumunich/marvel-rivals-meta-tracker/raw/main/703948.jpg");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}

    /* КОНТЕНТ: Стеклянная подложка */
    .block-container {{
        max-width: 1100px;
        background: rgba(15, 8, 25, 0.3); 
        border-radius: 25px;
        border: 1px solid rgba(255, 117, 24, 0.3);
        padding: 40px !important;
        margin-top: 2rem;
        box-shadow: 0 0 50px rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(0px);
    }}

    /* ТЛЕЮЩИЙ ЗАГОЛОВОК */
    .halloween-title {{
        color: #ff7518;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 4px;
        animation: flicker 3s infinite alternate;
    }}
    @keyframes flicker {{
        0%, 100% {{ text-shadow: 0 0 10px #ff4500, 0 0 20px #ff7518; }}
        50% {{ text-shadow: 0 0 30px #9400d3, 0 0 15px #ff4500; opacity: 0.9; }}
    }}

    /* КНОПКИ-АРТЕФАКТЫ */
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        font-size: 12px;
        height: 36px;
        background: linear-gradient(135deg, #4b0082 0%, #000000 100%) !important;
        color: #ff7518 !important;
        border: 1px solid #ff7518 !important;
        transition: 0.4s ease-in-out !important;
        box-shadow: 0 0 5px #4b0082;
    }}

    .stButton>button:hover {{
        border-color: #ffffff !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px #ff7518;
        transform: translateY(-3px) rotate(-1deg);
    }}

    /* ИКОНКИ ГЕРОЕВ (Морды) */
    [data-testid="stImage"] {{
        transition: 0.5s !important;
        filter: grayscale(20%);
    }}
    [data-testid="column"]:hover [data-testid="stImage"] {{
        filter: grayscale(0%) drop-shadow(0 0 15px #9400d3);
        transform: scale(1.2) rotate(5deg);
    }}

    /* СВЕТЛЯЧКИ: ФИКСИРОВАННОЕ ПОЗИЦИОНИРОВАНИЕ */
        .firefly {{
        position: fixed !important; /* Ультимативно фиксируем */
        border-radius: 50%;
        pointer-events: none;
        z-index: 999999 !important; /* Поднимаем ВЫШЕ шапки и стекла */
        opacity: 0;
        animation: slowDrift linear infinite, pulseGlow ease-in-out infinite;
    }}

    /* Убираем перекрытие от контейнеров Streamlit */
    iframe {{ z-index: 1; }}
    
    @keyframes slowDrift {{
        0% {{ transform: translate(0, 0); opacity: 0; }}
        10% {{ opacity: 0.8; }}
        100% {{ transform: translate(100px, -600px); opacity: 0; }}
    }}

    @keyframes pulseGlow {{
        0%, 100% {{ filter: blur(2px); box-shadow: 0 0 8px currentColor; }}
        50% {{ filter: blur(5px); box-shadow: 0 0 20px currentColor; }}
    }}
    </style>
    
    {fireflies_html}
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🦇 MARVEL RIVALS: HALLOWEEN META 🦇</h1>", unsafe_allow_html=True)


tab_meta, tab_skins = st.tabs(["📊 Тир-листы", "👗 Скины"])

# --- ВКЛАДКА МЕТА ---
with tab_meta:
    # Контейнер для кнопок СВЕРХУ
    c1, c2 = st.columns(2)

    # Контейнер для результата СНИЗУ
    meta_placeholder = st.container()

    if c1.button("📸 RivalsMeta", use_container_width=True):
        with st.spinner("Загрузка RivalsMeta..."):
            subprocess.run([sys.executable, "screenshoter.py", "https://rivalsmeta.com/tier-list", "meta.png"])
            meta_placeholder.image("meta.png", use_container_width=True)

    if c2.button("📸 RivalsTracker", use_container_width=True):
        with st.spinner("Загрузка RivalsTracker..."):
            subprocess.run([sys.executable, "screenshoter.py", "https://rivalstracker.com/tier-list", "tracker.png"])
            meta_placeholder.image("tracker.png", use_container_width=True)

# --- ВКЛАДКА СКИНЫ ---
with tab_skins:
    # 1. Главный экран (ВСЕГДА СВЕРХУ)
    skin_display = st.empty()

    # 2. Загрузка героев (в кэш сессии)
    if 'heroes_cache' not in st.session_state:
        with st.spinner("Синхронизация героев..."):
            res = subprocess.run([sys.executable, "hero_parser.py", "--meta"], capture_output=True, text=True)
            try:
                # Ищем строку с JSON
                json_str = next(line for line in res.stdout.split('\n') if line.strip().startswith('['))
                st.session_state['heroes_cache'] = json.loads(json_str)
            except:
                st.error("Ошибка связи с базой данных")

    # 3. Витрина героев
    if 'heroes_cache' in st.session_state:
        st.write("---")
        # 6 колонок — идеально для узкого макета
        cols = st.columns(6)
        for idx, hero in enumerate(st.session_state['heroes_cache']):
            with cols[idx % 6]:
                # Четкая иконка (64x64)
                icon_url = hero['icon'].replace("s_32x32", "s_64x64")
                st.image(icon_url, width=64)

                # Кнопка сразу под иконкой
                if st.button("Скины", key=f"btn_{hero['name']}"):
                    # Показываем спиннер прямо над кнопками, чтобы не скроллить
                    with st.spinner(f"💀 Духи доставили свежие скины для {hero['name']}..."):
                        img_path = "current_hero.png"
                        subprocess.run([sys.executable, "hero_parser.py", hero['name'], img_path])
                        if os.path.exists(img_path):
                            # Выводим результат в зарезервированное место НАВЕРХУ
                            skin_display.image(img_path, use_container_width=True)

# --- ФУТЕР  ---
st.markdown("---") # Разделительная линия


st.markdown("""
    <div style="text-align: center; color: rgba(255, 117, 24, 0.6); font-size: 14px; padding: 20px;">
        🕸️ Данные обновляются в реальном времени. Сделано на Python. 🕷️
    </div>
""", unsafe_allow_html=True)
