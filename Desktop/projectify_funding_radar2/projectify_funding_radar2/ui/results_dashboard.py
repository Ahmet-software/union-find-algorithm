"""Uygunluk Sonuçları — skor tablosu + detaylı analiz + alt skor grafiği (doküman bölüm 30)."""
from __future__ import annotations

import streamlit as st

from config import SUBSCORE_LABELS, USER_TYPE_LABELS, source_color, weights_for
from reports import summarize
from services import list_results

_STATUS_COLOR = {
    "Çok Uygun": "🟢", "Uygun": "🟢", "Revizyonla Uygun": "🟡",
    "Düşük Uygunluk": "🟠", "Uygun Değil": "🔴",
}


def _badge(text: str, color: str) -> str:
    return (f"<span style='background:{color};color:#fff;padding:2px 8px;"
            f"border-radius:10px;font-size:0.78em;font-weight:600;white-space:nowrap'>"
            f"{text}</span>")


def render():
    st.subheader("📊 Uygunluk Sonuçları")
    results = list_results()
    if not results:
        st.info("Henüz skorlanmış sonuç yok. **Tarama ve Analiz** sayfasından eşleştirme yapın.")
        return

    s = summarize(results)
    cols = st.columns(5)
    cols[0].metric("Toplam", s["total"])
    cols[1].metric("🟢 Çok Uygun", s["cok_uygun"])
    cols[2].metric("🟢 Uygun", s["uygun"])
    cols[3].metric("🟡 Revizyonla", s["revizyonla"])
    cols[4].metric("🔴 Uygun Değil", s["uygun_degil"] + s["dusuk"])

    st.markdown("#### Skor tablosu")
    # Kaynak renk açıklaması (lejant)
    sources_present = []
    for r in results:
        if r.source_name not in sources_present:
            sources_present.append(r.source_name)
    legend = " ".join(_badge(s, source_color(s)) for s in sources_present)
    st.markdown("Kaynaklar: " + legend, unsafe_allow_html=True)

    table = [
        {
            "Program": r.call_title,
            "Kaynak": r.source_name,
            "Tip": USER_TYPE_LABELS.get(r.matched_user_type, r.matched_user_type),
            "Skor": r.total_score,
            "Durum": f"{_STATUS_COLOR.get(r.status,'')} {r.status}",
            "Son Tarih": r.deadline or "-",
        }
        for r in results
    ]
    _styled_table(table)

    st.markdown("#### Detaylı analiz")
    for r in results:
        with st.expander(f"{_STATUS_COLOR.get(r.status,'')} {r.total_score}/100 — {r.call_title}"):
            top = st.columns(4)
            top[0].metric("Skor", f"{r.total_score}/100")
            top[1].write(f"**Durum:** {r.status}")
            top[2].markdown(f"**Kaynak:** {_badge(r.source_name, source_color(r.source_name))}",
                            unsafe_allow_html=True)
            top[3].write(f"**Son tarih:** {r.deadline or '-'}")
            if r.institution:
                st.caption(f"Kurum: {r.institution}")

            if r.funding_amount or r.funding_rate:
                st.write(f"**Destek:** {r.funding_amount or '-'} / oran {r.funding_rate or '-'}")

            # --- Alt skor grafiği ---
            _render_subscore_chart(r)

            _list_block("✅ Güçlü yönler", r.strengths)
            _list_block("⚠️ Zayıf yönler", r.weaknesses)
            _list_block("🚨 Riskler", r.risks)
            _list_block("📄 Eksik belgeler", r.missing_documents)
            _list_block("🔎 Doğrulanması gerekenler", r.required_checks)
            _list_block("✏️ Revizyon önerileri", r.project_revision_suggestions)

            st.info(f"**Önerilen ilk aksiyon:** {r.recommended_action}")
            link_cols = st.columns(2)
            if r.application_url:
                link_cols[0].markdown(f"[Başvuru linki]({r.application_url})")
            if r.guide_url:
                link_cols[1].markdown(f"[Rehber linki]({r.guide_url})")


def _render_subscore_chart(result):
    """Alt skorları, her kriterin maksimum puanına göre yatay çubuk grafikle gösterir."""
    sub = result.subscores or {}
    if not sub:
        return
    weights = weights_for(result.matched_user_type)

    rows = []
    for key, val in sub.items():
        label = SUBSCORE_LABELS.get(key, key)
        maxv = weights.get(key, 0) or max(val, 1)
        ratio = (val / maxv) if maxv else 0
        rows.append({"Kriter": label, "Puan": round(float(val), 1),
                     "Maks": float(maxv), "Oran": ratio,
                     "Etiket": f"{round(float(val),1):g} / {int(maxv)}"})

    st.markdown("**Alt skor dağılımı**")
    try:
        import altair as alt
        import pandas as pd

        df = pd.DataFrame(rows)
        order = df["Kriter"].tolist()

        base = alt.Chart(df).encode(
            y=alt.Y("Kriter:N", sort=order, title=None,
                    axis=alt.Axis(labelLimit=220, labelFontSize=11)),
        )
        # arka plan (maksimum) çubuğu
        bg = base.mark_bar(color="#e6ecf2", cornerRadius=3).encode(
            x=alt.X("Maks:Q", title="Puan", scale=alt.Scale(domain=[0, df["Maks"].max()]))
        )
        # alınan puan çubuğu (orana göre renk)
        fg = base.mark_bar(cornerRadius=3).encode(
            x=alt.X("Puan:Q"),
            color=alt.Color("Oran:Q",
                            scale=alt.Scale(scheme="redyellowgreen", domain=[0, 1]),
                            legend=None),
            tooltip=["Kriter", "Etiket", alt.Tooltip("Oran:Q", format=".0%")],
        )
        text = base.mark_text(align="left", dx=4, fontSize=10, color="#333").encode(
            x=alt.X("Maks:Q"), text="Etiket:N"
        )
        chart = (bg + fg + text).properties(height=max(120, 26 * len(rows)))
        st.altair_chart(chart, use_container_width=True)
    except Exception:  # noqa: BLE001 — Altair yoksa basit tabloya düş
        st.bar_chart({row["Kriter"]: row["Puan"] for row in rows})


def _styled_table(table):
    """Kaynak sütununu kaynağa göre renklendirerek tabloyu gösterir."""
    try:
        import pandas as pd

        df = pd.DataFrame(table)

        def _color_source(val):
            c = source_color(val)
            return f"background-color:{c};color:white;font-weight:600;border-radius:4px"

        styler = df.style.applymap(_color_source, subset=["Kaynak"])
        st.dataframe(styler, use_container_width=True, hide_index=True)
    except Exception:  # noqa: BLE001
        st.dataframe(table, use_container_width=True, hide_index=True)


def _list_block(title: str, items):
    if items:
        st.markdown(f"**{title}**")
        for it in items:
            st.write(f"• {it}")
