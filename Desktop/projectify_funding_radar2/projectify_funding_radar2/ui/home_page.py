"""Ana Sayfa — genel durum ve hızlı başlangıç."""
from __future__ import annotations

import streamlit as st

from config import APP_NAME, APP_VERSION, LOGO_PATH, USER_TYPE_LABELS
from services import count_calls, count_results, has_profile, load_profile, load_project_summary


def render():
    if LOGO_PATH.exists():
        c1, c2 = st.columns([3, 2])
        c1.image(str(LOGO_PATH), use_container_width=True)
        c2.write("")
    else:
        st.title(f"📡 {APP_NAME}")
    st.caption(f"Sürüm {APP_VERSION} — Fon ve hibe çağrısı uygunluk analiz platformu")

    st.markdown(
        "Bu uygulama; **şirket, akademisyen ve girişimci** kullanıcıların profil ve "
        "proje bilgilerini alarak TÜBİTAK, KOSGEB, TÜSEB, Kalkınma Ajansları, AB "
        "programları, Cascade Funding ve sizin ekleyeceğiniz PDF/site linklerinden "
        "destek programlarını tarar, standart bir veri modeline dönüştürür ve "
        "**0–100 arası uygunluk skoru** üretir."
    )

    ut, profile = load_profile()
    project = load_project_summary()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Profil", USER_TYPE_LABELS.get(ut, "—") if ut else "—")
    c2.metric("Proje Özeti", "✓ Var" if project else "—")
    c3.metric("Taranan Çağrı", count_calls())
    c4.metric("Skorlanan Sonuç", count_results())

    st.divider()
    st.subheader("Önerilen adımlar")
    st.markdown(
        "1. **Kullanıcı Profili** sayfasından tipinizi seçip bilgilerinizi girin.\n"
        "2. **Proje Özeti** sayfasında 7 alanı (her biri ≤ 500 karakter) doldurun.\n"
        "3. **Fon Kaynakları**'ndan kaynak seçin veya kendi PDF/link'inizi ekleyin.\n"
        "4. **Tarama ve Analiz**'ten taramayı başlatın.\n"
        "5. **Uygunluk Sonuçları** ve **Raporlar** sayfalarından sonuçları inceleyin/indirin."
    )

    if not has_profile():
        st.info("Henüz bir profil oluşturmadınız. Soldaki menüden **Kullanıcı Profili** ile başlayın.")
