"""
streamlit_app.py
Ana router — yan menü ve sayfa yönlendirmesi (doküman bölüm 22).
"""
from __future__ import annotations

import streamlit as st

from config import APP_NAME, LOGO_PATH, USER_TYPE_LABELS
from database import init_db
from services import load_profile
from ui import (academic_form, company_form, entrepreneur_form, home_page,
                project_summary_form, reports_page, results_dashboard,
                scan_dashboard, source_manager)


MENU = [
    "Ana Sayfa",
    "Kullanıcı Profili",
    "Proje Özeti",
    "Fon Kaynakları",
    "Tarama ve Analiz",
    "Uygunluk Sonuçları",
    "Raporlar",
]


def apply_custom_styles(): #buton renkleri ve ozel stillerle cssden tekrar yapildi.

    #Duruma gore burada selected(secilen),hover(fare ustune getirildiginde) olan yer veya cap degisebilir.

    bg_selected = "#0F2A4A"
    bg_hover = "#00A8C5"
    border_radius = "8px"
    
    custom_css = f"""
    <style>
    /* 1. Radyo menü kapsayıcısındaki aralığı düzenleme */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 6px !important;
    }}

    /* 2. icteki butonlari (radyo yuvarlak noktalarını) gizledigim yer */
    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    /* 3. Genel menudeki butonlarin tasarimi */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        background-color: #F0F2F6 !important;
        border-radius: {border_radius} !important;
        padding: 10px 16px !important;
        border: 1px solid #E0E0E0 !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        width: 100% !important;
        margin: 0 !important;
    }}

    /* Buton icindeki yazi rengini doğrudan hedefleme */
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
        color: #31333F !important;
        margin: 0 !important;
        font-weight: 500 !important;
    }}

    /* 4. Hover tasarimi (Fare ustune getirildiginde) */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: {bg_hover} !important;
        border-color: {bg_hover} !important;
        transform: translateX(4px);
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover p {{
        color: #FFFFFF !important;
    }}

    /* 5. Selected tasarimi (Tiklanip secilmis olan buton) */
    section[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"],
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background-color: {bg_selected} !important;
        border-color: {bg_selected} !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] p,
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def run():
    st.set_page_config(page_title=APP_NAME, page_icon="📡", layout="wide")
    init_db()

    # KISA NOT: CSS stillerini burada cagirmazsak ekrana yansımaz!
    apply_custom_styles()

    with st.sidebar:
        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), use_container_width=True)
        else:
            st.title("📡 Funding Radar")
            
        choice = st.radio("Menü", MENU, label_visibility="collapsed")
        st.divider()
        
        ut, _ = load_profile()
        st.caption(f"Aktif profil: {USER_TYPE_LABELS.get(ut, 'yok') if ut else 'yok'}")

    if choice == "Ana Sayfa":
        home_page.render()
    elif choice == "Kullanıcı Profili":
        _render_profile_section()
    elif choice == "Proje Özeti":
        project_summary_form.render()
    elif choice == "Fon Kaynakları":
        source_manager.render()
    elif choice == "Tarama ve Analiz":
        scan_dashboard.render()
    elif choice == "Uygunluk Sonuçları":
        results_dashboard.render()
    elif choice == "Raporlar":
        reports_page.render()


def _render_profile_section():
    st.header("👤 Kullanıcı Profili")
    ut, _ = load_profile()
    default_idx = {"company": 0, "academic": 1, "entrepreneur": 2}.get(ut, 0)
    label = st.radio(
        "Kullanıcı tipi seçin",
        ["company", "academic", "entrepreneur"],
        index=default_idx,
        format_func=lambda k: USER_TYPE_LABELS[k],
        horizontal=True,
    )
    st.divider()
    if label == "company":
        company_form.render()
    elif label == "academic":
        academic_form.render()
    else:
        entrepreneur_form.render()