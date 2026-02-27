# Ink Consumption Calculator

A specialized calculator for security printing and specialty ink industries.

## Formula

```
Consumption (g) = Area (m²) × Coverage (%) × Ink Density (g/m²) × Substrate Factor
```

## Supported Printing Methods

### Offset Printing
| Method | Density (g/m²) | Viscosity |
|--------|---------------|-----------|
| Sheet-fed | 0.7 - 1.5 | 40-100 Pa·s |
| Heat-set | 0.8 - 1.4 | 40-100 Pa·s |
| Cold-set | 0.6 - 1.2 | 40-100 Pa·s |

### UV Printing
| Method | Density (g/m²) | Viscosity |
|--------|---------------|-----------|
| UV Offset | 0.9 - 1.6 | 5-20 Pa·s |
| UV Flexo | 0.9 - 2.5 | 0.4-1.0 Pa·s |
| Process | 0.9 - 1.4 | - |
| Screen Fine | 0.9 - 1.0 | - |
| Screen Coarse | 1.2 - 1.5 | - |
| Lines Coarse | 1.5 - 2.0 | - |
| Solid Areas | 1.5 - 2.5 | - |

### Other Methods
| Method | Density (g/m²) | Viscosity |
|--------|---------------|-----------|
| Solvent Flexo | 1.0 - 2.0 | 0.1-0.5 Pa·s |
| Gravure | 1.5 - 4.0 | 0.01-0.1 Pa·s |
| Screen | 5.0 - 20.0 | 1-10 Pa·s |
| Digital UV | 1.0 - 2.0 | 0.01-0.05 Pa·s |
| Digital Aqueous | 0.8 - 1.5 | 0.001-0.01 Pa·s |
| Digital Solvent | 1.2 - 2.0 | 0.01-0.05 Pa·s |

### Security Inks
| Method | Density (g/m²) | Application |
|--------|---------------|-------------|
| OVI | 2.0 - 4.0 | Screen/Offset |
| IR Ink | 1.5 - 3.0 | Security features |
| UV Fluorescent | 1.0 - 2.5 | Authentication |
| Magnetic | 2.0 - 4.0 | MICR encoding |

## Features

- **15+ Printing Methods**: Offset, UV, Flexo, Gravure, Screen, Digital, Security inks
- **UV Flexo Variants**: Process, Screen (Fine/Coarse), Lines (Fine/Coarse), Solid Areas
- **Substrate Factors**: Coated/Uncoated paper, Cardboard, Plastic, Metallized, Security paper
- **Pantone Mixing**: CMYK + Orange/Green/Violet/Special with cost calculation
- **Technical Reference**: Industry standard data (ISO/TS 19857, ATEC standards)
- **Export**: CSV and JSON formats

## Installation

```bash
# Run setup
setup.bat

# Or manually
python -m venv ink_calculator_env
ink_calculator_env\Scripts\pip install streamlit pandas
```

## Usage

```bash
# Start application
start.bat
```

Open http://localhost:8501 in your browser.

## Data Sources

- ISO/TS 19857 - Colour and transparency of printing ink sets
- ATEC UV Flexo technical specifications
- Industry research papers on ink consumption
- Manufacturer datasheets (Daihei, ATECE, TOKA, etc.)

## File Structure

```
.
├── ink_calculator.py      # Main application (~32KB)
├── start.bat              # Windows launcher
├── setup.bat              # Installation script
└── README.md
```

## Requirements

- Python 3.8+
- Streamlit
- Pandas

## References

1. ISO/TS 19857:2021 - Graphic technology — Colour and transparency of printing ink sets for four-colour printing
2. ATECE UV Flexo Technical Data Sheets
3. Color-Logic FAQ on ink coverage calculations
4. Research: "Effects of ink consumption on print quality" (Cellulose Chem. Technol.)
