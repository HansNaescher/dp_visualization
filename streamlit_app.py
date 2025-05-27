import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

# Seitenkonfiguration
st.set_page_config(
    page_title="Design Principles Analyse",
    page_icon="📊",
    layout="wide"
)

# Titel
st.title("📊 Design Principles Analyse - 2x2 Matrix")
st.markdown("---")


# Daten strukturieren
@st.cache_data
def load_data():
    data = [
        {
            "name": "Arbeitsablaufintegration",
            "category": "Umsetzung",
            "workshop_relevanz": 7, "workshop_dringlichkeit": 7,
            "I1_relevanz": 7, "I1_dringlichkeit": 6,
            "I2_relevanz": 7, "I2_dringlichkeit": 6,
            "I3_relevanz": 7, "I3_dringlichkeit": 8,
            "I4_relevanz": 9, "I4_dringlichkeit": 7,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Bedarfsgerechte Erklärungen",
            "category": "User Interface",
            "workshop_relevanz": 5, "workshop_dringlichkeit": 5,
            "I1_relevanz": 5, "I1_dringlichkeit": 5,
            "I2_relevanz": 6, "I2_dringlichkeit": 4,
            "I3_relevanz": 5, "I3_dringlichkeit": 5,
            "I4_relevanz": 6, "I4_dringlichkeit": 5,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Berücksichtigung unterschiedlicher Nutzergruppen",
            "category": "Interaktion",
            "workshop_relevanz": 8, "workshop_dringlichkeit": 8,
            "I1_relevanz": 8, "I1_dringlichkeit": 7,
            "I2_relevanz": 8, "I2_dringlichkeit": 7,
            "I3_relevanz": 4, "I3_dringlichkeit": 3,
            "I4_relevanz": 8, "I4_dringlichkeit": 7,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Datengrundlage",
            "category": "Interaktion",
            "workshop_relevanz": 5, "workshop_dringlichkeit": 1,
            "I1_relevanz": 5, "I1_dringlichkeit": 1,
            "I2_relevanz": 5, "I2_dringlichkeit": 4,
            "I3_relevanz": 7, "I3_dringlichkeit": 8,
            "I4_relevanz": 5, "I4_dringlichkeit": 1,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Dokumentation",
            "category": "Monitoring",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 4,
            "I1_relevanz": 8, "I1_dringlichkeit": 4,
            "I2_relevanz": 8, "I2_dringlichkeit": 8,
            "I3_relevanz": 5, "I3_dringlichkeit": 3,
            "I4_relevanz": None, "I4_dringlichkeit": None,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Erklärung des KI Systems",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 5, "workshop_dringlichkeit": 2,
            "I1_relevanz": 5, "I1_dringlichkeit": 3,
            "I2_relevanz": 4, "I2_dringlichkeit": 3,
            "I3_relevanz": 5, "I3_dringlichkeit": 2,
            "I4_relevanz": 7, "I4_dringlichkeit": 3,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Erklärungstypen",
            "category": "User Interface",
            "workshop_relevanz": 7, "workshop_dringlichkeit": 2,
            "I1_relevanz": 7, "I1_dringlichkeit": 2,
            "I2_relevanz": 7, "I2_dringlichkeit": 2,
            "I3_relevanz": 7, "I3_dringlichkeit": 5,
            "I4_relevanz": 7, "I4_dringlichkeit": 2,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Explanation Style",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 5, "workshop_dringlichkeit": 7.5,
            "I1_relevanz": 4, "I1_dringlichkeit": 6.5,
            "I2_relevanz": 5, "I2_dringlichkeit": 6.5,
            "I3_relevanz": 5, "I3_dringlichkeit": 6.5,
            "I4_relevanz": 7, "I4_dringlichkeit": 6,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Fallbasierte Vergleiche",
            "category": "Interaktion",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 8,
            "I1_relevanz": 6, "I1_dringlichkeit": 7,
            "I2_relevanz": 6, "I2_dringlichkeit": 7,
            "I3_relevanz": 6, "I3_dringlichkeit": 8,
            "I4_relevanz": 9, "I4_dringlichkeit": 9,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Informationen zur KI und ihrem Anwendungskontext",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 3, "workshop_dringlichkeit": 6,
            "I1_relevanz": 3, "I1_dringlichkeit": 6.5,
            "I2_relevanz": 4, "I2_dringlichkeit": 5.5,
            "I3_relevanz": 3, "I3_dringlichkeit": 4,
            "I4_relevanz": 6, "I4_dringlichkeit": 6,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Informationsdarstellung",
            "category": "Fallbasiert",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 7,
            "I1_relevanz": 6, "I1_dringlichkeit": 5,
            "I2_relevanz": 6, "I2_dringlichkeit": 6,
            "I3_relevanz": 6, "I3_dringlichkeit": 4,
            "I4_relevanz": 7, "I4_dringlichkeit": 6,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Interaktionsdesign",
            "category": "Interaktion",
            "workshop_relevanz": 7, "workshop_dringlichkeit": 8,
            "I1_relevanz": 6, "I1_dringlichkeit": 7,
            "I2_relevanz": 7, "I2_dringlichkeit": 7,
            "I3_relevanz": 7, "I3_dringlichkeit": 8,
            "I4_relevanz": 8, "I4_dringlichkeit": 7,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Kognitive Aspekte und Nutzerengagement",
            "category": "User Interface",
            "workshop_relevanz": 1, "workshop_dringlichkeit": 3,
            "I1_relevanz": 2, "I1_dringlichkeit": 4,
            "I2_relevanz": 4, "I2_dringlichkeit": 4,
            "I3_relevanz": 5, "I3_dringlichkeit": 5,
            "I4_relevanz": 6, "I4_dringlichkeit": 3,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Kontextinformationen",
            "category": "Umsetzung",
            "workshop_relevanz": 2, "workshop_dringlichkeit": 4,
            "I1_relevanz": 2, "I1_dringlichkeit": 5,
            "I2_relevanz": 3, "I2_dringlichkeit": 5,
            "I3_relevanz": 2, "I3_dringlichkeit": 4.5,
            "I4_relevanz": 7, "I4_dringlichkeit": 6,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Kontrastierende Erklärungen",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 4, "workshop_dringlichkeit": 1,
            "I1_relevanz": 4, "I1_dringlichkeit": 1,
            "I2_relevanz": 4, "I2_dringlichkeit": 1,
            "I3_relevanz": 4, "I3_dringlichkeit": 1,
            "I4_relevanz": 5, "I4_dringlichkeit": 1,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Modellverhalten",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 5, "workshop_dringlichkeit": 8.5,
            "I1_relevanz": 5, "I1_dringlichkeit": 7.5,
            "I2_relevanz": 5, "I2_dringlichkeit": 5.5,
            "I3_relevanz": 5, "I3_dringlichkeit": 6.5,
            "I4_relevanz": 6, "I4_dringlichkeit": 8,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Monitoring",
            "category": "Monitoring",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 4,
            "I1_relevanz": 8, "I1_dringlichkeit": 4,
            "I2_relevanz": 6, "I2_dringlichkeit": 6,
            "I3_relevanz": None, "I3_dringlichkeit": None,
            "I4_relevanz": None, "I4_dringlichkeit": None,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Professionelle Autonomie",
            "category": "Interaktion",
            "workshop_relevanz": 7, "workshop_dringlichkeit": 9,
            "I1_relevanz": 7, "I1_dringlichkeit": 8,
            "I2_relevanz": 8, "I2_dringlichkeit": 9,
            "I3_relevanz": 7, "I3_dringlichkeit": 9,
            "I4_relevanz": 8, "I4_dringlichkeit": 9,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Reporting",
            "category": "Monitoring",
            "workshop_relevanz": 4, "workshop_dringlichkeit": 4,
            "I1_relevanz": 6, "I1_dringlichkeit": 4,
            "I2_relevanz": 5, "I2_dringlichkeit": 5,
            "I3_relevanz": None, "I3_dringlichkeit": None,
            "I4_relevanz": None, "I4_dringlichkeit": None,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Textuelle Erklärungen",
            "category": "User Interface",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 4,
            "I1_relevanz": 8, "I1_dringlichkeit": 8,
            "I2_relevanz": 6, "I2_dringlichkeit": 5,
            "I3_relevanz": 7, "I3_dringlichkeit": 6,
            "I4_relevanz": 8, "I4_dringlichkeit": 6,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Training und Nutzungsinformationen",
            "category": "Systembeschreibung/Systemarchitektur",
            "workshop_relevanz": 4, "workshop_dringlichkeit": 2,
            "I1_relevanz": 5, "I1_dringlichkeit": 9,
            "I2_relevanz": 5, "I2_dringlichkeit": 3,
            "I3_relevanz": 6, "I3_dringlichkeit": 6,
            "I4_relevanz": 9, "I4_dringlichkeit": 9,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Unerwartete Entscheidungen erklären",
            "category": "Fallbasiert",
            "workshop_relevanz": 6, "workshop_dringlichkeit": 3,
            "I1_relevanz": 6, "I1_dringlichkeit": 5,
            "I2_relevanz": 6, "I2_dringlichkeit": 5,
            "I3_relevanz": 7, "I3_dringlichkeit": 6,
            "I4_relevanz": 7, "I4_dringlichkeit": 3,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Usability",
            "category": "User Interface",
            "workshop_relevanz": 9, "workshop_dringlichkeit": 9,
            "I1_relevanz": 9, "I1_dringlichkeit": 8,
            "I2_relevanz": 9, "I2_dringlichkeit": 8,
            "I3_relevanz": 4, "I3_dringlichkeit": 3,
            "I4_relevanz": 9, "I4_dringlichkeit": 9,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Visualisierung von Regeln",
            "category": "Fallbasiert",
            "workshop_relevanz": 8, "workshop_dringlichkeit": 5,
            "I1_relevanz": 9, "I1_dringlichkeit": 5,
            "I2_relevanz": 8, "I2_dringlichkeit": 5,
            "I3_relevanz": 8, "I3_dringlichkeit": 5,
            "I4_relevanz": 9, "I4_dringlichkeit": 5,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Visuelle Erklärungen",
            "category": "User Interface",
            "workshop_relevanz": 8, "workshop_dringlichkeit": 9,
            "I1_relevanz": 7, "I1_dringlichkeit": 5,
            "I2_relevanz": 8, "I2_dringlichkeit": 8,
            "I3_relevanz": 6, "I3_dringlichkeit": 4,
            "I4_relevanz": 8, "I4_dringlichkeit": 9,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Regionale Zusammenhänge",
            "category": "Fallbasiert",
            "workshop_relevanz": 9, "workshop_dringlichkeit": 9,
            "I1_relevanz": None, "I1_dringlichkeit": None,
            "I2_relevanz": None, "I2_dringlichkeit": None,
            "I3_relevanz": None, "I3_dringlichkeit": None,
            "I4_relevanz": None, "I4_dringlichkeit": None,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        },
        {
            "name": "Zeitkomponente",
            "category": "Fallbasiert",
            "workshop_relevanz": 8, "workshop_dringlichkeit": 9,
            "I1_relevanz": None, "I1_dringlichkeit": None,
            "I2_relevanz": None, "I2_dringlichkeit": None,
            "I3_relevanz": None, "I3_dringlichkeit": None,
            "I4_relevanz": None, "I4_dringlichkeit": None,
            "I5_relevanz": None, "I5_dringlichkeit": None,
            "I6_relevanz": None, "I6_dringlichkeit": None
        }
    ]

    return pd.DataFrame(data)


# Daten laden
df = load_data()

# Sidebar für Kontrollen
st.sidebar.header("🎛️ Analyse-Einstellungen")

# Datenquellen auswählen
st.sidebar.subheader("Datenquellen")
all_sources = ['workshop', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6']
source_labels = {
    'workshop': 'Workshop',
    'I1': 'Interview 1',
    'I2': 'Interview 2',
    'I3': 'Interview 3',
    'I4': 'Interview 4',
    'I5': 'Interview 5',
    'I6': 'Interview 6'
}

selected_sources = []
for source in all_sources:
    if st.sidebar.checkbox(source_labels[source], value=source in ['workshop', 'I1', 'I2', 'I3', 'I4'], key=source):
        selected_sources.append(source)

# Darstellungsmodus
st.sidebar.subheader("Darstellungsmodus")
show_mode = st.sidebar.radio(
    "Ansicht wählen:",
    ["Einzelne Datenpunkte", "Durchschnittswerte"],
    index=0
)

# Kategoriefilter
st.sidebar.subheader("Kategorien")
categories = df['category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Kategorien auswählen:",
    options=categories,
    default=categories
)

# Farbpalette für Kategorien
category_colors = {
    'Umsetzung': '#FF6B6B',
    'User Interface': '#4ECDC4',
    'Interaktion': '#45B7D1',
    'Monitoring': '#96CEB4',
    'Systembeschreibung/Systemarchitektur': '#FFEAA7',
    'Fallbasiert': '#DDA0DD'
}


# Datenverarbeitung für Visualisierung
def prepare_visualization_data(df, selected_sources, show_mode, selected_categories):
    # Nach Kategorien filtern
    filtered_df = df[df['category'].isin(selected_categories)]

    plot_data = []

    for _, row in filtered_df.iterrows():
        if show_mode == "Durchschnittswerte":
            # Durchschnittswerte berechnen
            relevanz_values = []
            dringlichkeit_values = []

            for source in selected_sources:
                rel_col = f"{source}_relevanz"
                dring_col = f"{source}_dringlichkeit"

                if rel_col in row and row[rel_col] is not None:
                    relevanz_values.append(row[rel_col])
                    dringlichkeit_values.append(row[dring_col])

            if relevanz_values:
                avg_relevanz = np.mean(relevanz_values)
                avg_dringlichkeit = np.mean(dringlichkeit_values)

                plot_data.append({
                    'name': row['name'],
                    'category': row['category'],
                    'relevanz': avg_relevanz,
                    'dringlichkeit': avg_dringlichkeit,
                    'source': 'Durchschnitt',
                    'color': category_colors.get(row['category'], '#999999')
                })
        else:
            # Einzelne Datenpunkte
            for source in selected_sources:
                rel_col = f"{source}_relevanz"
                dring_col = f"{source}_dringlichkeit"

                if rel_col in row and row[rel_col] is not None:
                    plot_data.append({
                        'name': row['name'],
                        'category': row['category'],
                        'relevanz': row[rel_col],
                        'dringlichkeit': row[dring_col],
                        'source': source_labels[source],
                        'color': category_colors.get(row['category'], '#999999')
                    })

    return pd.DataFrame(plot_data)


# Visualisierungsdaten erstellen
viz_df = prepare_visualization_data(df, selected_sources, show_mode, selected_categories)

# Hauptbereich
if not viz_df.empty:
    # Statistiken anzeigen
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Datenpunkte", len(viz_df))

    with col2:
        avg_relevanz = viz_df['relevanz'].mean()
        st.metric("📈 ⌀ Relevanz", f"{avg_relevanz:.1f}")

    with col3:
        avg_dringlichkeit = viz_df['dringlichkeit'].mean()
        st.metric("⚡ ⌀ Dringlichkeit", f"{avg_dringlichkeit:.1f}")

    with col4:
        num_categories = len(selected_categories)
        st.metric("🏷️ Kategorien", num_categories)

    st.markdown("---")

    # 2x2 Matrix erstellen
    fig = go.Figure()

    # Quadranten-Hintergrund
    fig.add_shape(
        type="rect",
        x0=0, y0=5, x1=5, y1=10,
        fillcolor="rgba(255,0,0,0.1)",
        line=dict(width=0),
        layer="below"
    )
    fig.add_shape(
        type="rect",
        x0=5, y0=5, x1=10, y1=10,
        fillcolor="rgba(255,0,0,0.2)",
        line=dict(width=0),
        layer="below"
    )
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=5, y1=5,
        fillcolor="rgba(255,255,0,0.1)",
        line=dict(width=0),
        layer="below"
    )
    fig.add_shape(
        type="rect",
        x0=5, y0=0, x1=10, y1=5,
        fillcolor="rgba(0,255,0,0.1)",
        line=dict(width=0),
        layer="below"
    )

    # Datenpunkte nach Kategorie gruppieren
    for category in viz_df['category'].unique():
        category_data = viz_df[viz_df['category'] == category]

        fig.add_trace(go.Scatter(
            x=category_data['relevanz'],
            y=category_data['dringlichkeit'],
            mode='markers',
            name=category,
            text=category_data['name'] + '<br>Quelle: ' + category_data['source'],
            textposition="top center",
            marker=dict(
                size=12,
                color=category_colors.get(category, '#999999'),
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{text}</b><br>Relevanz: %{x}<br>Dringlichkeit: %{y}<extra></extra>'
        ))

    # Layout anpassen
    fig.update_layout(
        title={
            'text': f"Design Principles Matrix - {show_mode}",
            'x': 0.5,
            'font': {'size': 20}
        },
        xaxis_title="Relevanz",
        yaxis_title="Dringlichkeit",
        xaxis=dict(range=[0, 10], dtick=1, gridcolor='lightgray'),
        yaxis=dict(range=[0, 10], dtick=1, gridcolor='lightgray'),
        width=800,
        height=600,
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    # Quadranten-Labels hinzufügen
    fig.add_annotation(x=2.5, y=7.5, text="Hoch Relevant<br>Hoch Dringlich", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=7.5, y=7.5, text="Sehr Relevant<br>Hoch Dringlich", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=2.5, y=2.5, text="Hoch Relevant<br>Wenig Dringlich", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=7.5, y=2.5, text="Sehr Relevant<br>Wenig Dringlich", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")

    st.plotly_chart(fig, use_container_width=True)

    # Detailanalyse
    st.markdown("---")
    st.subheader("📊 Detailanalyse")

    # Tabs für verschiedene Ansichten
    tab1, tab2, tab3 = st.tabs(["📋 Datentabelle", "📈 Verteilungsanalyse", "🔍 Top/Low Performer"])

    with tab1:
        st.dataframe(
            viz_df[['name', 'category', 'relevanz', 'dringlichkeit', 'source']].round(2),
            use_container_width=True
        )

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            # Relevanz-Verteilung
            fig_rel = px.histogram(
                viz_df,
                x='relevanz',
                color='category',
                title="Verteilung der Relevanz-Bewertungen",
                nbins=10,
                color_discrete_map=category_colors
            )
            fig_rel.update_layout(height=400)
            st.plotly_chart(fig_rel, use_container_width=True)

        with col2:
            # Dringlichkeit-Verteilung
            fig_dring = px.histogram(
                viz_df,
                x='dringlichkeit',
                color='category',
                title="Verteilung der Dringlichkeits-Bewertungen",
                nbins=10,
                color_discrete_map=category_colors
            )
            fig_dring.update_layout(height=400)
            st.plotly_chart(fig_dring, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔝 Top Prioritäten")
            viz_df['priority_score'] = viz_df['relevanz'] * viz_df['dringlichkeit']
            top_items = viz_df.nlargest(10, 'priority_score')[
                ['name', 'category', 'relevanz', 'dringlichkeit', 'priority_score']]
            st.dataframe(top_items.round(2), use_container_width=True)

        with col2:
            st.subheader("📉 Niedrige Prioritäten")
            low_items = viz_df.nsmallest(10, 'priority_score')[
                ['name', 'category', 'relevanz', 'dringlichkeit', 'priority_score']]
            st.dataframe(low_items.round(2), use_container_width=True)

    # Kategorie-Analyse
    st.markdown("---")
    st.subheader("🏷️ Kategorie-Analyse")

    category_stats = viz_df.groupby('category').agg({
        'relevanz': ['mean', 'std', 'count'],
        'dringlichkeit': ['mean', 'std']
    }).round(2)

    category_stats.columns = ['Relevanz_Mittel', 'Relevanz_Std', 'Anzahl', 'Dringlichkeit_Mittel', 'Dringlichkeit_Std']
    st.dataframe(category_stats, use_container_width=True)

else:
    st.warning("⚠️ Keine Daten für die gewählten Filter verfügbar. Bitte passen Sie Ihre Auswahl an.")

# Exportfunktion
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Export")

if not viz_df.empty:
    csv = viz_df.to_csv(index=False)
    st.sidebar.download_button(
        label="📊 Daten als CSV herunterladen",
        data=csv,
        file_name='design_principles_analysis.csv',
        mime='text/csv'
    )

# Informationen
st.sidebar.markdown("---")
st.sidebar.info("""
**ℹ️ Hinweise zur Nutzung:**

- Wählen Sie verschiedene Datenquellen für die Analyse
- Verwenden Sie Durchschnittswerte für aggregierte Sichten
- Filtern Sie nach Kategorien für fokussierte Analysen
- Nutzen Sie die Tabs für detaillierte Einblicke
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🔬 Design Principles Forschungsanalyse | 
    Entwickelt für Workshop- und Interview-Datenauswertung
    </div>
    """,
    unsafe_allow_html=True
)