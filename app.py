import streamlit as st
import subprocess
import os
import sys
from datetime import datetime

# 1. Конфиг и стиль
st.set_page_config(page_title="Marvel Rivals Tracker", page_icon="🦸‍♂️")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff1f1f 100%);
        color: white;
        font-size: 18px !important;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
        color: white;
    }
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦸‍♂️ Marvel Rivals Meta")
st.write("Твой быстрый доступ к актуальному тир-листу без лишней рекламы.")

# 2. Основная кнопка
if st.button('🔥 ОБНОВИТЬ ДАННЫЕ'):
    # Список прикольных фраз для загрузки
    phrases = ["Прогреваем репульсоры...", "Анализируем винрейты...", "Вламываемся в базу данных...",
               "Пени Паркер одобряет..."]
    import random

    with st.spinner(random.choice(phrases)):
        result = subprocess.run([sys.executable, "screenshoter.py"], capture_output=True, text=True)

        if "SUCCESS" in result.stdout:
            img_path = "tierlist_final.png"
            if os.path.exists(img_path):
                # Показываем время обновления
                now = datetime.now().strftime("%d.%m %H:%M")
                st.success(f"Обновлено в {now}")

                # Показываем само изображение
                st.image(img_path, use_container_width=True)
            else:
                st.error("Файл не найден. Попробуй еще раз.")
        else:
            st.error(f"Ошибка агента: {result.stdout}")

# 3. Полезный футер в колонках
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Источник данных:**")
    st.markdown("[RivalsMeta.com](https://rivalsmeta.com/)")
with col2:
    st.markdown("**Разработка:**")
    st.markdown("[My GitHub](https://github.com/Mumunich)")  # Замени на свою ссылку!

st.caption(f"© {datetime.now().year} Marvel Rivals Meta Tracker")