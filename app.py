import streamlit as st
import subprocess
import sys
import json
import os

# 1. Центрированный макет
st.set_page_config(page_title="Marvel Rivals Hub", page_icon="🎃️", layout="wide")

# 2. Чистый CSS: добавили ограничение ширины и лоск
st.markdown("""
    <style>
    /* Главный фон — глубокий полночный черный с фиолетовым отливом */
    .stApp {
        background: radial-gradient(circle, #1a0f2e 0%, #050505 100%);
    }

    /* Ограничиваем контент */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    /* Заголовки — неоновый оранжевый с "тлеющим" эффектом */
    h1, h2, h3 {
        color: #ff7518 !important;
        text-shadow: 0 0 10px #ff4500, 0 0 20px #ff7518;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Кнопки — как магические артефакты */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-size: 12px;
        height: 32px;
        background: linear-gradient(135deg, #4b0082 0%, #000000 100%) !important;
        color: #ff7518 !important;
        border: 1px solid #ff7518 !important;
        transition: 0.4s ease-in-out;
        box-shadow: 0 0 5px #4b0082;
    }

    .stButton>button:hover {
        border-color: #ffffff !important;
        color: #ffffff !important;
        box-shadow: 0 0 20px #ff7518;
        transform: translateY(-3px) rotate(-1deg);
    }

    /* Иконки героев — легкое свечение при наведении */
    .stImage {
        transition: 0.5s;
        filter: grayscale(30%);
    }
    .stImage:hover {
        filter: grayscale(0%) drop-shadow(0 0 15px #9400d3);
        transform: scale(1.2);
    }

    /* Вкладки (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ff7518 !important;
        border-radius: 10px 10px 0 0;
        border: 1px solid #4b0082;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #4b0082;
    }

    /* Скриншоты с "рамкой" */
    img {
        border: 2px solid #4b0082;
        border-radius: 15px;
        pointer-events: none;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }

    /* Анимация появления */
    @keyframes ghostFade {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stImage, .stMarkdown {
        animation: ghostFade 1.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🦇 MARVEL RIVALS: HALLOWEEN META 🦇</h1>", unsafe_allow_html=True)


tab_meta, tab_skins = st.tabs(["📊 Тир-листы", "👗 Скины"])

# --- ВКЛАДКА МЕТА ---
with tab_meta:
    # Контейнер для кнопок СВЕРХУ (чтобы они не убегали вниз при появлении скрина)
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

st.caption("Данные обновляются в реальном времени. Сделано на Python.")
