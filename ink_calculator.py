"""
Ink Consumption Calculator
Specialized for security printing and specialty ink industries.

Formula: Area (m²) × Coverage (%) × Ink Density (g/m²) = Consumption (g)

Supported Printing Methods:
- Offset (Sheet-fed, Heat-set, Cold-set)
- UV Offset
- Flexo UV
- Gravure
- Screen Printing
- Digital
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum
import json

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Ink Calculator",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Constants & Technical Data
# ---------------------------------------------------------------------------

CM2_TO_M2 = 1e-4

class PrintMethod(Enum):
    OFFSET_SHEET_FED = "Offset - Sheet-fed"
    OFFSET_HEAT_SET = "Offset - Heat-set"
    OFFSET_COLD_SET = "Offset - Cold-set"
    UV_OFFSET = "UV Offset"
    UV_FLEXO = "UV Flexo"
    SOLVENT_FLEXO = "Solvent Flexo"
    GRAVURE = "Gravure"
    SCREEN = "Screen Printing"
    DIGITAL_UV = "Digital - UV"
    DIGITAL_AQUEOUS = "Digital - Aqueous"
    DIGITAL_SOLVENT = "Digital - Solvent"
    SECURITY_OVI = "Security - OVI"
    SECURITY_IR = "Security - IR Ink"
    SECURITY_UV_FLUORESCENT = "Security - UV Fluorescent"
    SECURITY_MAGNETIC = "Security - Magnetic"

# Technical specifications from industry standards
# Source: ISO/TS 19857, manufacturer datasheets, industry research
INK_SPECIFICATIONS = {
    PrintMethod.OFFSET_SHEET_FED: {
        "density_range": (0.7, 1.5),
        "typical": 1.0,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "40-100 Pa·s",
        "description": "Oil-based, high viscosity ink for paper printing",
    },
    PrintMethod.OFFSET_HEAT_SET: {
        "density_range": (0.8, 1.4),
        "typical": 1.1,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "40-100 Pa·s",
        "description": "Web offset with heat drying",
    },
    PrintMethod.OFFSET_COLD_SET: {
        "density_range": (0.6, 1.2),
        "typical": 0.9,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "40-100 Pa·s",
        "description": "Newsprint, penetration drying",
    },
    PrintMethod.UV_OFFSET: {
        "density_range": (0.9, 1.6),
        "typical": 1.2,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "5-20 Pa·s",
        "description": "Instant curing, high gloss",
    },
    PrintMethod.UV_FLEXO: {
        "density_range": (0.9, 2.5),
        "typical": 1.4,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.4-1.0 Pa·s",
        "anilox_range": "2.8-8.0 cm³/m²",
        "description": "Low viscosity, for labels and packaging",
        "variants": {
            "Process Printing": {"density": (0.9, 1.4), "anilox": "3.0-4.5"},
            "Screen Fine": {"density": (0.9, 1.0), "anilox": "2.8-3.5"},
            "Screen Coarse": {"density": (1.2, 1.5), "anilox": "3.0-6.0"},
            "Lines Fine": {"density": (1.0, 1.5), "anilox": "2.8-4.0"},
            "Lines Coarse": {"density": (1.5, 2.0), "anilox": "3.5-6.0"},
            "Solid Areas": {"density": (1.5, 2.5), "anilox": "4.0-8.0"},
        }
    },
    PrintMethod.SOLVENT_FLEXO: {
        "density_range": (1.0, 2.0),
        "typical": 1.5,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.1-0.5 Pa·s",
        "description": "For flexible packaging, PE/PP films",
    },
    PrintMethod.GRAVURE: {
        "density_range": (1.5, 4.0),
        "typical": 2.5,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.01-0.1 Pa·s",
        "description": "High density, solvent or water-based",
    },
    PrintMethod.SCREEN: {
        "density_range": (5.0, 20.0),
        "typical": 10.0,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "1-10 Pa·s",
        "description": "Heavy deposit, security applications",
    },
    PrintMethod.DIGITAL_UV: {
        "density_range": (1.0, 2.0),
        "typical": 1.5,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.01-0.05 Pa·s",
        "description": "Piezoelectric inkjet, UV curable",
    },
    PrintMethod.DIGITAL_AQUEOUS: {
        "density_range": (0.8, 1.5),
        "typical": 1.1,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.001-0.01 Pa·s",
        "description": "Water-based dye/pigment inks",
    },
    PrintMethod.DIGITAL_SOLVENT: {
        "density_range": (1.2, 2.0),
        "typical": 1.6,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "0.01-0.05 Pa·s",
        "description": "For uncoated vinyl and banners",
    },
    PrintMethod.SECURITY_OVI: {
        "density_range": (2.0, 4.0),
        "typical": 3.0,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "2-5 Pa·s",
        "description": "Optically Variable Ink - screen/offset",
    },
    PrintMethod.SECURITY_IR: {
        "density_range": (1.5, 3.0),
        "typical": 2.0,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "2-5 Pa·s",
        "description": "Infrared absorbing ink",
    },
    PrintMethod.SECURITY_UV_FLUORESCENT: {
        "density_range": (1.0, 2.5),
        "typical": 1.8,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "2-5 Pa·s",
        "description": "Visible under UV light",
    },
    PrintMethod.SECURITY_MAGNETIC: {
        "density_range": (2.0, 4.0),
        "typical": 3.0,
        "coverage_factor": 1.0,
        "unit": "g/m²",
        "viscosity": "5-10 Pa·s",
        "description": "MICR encoding",
    },
}

# Pantone mixing base specifications
BASE_COLOR_SPECIFICATIONS = {
    "C (Cyan)": {
        "typical_density": 1.2,
        "price_range": (80, 150),
        "pigment_content": "18-22%",
        "lightfastness": "7-8",
    },
    "M (Magenta)": {
        "typical_density": 1.25,
        "price_range": (90, 160),
        "pigment_content": "15-20%",
        "lightfastness": "6-7",
    },
    "Y (Yellow)": {
        "typical_density": 1.1,
        "price_range": (70, 130),
        "pigment_content": "12-16%",
        "lightfastness": "6-7",
    },
    "K (Black)": {
        "typical_density": 1.4,
        "price_range": (60, 110),
        "pigment_content": "20-25%",
        "lightfastness": "8",
    },
    "Orange": {
        "typical_density": 1.3,
        "price_range": (100, 180),
        "pigment_content": "15-20%",
        "lightfastness": "6-7",
    },
    "Green": {
        "typical_density": 1.25,
        "price_range": (100, 180),
        "pigment_content": "15-20%",
        "lightfastness": "7",
    },
    "Violet": {
        "typical_density": 1.3,
        "price_range": (120, 200),
        "pigment_content": "15-20%",
        "lightfastness": "6-7",
    },
    "Special": {
        "typical_density": 1.5,
        "price_range": (150, 400),
        "pigment_content": "Variable",
        "lightfastness": "Variable",
    },
}

DEFAULT_PANTONE_FORMULAS = {
    "185 C (Red)": {"C": 0, "M": 80, "Y": 90, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "2945 C (Blue)": {"C": 100, "M": 45, "Y": 0, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "375 C (Green)": {"C": 60, "M": 0, "Y": 100, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "130 C (Orange)": {"C": 0, "M": 30, "Y": 100, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "Process Cyan": {"C": 100, "M": 0, "Y": 0, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "Process Magenta": {"C": 0, "M": 100, "Y": 0, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "Process Yellow": {"C": 0, "M": 0, "Y": 100, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
    "Process Black": {"C": 0, "M": 0, "Y": 0, "K": 100, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0},
}

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ConsumptionResult:
    print_method: PrintMethod
    area_cm2: float
    area_m2: float
    coverage: float
    ink_density: float
    quantity: int
    waste_rate: float
    ink_price_per_kg: float
    anilox_volume: Optional[float] = None
    substrate_factor: float = 1.0
    
    @property
    def base_consumption_g(self) -> float:
        return self.area_m2 * (self.coverage / 100) * self.ink_density * self.substrate_factor
    
    @property
    def actual_consumption_g(self) -> float:
        return self.base_consumption_g * (1 + self.waste_rate / 100)
    
    @property
    def total_consumption_kg(self) -> float:
        return (self.actual_consumption_g * self.quantity) / 1000
    
    @property
    def total_cost(self) -> float:
        return self.total_consumption_kg * self.ink_price_per_kg
    
    @property
    def unit_cost(self) -> float:
        return self.total_cost / self.quantity if self.quantity > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "print_method": self.print_method.value,
            "area_cm2": round(self.area_cm2, 2),
            "area_m2": round(self.area_m2, 6),
            "coverage_pct": self.coverage,
            "ink_density_g_m2": self.ink_density,
            "quantity": self.quantity,
            "waste_rate_pct": self.waste_rate,
            "ink_price_per_kg": self.ink_price_per_kg,
            "substrate_factor": self.substrate_factor,
            "consumption_per_print_g": round(self.actual_consumption_g, 4),
            "total_consumption_kg": round(self.total_consumption_kg, 4),
            "total_cost": round(self.total_cost, 2),
            "unit_cost": round(self.unit_cost, 4),
        }


@dataclass
class PantoneMixture:
    name: str
    total_kg: float
    components: Dict[str, float]
    unit_prices: Dict[str, float]
    
    @property
    def total_percentage(self) -> float:
        return sum(self.components.values())
    
    @property
    def is_valid(self) -> bool:
        return abs(self.total_percentage - 100) < 0.01
    
    def calculate_costs(self) -> List[Dict]:
        results = []
        for color, percentage in self.components.items():
            if percentage > 0:
                weight_kg = self.total_kg * (percentage / 100)
                unit_price = self.unit_prices.get(color, 0)
                cost = weight_kg * unit_price
                results.append({
                    "color": color,
                    "percentage": percentage,
                    "weight_kg": round(weight_kg, 4),
                    "unit_price": unit_price,
                    "cost": round(cost, 2),
                })
        return results
    
    @property
    def total_cost(self) -> float:
        return sum(item["cost"] for item in self.calculate_costs())
    
    @property
    def unit_cost(self) -> float:
        return self.total_cost / self.total_kg if self.total_kg > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mixture_name": self.name,
            "total_weight_kg": self.total_kg,
            "unit_cost_per_kg": round(self.unit_cost, 2),
            "total_cost": round(self.total_cost, 2),
            "formula": json.dumps(self.components),
        }


# ---------------------------------------------------------------------------
# Session State Management
# ---------------------------------------------------------------------------

def init_session_state():
    defaults = {
        "consumption_history": [],
        "pantone_history": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# UI Components
# ---------------------------------------------------------------------------

def render_header():
    st.title("Ink Consumption Calculator")
    st.caption("Security Printing & Specialty Ink Industry Tool")
    st.markdown("---")


def render_print_method_selector() -> Tuple[PrintMethod, Dict]:
    st.subheader("Printing Method")
    
    method = st.selectbox(
        "Select printing method",
        options=list(PrintMethod),
        format_func=lambda x: x.value
    )
    
    specs = INK_SPECIFICATIONS[method]
    
    with st.expander("Technical Specifications"):
        st.markdown(f"""
        **Description:** {specs['description']}  
        **Density Range:** {specs['density_range'][0]} - {specs['density_range'][1]} {specs['unit']}  
        **Typical Value:** {specs['typical']} {specs['unit']}  
        **Viscosity:** {specs.get('viscosity', 'N/A')}
        """)
        
        if 'variants' in specs:
            st.markdown("**Variants:**")
            for variant, data in specs['variants'].items():
                st.markdown(f"- {variant}: {data['density'][0]}-{data['density'][1]} g/m²")
    
    return method, specs


def render_consumption_tab():
    st.header("Ink Consumption Calculation")
    
    st.markdown("""
    **Formula:** `Area (m²) × Coverage (%) × Ink Density (g/m²) × Substrate Factor = Consumption (g)`
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        method, specs = render_print_method_selector()
        
        st.markdown("---")
        st.subheader("Print Parameters")
        
        calc_method = st.radio(
            "Area input",
            ["Width × Height", "Direct Area (cm²)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if calc_method == "Width × Height":
            w_col, h_col = st.columns(2)
            with w_col:
                width = st.number_input("Width (cm)", min_value=0.01, value=21.0, step=0.1, format="%.2f")
            with h_col:
                height = st.number_input("Height (cm)", min_value=0.01, value=29.7, step=0.1, format="%.2f")
            area = width * height
            st.text(f"Area: {area:.2f} cm²")
        else:
            area = st.number_input("Area (cm²)", min_value=0.01, value=623.7, step=0.1, format="%.2f")
        
        coverage = st.slider("Ink Coverage (%)", 0, 100, 50, help="Percentage of area covered by ink")
        
        # Density selection with method-specific defaults
        density_col1, density_col2 = st.columns([2, 1])
        with density_col1:
            use_variant = False
            variant_name = None
            
            if 'variants' in specs:
                variant_name = st.selectbox("Print Type", list(specs['variants'].keys()))
                variant_data = specs['variants'][variant_name]
                default_density = (variant_data['density'][0] + variant_data['density'][1]) / 2
                use_variant = True
            else:
                default_density = specs['typical']
            
            ink_density = st.number_input(
                "Ink Density (g/m²)",
                min_value=0.001,
                value=float(default_density),
                step=0.1,
                format="%.3f",
                help=f"Range: {specs['density_range'][0]}-{specs['density_range'][1]} g/m²"
            )
        
        with density_col2:
            st.markdown("**Quick Select**")
            quick_values = [
                specs['density_range'][0],
                specs['typical'],
                specs['density_range'][1]
            ]
            for val in quick_values:
                if st.button(f"{val:.2f}", key=f"dens_{val}"):
                    st.session_state[f"quick_density_{method.name}"] = val
    
    with col2:
        st.subheader("Production Parameters")
        
        quantity = st.number_input("Print Quantity", min_value=1, value=10000, step=1000)
        ink_price = st.number_input("Ink Price (per kg)", min_value=0.01, value=150.0, step=10.0, format="%.2f")
        waste_rate = st.slider("Waste Rate (%)", 0, 30, 5)
        include_waste = st.checkbox("Include Waste", value=True)
        
        st.markdown("---")
        st.subheader("Substrate Factor")
        
        substrate_type = st.selectbox(
            "Substrate Type",
            [
                "Coated Paper (factor: 1.0)",
                "Uncoated Paper (factor: 1.2)",
                "Cardboard (factor: 1.3)",
                "Plastic Film (factor: 0.9)",
                "Metallized (factor: 0.8)",
                "Synthetic Paper (factor: 1.0)",
                "Security Paper (factor: 1.1)",
            ]
        )
        
        substrate_factors = {
            "Coated Paper (factor: 1.0)": 1.0,
            "Uncoated Paper (factor: 1.2)": 1.2,
            "Cardboard (factor: 1.3)": 1.3,
            "Plastic Film (factor: 0.9)": 0.9,
            "Metallized (factor: 0.8)": 0.8,
            "Synthetic Paper (factor: 1.0)": 1.0,
            "Security Paper (factor: 1.1)": 1.1,
        }
        substrate_factor = substrate_factors[substrate_type]
        
        custom_factor = st.checkbox("Custom substrate factor")
        if custom_factor:
            substrate_factor = st.number_input("Factor", min_value=0.1, value=1.0, step=0.1, format="%.2f")
    
    st.markdown("---")
    
    if st.button("Calculate", type="primary", use_container_width=True):
        result = ConsumptionResult(
            print_method=method,
            area_cm2=area,
            area_m2=area * CM2_TO_M2,
            coverage=coverage,
            ink_density=ink_density,
            quantity=quantity,
            waste_rate=waste_rate if include_waste else 0,
            ink_price_per_kg=ink_price,
            substrate_factor=substrate_factor,
        )
        
        st.session_state["consumption_history"].append(result.to_dict())
        
        st.success("Calculation Complete")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        metric_col1.metric("Per Print", f"{result.actual_consumption_g:.3f} g")
        metric_col2.metric("Total", f"{result.total_consumption_kg:.3f} kg")
        metric_col3.metric("Total Cost", f"${result.total_cost:,.2f}")
        metric_col4.metric("Unit Cost", f"${result.unit_cost:.4f}")
        
        with st.expander("Calculation Details"):
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.markdown(f"""
                **Method:** {method.value}
                **Area:** {result.area_cm2:.2f} cm² ({result.area_m2:.6f} m²)
                **Coverage:** {result.coverage}%
                **Ink Density:** {result.ink_density} g/m²
                **Substrate Factor:** {result.substrate_factor}
                **Waste Rate:** {result.waste_rate}%
                """)
            with detail_col2:
                st.markdown(f"""
                **Quantity:** {result.quantity:,}
                **Ink Price:** ${result.ink_price_per_kg:.2f}/kg
                **Formula:** {result.area_m2:.6f} × {result.coverage/100} × {result.ink_density} × {result.substrate_factor}
                **Base Consumption:** {result.base_consumption_g:.4f} g
                **With Waste:** {result.actual_consumption_g:.4f} g
                """)


def render_pantone_tab():
    st.header("Pantone Mixture Cost Calculator")
    
    st.info("Calculate custom ink mixture costs based on component percentages and unit prices.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Base Color Specifications")
        
        # Display base color specs
        with st.expander("View Base Color Technical Data"):
            base_df = []
            for color, data in BASE_COLOR_SPECIFICATIONS.items():
                base_df.append({
                    "Color": color,
                    "Typical Density": data["typical_density"],
                    "Price Range": f"${data['price_range'][0]}-${data['price_range'][1]}",
                    "Pigment Content": data["pigment_content"],
                    "Lightfastness": data["lightfastness"],
                })
            st.dataframe(pd.DataFrame(base_df), hide_index=True, use_container_width=True)
        
        colors = list(BASE_COLOR_SPECIFICATIONS.keys())
        
        st.markdown("---")
        st.subheader("Component Pricing")
        
        price_cols = st.columns(4)
        unit_prices = {}
        
        for i, color in enumerate(colors):
            with price_cols[i % 4]:
                default_price = (BASE_COLOR_SPECIFICATIONS[color]["price_range"][0] + 
                               BASE_COLOR_SPECIFICATIONS[color]["price_range"][1]) / 2
                unit_prices[color] = st.number_input(
                    f"{color}",
                    min_value=1.0,
                    value=float(default_price),
                    step=5.0,
                    format="%.2f",
                    key=f"price_{color}"
                )
        
        st.markdown("---")
        st.subheader("Mixture Formula")
        
        mixture_name = st.text_input("Mixture Name", value="Pantone 185 C")
        total_weight = st.number_input("Total Weight (kg)", min_value=0.001, value=5.0, step=0.5, format="%.3f")
        
        st.markdown("**Component Percentages:**")
        
        pct_cols = st.columns(4)
        components = {}
        
        # Default values for 185 C
        defaults_185c = {"C": 0, "M": 80, "Y": 90, "K": 0, "Orange": 0, "Green": 0, "Violet": 0, "Special": 0}
        
        for i, color in enumerate(colors):
            with pct_cols[i % 4]:
                components[color] = st.number_input(
                    f"{color} %",
                    min_value=0,
                    max_value=100,
                    value=defaults_185c.get(color, 0),
                    step=5,
                    key=f"pct_{color}"
                )
        
        total_pct = sum(components.values())
        if total_pct != 100:
            st.warning(f"Total: {total_pct}% (must be 100%)")
        else:
            st.success(f"Total: {total_pct}%")
    
    with col2:
        st.subheader("Cost Analysis")
        
        if total_pct == 100:
            mixture = PantoneMixture(
                name=mixture_name,
                total_kg=total_weight,
                components=components,
                unit_prices=unit_prices,
            )
            
            costs = mixture.calculate_costs()
            if costs:
                df = pd.DataFrame(costs)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown(f"""
**{mixture.name}**

Total Cost: **${mixture.total_cost:,.2f}**

Unit Cost: **${mixture.unit_cost:,.2f}/kg**
                """)
                
                if st.button("Save Mixture", use_container_width=True):
                    st.session_state["pantone_history"].append(mixture.to_dict())
                    st.success("Saved")
    
    # Preset formulas
    with st.expander("Preset Pantone Formulas"):
        preset_col1, preset_col2 = st.columns(2)
        
        with preset_col1:
            st.markdown("**Standard Formulas:**")
            for name, formula in list(DEFAULT_PANTONE_FORMULAS.items())[:4]:
                active_components = {k: v for k, v in formula.items() if v > 0}
                st.text(f"{name}: {active_components}")
        
        with preset_col2:
            st.markdown("**Process Colors:**")
            for name, formula in list(DEFAULT_PANTONE_FORMULAS.items())[4:]:
                active_components = {k: v for k, v in formula.items() if v > 0}
                st.text(f"{name}: {active_components}")


def render_reference_tab():
    st.header("Technical Reference Data")
    
    tab1, tab2, tab3 = st.tabs(["Print Methods", "Ink Specifications", "Coverage Guidelines"])
    
    with tab1:
        st.subheader("Print Method Comparison")
        
        comparison_data = []
        for method, specs in INK_SPECIFICATIONS.items():
            comparison_data.append({
                "Method": method.value,
                "Typical Density": specs['typical'],
                "Min Density": specs['density_range'][0],
                "Max Density": specs['density_range'][1],
                "Unit": specs['unit'],
                "Viscosity": specs.get('viscosity', 'N/A'),
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Method Descriptions")
        
        for method, specs in INK_SPECIFICATIONS.items():
            with st.expander(f"{method.value}"):
                st.markdown(f"""
**Description:** {specs['description']}

**Technical Data:**
- Density Range: {specs['density_range'][0]} - {specs['density_range'][1]} {specs['unit']}
- Typical Value: {specs['typical']} {specs['unit']}
- Viscosity: {specs.get('viscosity', 'N/A')}
                """)
                
                if 'variants' in specs:
                    st.markdown("**Variants:**")
                    for variant, data in specs['variants'].items():
                        st.markdown(f"- **{variant}:** Density {data['density'][0]}-{data['density'][1]} g/m²")
    
    with tab2:
        st.subheader("Base Color Specifications")
        
        base_data = []
        for color, data in BASE_COLOR_SPECIFICATIONS.items():
            base_data.append({
                "Color": color,
                "Density": data['typical_density'],
                "Min Price": data['price_range'][0],
                "Max Price": data['price_range'][1],
                "Pigment Content": data['pigment_content'],
                "Lightfastness": data['lightfastness'],
            })
        
        st.dataframe(pd.DataFrame(base_data), hide_index=True, use_container_width=True)
    
    with tab3:
        st.subheader("Coverage Guidelines")
        
        st.markdown("""
### Industry Standard Coverage Values

| Coverage Level | Description | Typical Use |
|---------------|-------------|-------------|
| **100%** | Solid area | Backgrounds, solid colors |
| **80%** | Heavy coverage | Deep colors, graphics |
| **50%** | Medium coverage | Halftones, photographs |
| **40%** | Light-medium | Pastel colors |
| **25%** | Light coverage | Highlights, tints |
| **10%** | Very light | Shadows, gradients |

### UV Flexo Specific (ATEC Standards)
| Print Subject | Ink Application | Cell Volume |
|--------------|-----------------|-------------|
| Process Printing | 0.9-1.4 g/m² | 3.0-4.5 cm³/m² |
| Screen Fine | 0.9-1.0 g/m² | 2.8-3.5 cm³/m² |
| Screen Coarse | 1.2-1.5 g/m² | 3.0-6.0 cm³/m² |
| Lines Fine | 1.0-1.5 g/m² | 2.8-4.0 cm³/m² |
| Lines Coarse | 1.5-2.0 g/m² | 3.5-6.0 cm³/m² |
| Solid Areas | 1.5-2.5 g/m² | 4.0-8.0 cm³/m² |

### Offset Printing (ISO/TS 19857)
| Ink Type | Ideal Amount | Print Density |
|----------|--------------|---------------|
| Sheet-fed | 0.7-1.5 g/m² | 1.0-1.4 D |
| Heat-set | 0.8-1.4 g/m² | 1.0-1.3 D |
| Cold-set | 0.6-1.2 g/m² | 0.9-1.2 D |
        """)


def render_history_tab():
    st.header("History & Export")
    
    hist_col1, hist_col2 = st.columns(2)
    
    with hist_col1:
        st.subheader("Consumption Records")
        
        if st.session_state["consumption_history"]:
            df = pd.DataFrame(st.session_state["consumption_history"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Download Consumption CSV",
                csv,
                f"consumption_{datetime.now():%Y%m%d_%H%M%S}.csv",
                "text/csv",
                use_container_width=True
            )
            
            if st.button("Clear Consumption History", use_container_width=True):
                st.session_state["consumption_history"] = []
                st.rerun()
        else:
            st.text("No records")
    
    with hist_col2:
        st.subheader("Pantone Records")
        
        if st.session_state["pantone_history"]:
            df = pd.DataFrame(st.session_state["pantone_history"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Download Pantone CSV",
                csv,
                f"pantone_{datetime.now():%Y%m%d_%H%M%S}.csv",
                "text/csv",
                use_container_width=True
            )
            
            if st.button("Clear Pantone History", use_container_width=True):
                st.session_state["pantone_history"] = []
                st.rerun()
        else:
            st.text("No records")
    
    st.markdown("---")
    st.subheader("Full Export")
    
    if st.session_state["consumption_history"] or st.session_state["pantone_history"]:
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "consumption_records": st.session_state["consumption_history"],
            "pantone_records": st.session_state["pantone_history"],
        }
        
        json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            "Download Full Report (JSON)",
            json_data,
            f"ink_calculator_report_{datetime.now():%Y%m%d_%H%M%S}.json",
            "application/json",
            use_container_width=True
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    init_session_state()
    render_header()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Consumption", 
        "Pantone Mix", 
        "Reference Data",
        "History"
    ])
    
    with tab1:
        render_consumption_tab()
    
    with tab2:
        render_pantone_tab()
    
    with tab3:
        render_reference_tab()
    
    with tab4:
        render_history_tab()
    
    st.markdown("---")
    st.caption("Ink Consumption Calculator | Formula: Area × Coverage × Density × Substrate Factor")


if __name__ == "__main__":
    main()
