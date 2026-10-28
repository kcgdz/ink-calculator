<div align="center">

# Ink Calculator
### Every drop. A better estimate.

A focused print-production toolkit for ink consumption, job costing, and custom ink mixtures.

[**Launch the app →**](https://ink-calculator.streamlit.app) · [Report a bug](https://github.com/kcgdz/ink-calculator/issues) · [Suggest a feature](https://github.com/kcgdz/ink-calculator/issues)

![Python](https://img.shields.io/badge/Python-3.10%2B-182b3a?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-087f8c?logo=streamlit&logoColor=white)

</div>

---

## From print brief to production estimate

Set your sheet size, coverage and print method. Adjust ink laydown, substrate and waste for your press. Get consumption and cost estimates, then export your job history.

| Plan the job | Build a mixture | Keep the numbers |
| --- | --- | --- |
| 15 printing methods, including offset, UV flexo, gravure, screen, digital and specialty security inks | Component percentages, individual ink prices and weighted batch costs | Consumption and mixture history with CSV and JSON downloads |

## Start in three steps

```sh
git clone https://github.com/kcgdz/ink-calculator.git
cd ink-calculator
python -m pip install -r requirements.txt
python -m streamlit run ink_calculator.py
```

On Windows, run `setup.bat` once, then `start.bat`. On macOS/Linux, use `python3` if your Python installation requires it. Python 3.10 or newer is recommended.

## How the estimate works

```text
Ink (g) = area (m²) × (coverage / 100) × laydown (g/m²) × substrate factor
Job ink (kg) = ink (g) × quantity × (1 + waste / 100) / 1000
Job cost = job ink (kg) × price per kg
```

For example, an A4 sheet (21 × 29.7 cm), 50% coverage, 1 g/m² laydown, substrate factor 1, 10,000 copies and 5% waste needs **0.327 kg** of ink. At 150 currency units/kg, the estimate is **49.12**.

Use one currency consistently across your prices. Coverage describes the area covered by the selected ink; estimate separate colors separately when planning a multicolor job.

## A toolkit for the pressroom

- **Consumption:** sheet dimensions or direct area, coverage, method presets, custom laydown and substrate factors.
- **UV flexo:** process, fine/coarse screens, fine/coarse lines and solid-area presets.
- **Mixtures:** CMYK plus orange, green, violet and special components, with batch and unit costs.
- **Reference:** compare the included method ranges and coverage guidelines.
- **Export:** save estimates as CSV or download all session records as JSON.

The included technical ranges are starting assumptions, not certified press settings. Mixture percentages are supplied by the user; no branded color recipes or color matching are provided. Validate them against your ink supplier's data and production trials. The g/m² input represents ink laydown per area, rather than volumetric density. History is stored only in the current Streamlit session; download records before leaving.

## Contribute

Have a press-specific correction or a workflow improvement? [Open an issue](https://github.com/kcgdz/ink-calculator/issues) with your print method, substrate, expected result and a reproducible example. For changes, include a short explanation and run the checks below.

```sh
python -m compileall -q ink_calculator.py
python -m unittest discover -s tests
```

If this tool helps your workflow, a star helps other print professionals discover it.
