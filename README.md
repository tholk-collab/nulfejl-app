# Nulfejl-visualisering

Interaktiv visualisering af, hvad der sker med spændingen på de tre faser i
en 3-faset installation, hvis nul-lederen (PEN) brister. Indtast belastning
i watt for L1, L2 og L3, og se hvordan det neutrale nulpunkt forskyder sig
væk fra centrum — og hvilken spænding hver fase reelt ender med at få.

Beregningen bruger Millmans sætning på tre rent ohmske laster (`Y = P / U_n²`)
og er samme model, der ligger bag eksemplerne i samtalen: en tungt belastet
fase trækker nulpunktet mod sig og får *lavere* spænding, mens en let/ubelastet
fase kan komme op i nærheden af linjespændingen (≈400 V).

## Kør lokalt

```bash
git clone <din-repo-url>
cd nulfejl-app
pip install -r requirements.txt
streamlit run app.py
```

Appen åbner i din browser på `http://localhost:8501`.

## Deploy på Streamlit Community Cloud

1. Push denne mappe til et GitHub-repo (offentligt eller privat).
2. Gå til [share.streamlit.io](https://share.streamlit.io) og log ind med GitHub.
3. Vælg "New app", peg på dit repo og sæt "Main file path" til `app.py`.
4. Klik "Deploy" — appen bygger automatisk ud fra `requirements.txt`.

## Filstruktur

```
nulfejl-app/
├── app.py              # Streamlit-app (UI + diagram)
├── nulfejl_core.py      # Beregningslogik (Millmans sætning), uafhængig af Streamlit
├── requirements.txt     # Python-afhængigheder
└── README.md
```

## Forbehold

Modellen antager rent ohmske laster (varmelegemer, glødepærer, kogeplader).
Elektroniske apparater, motorer og andre ikke-lineære laster kan reagere
anderledes — typisk går de i stykker, længe før den beregnede spænding når
sit fulde udslag.
