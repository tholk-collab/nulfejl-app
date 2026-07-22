"""
Interaktiv visualisering af nulfejl (PEN-brud) i en 3-faset installation.
Indtast belastning i watt for hver fase, og se hvordan det neutrale
nulpunkt forskyder sig, og hvilken spænding hver fase reelt får.
"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from nulfejl_core import fase_spaendinger

st.set_page_config(page_title="Nulfejl-visualisering", layout="wide")

st.title("Nulfejl i 3-faset installation")
st.markdown(
    "Indtast belastningen (i **watt**) på hver fase for at se, hvordan det "
    "neutrale nulpunkt forskyder sig, hvis PEN/nul-lederen brister. "
    "Beregningen antager rent ohmske laster og bruger Millmans sætning."
)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    p1_col, _ = st.columns([1, 1])
    with p1_col:
        p1 = st.number_input("L1 – belastning (W)", min_value=0, max_value=20000,
                              value=10580, step=50)
with col2:
    p2_col, _ = st.columns([1, 1])
    with p2_col:
        p2 = st.number_input("L2 – belastning (W)", min_value=0, max_value=20000,
                              value=2645, step=50)
with col3:
    p3_col, _ = st.columns([1, 1])
    with p3_col:
        p3 = st.number_input("L3 – belastning (W)", min_value=0, max_value=20000,
                              value=53, step=10)

u_n = st.slider("Nominel fasespænding U_n (V)", 200, 250, 230)

res = fase_spaendinger(p1, p2, p3, u_n=u_n)

if res["udefineret"]:
    st.warning("Ingen belastning på nogen fase — nulpunktets position er "
               "udefineret i denne model. Sæt mindst én fase > 0 W.")
else:
    diagram_col, resultat_col = st.columns([2, 3], gap="large")

    # --- Tegn fasediagrammet ---
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.set_aspect("equal")

    r_normal = u_n
    r_linje = res["linjespaending"]
    grænse = r_linje * 1.15

    # Referencecirkler
    ax.add_patch(plt.Circle((0, 0), r_normal, fill=False, linestyle="--",
                             linewidth=0.8, color="gray"))
    ax.add_patch(plt.Circle((0, 0), r_linje, fill=False, linestyle="--",
                             linewidth=0.8, color="gray"))
    ax.text(0, r_normal + 8, f"{u_n:.0f} V (normalt)", ha="center",
            fontsize=8, color="gray")
    ax.text(0, r_linje + 8, f"≈{r_linje:.0f} V (linjespænding)", ha="center",
            fontsize=8, color="gray")

    # Faste fasepunkter (O = origo er det faste, teoretiske centrum)
    farver = {"L1": "#185FA5", "L2": "#0F6E56", "L3": "#993C1D"}
    labels = ["L1", "L2", "L3"]
    v_n = res["v_n"]

    ax.plot(v_n.real, v_n.imag, "o", color="black", markersize=6)
    ax.text(v_n.real + 8, v_n.imag + 8, "N", fontsize=10, fontweight="bold")

    # Tynd, diskret linje der viser berøringsspændingen (afstand O til N)
    ax.plot([0, v_n.real], [0, v_n.imag], "-", color="#7C3AED",
             linewidth=1, alpha=0.5, zorder=1)

    for i, (vertex, u_last) in enumerate(zip(res["vertices"], res["u_load"])):
        navn = labels[i]
        farve = farver[navn]
        ax.plot(vertex.real, vertex.imag, "o", color=farve, markersize=5)
        offset = 1.22
        ax.text(vertex.real * offset, vertex.imag * offset, navn,
                color=farve, fontsize=12, fontweight="bold", ha="center")
        ax.annotate(
            "", xy=(vertex.real, vertex.imag), xytext=(v_n.real, v_n.imag),
            arrowprops=dict(arrowstyle="-|>", color=farve, lw=2),
        )
        midt = (vertex + v_n) / 2
        ax.text(midt.real, midt.imag, f"{u_last:.0f} V", fontsize=9,
                color=farve, ha="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.7, pad=1))

    ax.set_xlim(-grænse, grænse)
    ax.set_ylim(-grænse, grænse)
    ax.axis("off")

    with diagram_col:
        st.pyplot(fig, use_container_width=False)

    # --- Resultattabel med farvekodede advarsler ---
    with resultat_col:
        st.subheader("Spænding pr. fase")
        boks_col, _ = st.columns([1, 1])
        with boks_col:
            for navn, u_last, p in zip(labels, res["u_load"], [p1, p2, p3]):
                if u_last > 250 or u_last < 200:
                    st.error(f"**{navn}** ({p:.0f} W): {u_last:.1f} V ⚠️ uden for normalområde")
                else:
                    st.success(f"**{navn}** ({p:.0f} W): {u_last:.1f} V")

            beroering = res["beroeringsspaending"]
            if beroering > 50:
                st.error(f"**Berøringsspænding** (kabinet mod jord): {beroering:.1f} V ⚠️ over 50V-grænsen")
            else:
                st.success(f"**Berøringsspænding** (kabinet mod jord): {beroering:.1f} V")

        st.caption(
            "Bemærk: modellen antager rent ohmske laster (varmelegemer, "
            "glødepærer o.l.). Elektroniske apparater og motorer kan reagere "
            "anderledes og ofte gå i stykker før den beregnede spænding når "
            "sit fulde udslag."
        )
