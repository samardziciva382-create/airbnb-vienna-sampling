# ============================================================
# PRILOG A: Python kod korišćen u analizi
# Tema: Airbnb Beč – uzoračka statistička analiza
# Student: Samardžić Iva (1408/22)
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 0) Podešavanja
# ------------------------------------------------------------
DATA_PATH = "airbnb_vienna.csv"   # <- naziv CSV fajla sa podacima
OUT_DIR = "rezultati"            # folder gde se snimaju tabele i slike
N_SAMPLE = 300                   # veličina uzorka
RANDOM_SEED = 42

os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# 1) Učitavanje i osnovno čišćenje podataka
# ------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

needed_cols = ["price", "accommodates", "room_type", "availability_365", "number_of_reviews"]
df = df[[c for c in needed_cols if c in df.columns]].copy()

# Čišćenje "price" ako je string (npr. "€85")
if df["price"].dtype == "object":
    df["price"] = (
        df["price"].astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Uklanjanje redova sa nedostajućim vrednostima u ključnim kolonama
key_cols = ["price", "accommodates"]
if "room_type" in df.columns:
    key_cols.append("room_type")

df = df.dropna(subset=key_cols)

# Konverzija tipova
df["accommodates"] = pd.to_numeric(df["accommodates"], errors="coerce")
df = df.dropna(subset=["accommodates"])
df["accommodates"] = df["accommodates"].astype(int)

# Izbacivanje nerealnih vrednosti (ako postoje greške u bazi)
df = df[(df["price"] > 0) & (df["price"] < 2000)]

N = len(df)
print(f"Ukupan broj jedinica u populaciji (N): {N}")

# ------------------------------------------------------------
# 2) Deskriptivna statistika + grafikoni
# ------------------------------------------------------------
df["price"].describe().to_csv(os.path.join(OUT_DIR, "deskriptiva_price.csv"))

# Histogram
plt.figure()
plt.hist(df["price"].values, bins=40)
plt.xlabel("Cena noćenja (EUR)")
plt.ylabel("Frekvencija")
plt.title("Histogram cene noćenja u Beču")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "slika_histogram_price.png"), dpi=200)
plt.close()

# Box-plot
plt.figure()
plt.boxplot(df["price"].values, vert=True)
plt.ylabel("Cena noćenja (EUR)")
plt.title("Box-plot dijagram cene noćenja")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "slika_boxplot_price.png"), dpi=200)
plt.close()

# Scatter: price vs accommodates
plt.figure()
plt.scatter(df["accommodates"].values, df["price"].values, alpha=0.35)
plt.xlabel("Kapacitet smeštaja (accommodates)")
plt.ylabel("Cena noćenja (EUR)")
plt.title("Veza između cene noćenja i kapaciteta smeštaja")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "slika_scatter_price_accommodates.png"), dpi=200)
plt.close()

# ------------------------------------------------------------
# 3) Korelacija + heatmap
# ------------------------------------------------------------
num_cols = [c for c in ["price", "accommodates", "availability_365", "number_of_reviews"] if c in df.columns
