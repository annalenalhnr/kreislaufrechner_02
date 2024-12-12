import streamlit as st
import ifcopenshell
import pandas as pd

def upload_and_process_ifc():
    """Lädt die IFC-Datei hoch und extrahiert Materialnamen."""
    uploaded_file = st.file_uploader("Laden Sie Ihre IFC-Datei hoch", type=["ifc"])
    
    if uploaded_file is not None:
        try:
            # Temporäre Datei speichern
            with open("temp.ifc", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # IFC-Modell laden
            ifc_model = ifcopenshell.open("temp.ifc")
            
            # Extrahiere Materialnamen
            material_names = extract_material_names(ifc_model)

            if material_names:
                # Speichern der Materialnamen in Session State
                st.session_state.material_names = material_names
                
                # Materialnamen anzeigen
                material_df = pd.DataFrame({"Material": material_names})
                st.write("Gefundene Materialien:", material_df)

            else:
                st.warning("Keine Materialien in der IFC-Datei gefunden.")
        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der IFC-Datei: {e}")

def extract_material_names(ifc_model):
    """
    Extrahiert Materialnamen aus der IFC-Datei.
    Gibt eine Liste mit Materialnamen zurück.
    """
    material_names = []

    # Gehe alle Relationen von Materialien durch
    for rel in ifc_model.by_type("IfcRelAssociatesMaterial"):
        material = rel.RelatingMaterial
        
        if material and hasattr(material, 'Name') and material.Name:
            material_names.append(material.Name)

    return material_names

def get_material_from_excel(material_name):
    """
    Diese Funktion liest die Excel-Datei und gibt den Preis und Recyclinganteil für das Material zurück.
    """
    # Lade die Excel-Datei mit der richtigen Kopfzeile
    material_df = pd.read_excel("material_infos.xlsx", header=0)

    # Bereinige Materialname und suche nach dem Material
    material_name = material_name.strip().lower()

    # Suche nach der passenden Zeile basierend auf dem Materialnamen
    matching_row = material_df[material_df['Materialname'].str.lower() == material_name]

    if not matching_row.empty:
        # Preis bleibt unverändert
        price = matching_row['Preis'].values[0]
        
        # Recyclinganteil wird direkt als Prozentsatz übernommen (keine Umwandlung in Dezimalform)
        recycling_rate = matching_row['Recyclinganteil'].values[0]  # Wert bleibt als Prozentsatz, z.B. 60%
    else:
        # Standardwerte setzen, wenn das Material nicht gefunden wurde
        price = 0.0
        recycling_rate = 0.0

    return price, recycling_rate