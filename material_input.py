import streamlit as st
import pandas as pd
from file_uploader import get_material_from_excel

import streamlit as st

def get_material_inputs(material_names):
    """Ermöglicht die manuelle Eingabe von Materialkosten und Recyclinganteilen."""
    material_data = {}

    for idx, material in enumerate(material_names):  # Hier arbeiten wir direkt mit der Liste
        st.subheader(f"{material}")

        # Holen Sie die Werte aus der Excel-Tabelle
        price, recycling_rate = get_material_from_excel(material)
        
        # Stellen sicher, dass der Recyclinganteil als float ist (falls es ein int oder None ist)
        recycling_rate = float(recycling_rate)

        # Eingabe von Kosten und Recyclinganteil für jedes Material
        cost = st.number_input(f"Kosten pro Einheit für {material} in Franken", value=float(price), min_value=0.0, step=0.1, key=f"cost_{idx}")
        recycling = st.number_input(f"Recyclinganteil für {material} (%)", value=recycling_rate, min_value=0.0, max_value=100.0, step=1.0, key=f"recycling_{idx}")
        
        material_data[material] = {"cost": cost, "recycling": recycling}

    return material_data