# AR Recurrence Lab

An open web-based augmented reality (WebAR) learning environment for recurrence analysis of financial market crashes.
Students explore three-dimensional phase-space trajectories, stacks of recurrence plots and recurrence quantification surfaces of real crashes on the S&P 500, Brent crude oil and BTC-USD markets, on their own smartphones and without installing an application.

**Live demo:** https://butman2099.github.io/AR-Recurrence-Lab/

It extends the laboratory work on recurrence analysis of the open textbook *Modeling Complex Systems in Python* (V. N. Soloviev, A. O. Bielinskyi; [online version](https://butman2099.github.io/Complex-systems-book/), [notebooks and sources](https://github.com/Butman2099/Complex-systems-book)).

The environment accompanies the paper *AR Recurrence Lab: an augmented reality learning environment for recognising financial market crashes with recurrence quantification analysis* (A. O. Bielinskyi, V. N. Soloviev, A. V. Matviychuk, V. V. Solovieva, Y. I. Strilchuk, M. A. Tepliuk, V. S. Bezkorovainyi), submitted to AREdu 2026.

## Learning objects

1. **Attractor gallery.** Phase portraits of six crash events at four window positions (calm, early pre-crash, late pre-crash, crash), plus the Lorenz and Rössler systems and a random walk.
2. **Recurrence tunnel.** Twelve recurrence plots along the sliding window, stacked as semi-transparent layers.
3. **RQA landscape.** Determinism DET(t, ε) of BTC-USD in 2017–2018 as a surface over time and threshold.
4. **Time slider.** Synchronised phase portrait, recurrence plot and DET/LAM curves with Predict–Observe–Explain prompts.

AR mode uses WebXR or Scene Viewer on Android and Quick Look on iOS (via [`model-viewer`](https://modelviewer.dev)). On other devices the objects open as interactive 3D views.

## Repository structure

| Path | Content |
|---|---|
| `index.html`, `vendor/`, `models/`, `img/`, `data/` | the web application (served by GitHub Pages) |
| `code/` | Python and Node.js scripts that compute the results, figures and AR models |
| `results/` | computed event catalogue and sliding-window RQA measures |
| `figs/` | output folder for the figures of the paper |

## Parameters

| Item | Setting |
|---|---|
| Windows | Sliding windows of 250 (S&P 500, Brent) and 100 (BTC-USD) observations, step 1 |
| Input | Prices standardised within each window |
| RQA | m = 1, τ = 1, ε = 0.1 window standard deviations, Theiler window 1, l_min = v_min = 2 |
| 3D phase portraits (visualisation only) | m = 3, τ = 9 (S&P 500), 10 (Brent), 5 (BTC-USD) |

## Reproducing the results

Install the requirements:

```bash
pip install numpy pandas scipy matplotlib numba yfinance xlrd trimesh pillow
```

Then run, from the `code/` folder:

```bash
cd code
python download.py ../prices       # S&P 500 and BTC-USD (Yahoo Finance), Brent (EIA)
python events.py                   # crash events and window positions -> ../results/events.json
python rqa.py                      # sliding-window RQA, window values, DET(t, eps) grid -> ../results/
python fig_prices.py               # figures -> ../figs/
python fig_portraits_rps.py
python fig_rqa.py
python build_ar.py                 # GLB models, RP images and data/meta.json for the web application
```

Raw price data are not included. They are downloaded by `download.py`; Yahoo Finance data are subject to Yahoo's terms of use.

To run the web application locally, start a server in the repository root and open http://localhost:8000:

```bash
python -m http.server 8000
```

Opening `index.html` directly from disk does not work, because the page loads `data/meta.json`. AR mode requires HTTPS, which GitHub Pages provides.

## Data sources

- S&P 500 (^GSPC) and BTC-USD daily closing prices: Yahoo Finance.
- Europe Brent spot price FOB, series RBRTE: U.S. Energy Information Administration.
