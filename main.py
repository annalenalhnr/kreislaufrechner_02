import streamlit as st
from file_uploader import upload_and_process_ifc  # Funktion für das Hochladen und Verarbeiten der IFC-Datei
from material_input import get_material_inputs  # Für die Eingabe von Kosten und Recyclinganteilen
from calculations import calculate_costs_and_recycling  # Berechnungen der Ergebnisse
from visualization import plot_results, plot_pie_chart  # Für die Visualisierung der Ergebnisse

def main():
    if "page" not in st.session_state:
        st.session_state.page = "start"  # Neue Startseite als Anfang

    if st.session_state.page == "start":
        start_page()
    elif st.session_state.page == "upload":
        upload_page()
    elif st.session_state.page == "input":
        input_page()
    elif st.session_state.page == "results":
        results_page()

def start_page():
    """Einführung und Programmbeschreibung mit rechtsbündigem Logo."""
    col1, col2 = st.columns([1.5, 2.5])  # Linke Spalte für Text, rechte Spalte für das Logo
    
    with col2:
        st.markdown(
            """
            **Willkommen zum Bau- & Recycling-Kreislauf Rechner!**

            Dieses Tool unterstützt Sie dabei, die Materialkosten und Recyclinganteile eines Bauprojekts basierend auf einer hochgeladenen IFC-Datei zu analysieren.

            **Funktionen:**
            - Hochladen einer IFC-Datei zur Extraktion der Materialdaten.
            - Eingabe von Materialkosten und Recyclinganteilen.
            - Visualisierung der Gesamtkosten und Recyclinganteile.

            Klicken Sie auf **Weiter**, um zu starten.
            """
        )
    
    with col1:
        st.image("BR.png", use_container_width=True) 
    
    st.write("")
    if st.button("Weiter"):
        st.session_state.page = "upload"  # Wechsel zur Upload-Seite

def upload_page():
    col1, col2 = st.columns([5, 0.7])  # Zwei Spalten: Eine für den Titel, eine für das Logo
    
    with col1:
        st.write("")
        st.markdown(
            """
            <style>
                .title {
                    font-size: 42px;
                    font-weight: bold;
                }
            </style>
            <div class="title">
                Bau- & Recycling-Kreislauf Rechner
            </div>
            """, unsafe_allow_html=True
        )
    
    with col2:
        st.write("")
        st.image("BR2.png", width=70)  # Das Logo wird rechts angezeigt und ist 60px breit

    st.header("1. IFC-Datei hochladen")
    upload_and_process_ifc()  # Materialien extrahieren
    
    if "material_names" in st.session_state and st.session_state.material_names:
        if st.button("Weiter zur Eingabe der Materialdaten", key="upload_to_input_button"):
            st.session_state.page = "input"

def input_page():
    # Erstelle die Spalten für das Logo und den Titel nebeneinander
    col1, col2 = st.columns([5, 0.7])  # Anpassen der Spaltenbreite
    with col2:
        # Lade das Logo
        st.write("")
        st.image("BR2.png", width=70)  # Logo in kleinerer Größe
    with col1:
        # Titel anzeigen
        st.title("Bau- & Recycling-Kreislauf Rechner")
    
    st.header("2. Materialkosten und Recyclinganteile eingeben")
    
    
    if "material_names" not in st.session_state:
        st.error("Keine Materialien aus der IFC-Datei gefunden. Bitte laden Sie die Datei erneut hoch.")
        return
    
    material_names = st.session_state.material_names
    material_data = get_material_inputs(material_names)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Zurück"):
            st.session_state.page = "upload"
    with col2:
        if material_data and st.button("Weiter zur Visualisierung"):
            st.session_state.page = "results"
            st.session_state.material_data = material_data

def results_page():
    col1, col2 = st.columns([5, 0.7])
    with col1:
        st.title("Bau- und Recycling-Kreislauf Rechner")

    with col2:
        st.write("")
        st.image("BR2.png", width=70)

    st.header("3. Berechnungsergebnisse")

    if "material_data" not in st.session_state:
        st.error("Keine Materialdaten gefunden. Bitte geben Sie die Daten ein.")
        return

    material_data = st.session_state.material_data
    costs, recycling_rates = calculate_costs_and_recycling(material_data)

    total_cost = sum(costs.values())
    total_material_quantity = len(recycling_rates)
    total_recycled = sum(recycling_rates.values())
    total_recycling_percentage = (total_recycled / total_material_quantity) if total_material_quantity > 0 else 0

    # Einfärbung des Gesamtrecyclinganteils je nach Wert
    if total_recycling_percentage >= 70:
        recycling_color = "green"
        recycling_message = "Laut EU-Gebäuderichtlinien wird bis 2025 eine Bau- und Abbruchabfall Wiederverwertungsquote von mindestens 70% erwartet!"
    elif 50 <= total_recycling_percentage < 70:
        recycling_color = "orange"
        recycling_message = "Laut EU-Gebäuderichtlinien wird bis 2025 eine Bau- und Abbruchabfall Wiederverwertungsquote von mindestens 70% erwartet!"
    else:
        recycling_color = "red"
        recycling_message = "Laut EU-Gebäuderichtlinien wird bis 2025 eine Bau- und Abbruchabfall Wiederverwertungsquote von mindestens 70% erwartet!"

    # Visualisierung der Kosten
    st.subheader("Kostenanalyse")
    plot_results(costs, "Kosten in Franken", "Material", "Kosten (Fr.)")

    st.write("")  # Leerzeile für Abstand
    st.write("")  # Leerzeile für Abstand

    # Visualisierung des Kostenanteils als Kreisdiagramm
    plot_pie_chart(costs, "Kostenanteil je Material")

    st.write("")  # Leerzeile für Abstand
    st.write("")  # Leerzeile für Abstand

    # Ausgabe der Gesamtrecyclingquote mit der entsprechenden Farbe
    st.markdown(f"### Gesamtrecyclinganteil: <span style='color:{recycling_color};'>{total_recycling_percentage:.2f} %</span>", unsafe_allow_html=True)

    # Anzeige des Hinweises, wenn der Recyclinganteil unter 70% liegt
    if total_recycling_percentage < 70:
        st.write("Laut EU-Gebäuderichtlinien wird bis 2025 eine Bau- und Abbruchabfall Wiederverwertungsquote von mindestens 70% erwartet!")

    st.subheader("Recyclinganteile")
    plot_results(recycling_rates, "Recyclinganteile (%)", "Material", "Recyclinganteil (%)")

    st.write("")  # Leerzeile für Abstand
    st.write("")  # Leerzeile für Abstand

    # Visualisierung des Recyclinganteils als Kreisdiagramm
    plot_pie_chart(recycling_rates, "Recyclinganteil je Material")

    # Zurück-Button
    if st.button("Zurück", key="results_to_input_button_1"):
        st.session_state.page = "input"  # Zurück zur Eingabeseite

if __name__ == "__main__":
    main()