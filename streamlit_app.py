import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from data import design_principles_data

# Seitenkonfiguration
st.set_page_config(
    page_title="Design Principles Analyse",
    page_icon="📊",
    layout="wide"
)

# Titel
st.title("📊 Design Principles Analyse - 2x2 Matrix")
st.markdown("---")


# Daten laden aus zentraler Funktion
@st.cache_data
def load_data():
    """Lädt alle Design Principles Daten inklusive Interview 5 und neue DPs"""
    return pd.DataFrame(design_principles_data)


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
    if st.sidebar.checkbox(source_labels[source], value=source in ['workshop', 'I1', 'I2', 'I3', 'I4', 'I5'],
                           key=source):
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

# NEUER FILTER: Design Principles Filter
st.sidebar.subheader("Design Principles")
all_dp_names = sorted(df['name'].unique().tolist())
selected_dp_names = st.sidebar.multiselect(
    "Design Principles auswählen:",
    options=all_dp_names,
    default=all_dp_names,
    help="Wählen Sie spezifische Design Principles für die Analyse aus"
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
def prepare_visualization_data(df, selected_sources, show_mode, selected_categories, selected_dp_names):
    # Nach Kategorien und Design Principles filtern
    filtered_df = df[
        (df['category'].isin(selected_categories)) &
        (df['name'].isin(selected_dp_names))
        ]

    plot_data = []

    for _, row in filtered_df.iterrows():
        if show_mode == "Durchschnittswerte":
            # Durchschnittswerte berechnen
            relevanz_values = []
            dringlichkeit_values = []
            sources_used = []

            for source in selected_sources:
                rel_col = f"{source}_relevanz"
                dring_col = f"{source}_dringlichkeit"

                if rel_col in row and row[rel_col] is not None:
                    relevanz_values.append(row[rel_col])
                    dringlichkeit_values.append(row[dring_col])
                    sources_used.append(source_labels[source])

            if relevanz_values:
                avg_relevanz = np.mean(relevanz_values)
                avg_dringlichkeit = np.mean(dringlichkeit_values)

                plot_data.append({
                    'name': row['name'],
                    'category': row['category'],
                    'relevanz': avg_relevanz,
                    'dringlichkeit': avg_dringlichkeit,
                    'source': f"Durchschnitt ({', '.join(sources_used)})",
                    'sources_list': sources_used,
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
                        'sources_list': [source_labels[source]],
                        'color': category_colors.get(row['category'], '#999999')
                    })

    return pd.DataFrame(plot_data)


# NEUE FUNKTION: Daten für verbessertes Hovering gruppieren
def prepare_grouped_visualization_data(viz_df):
    """Gruppiert Daten mit gleichen Koordinaten für verbessertes Hovering"""
    if viz_df.empty:
        return viz_df

    # Gruppiere nach name, category, relevanz, dringlichkeit
    grouped_data = []

    for (name, category, relevanz, dringlichkeit), group in viz_df.groupby(
            ['name', 'category', 'relevanz', 'dringlichkeit']):
        sources = group['source'].tolist()
        sources_list = []
        for source_list in group['sources_list']:
            sources_list.extend(source_list)

        # Entferne Duplikate und sortiere
        unique_sources = sorted(list(set(sources_list)))

        grouped_data.append({
            'name': name,
            'category': category,
            'relevanz': relevanz,
            'dringlichkeit': dringlichkeit,
            'sources': ', '.join(sources),
            'sources_list': unique_sources,
            'sources_count': len(unique_sources),
            'color': category_colors.get(category, '#999999')
        })

    return pd.DataFrame(grouped_data)


# Visualisierungsdaten erstellen
viz_df = prepare_visualization_data(df, selected_sources, show_mode, selected_categories, selected_dp_names)

# Hauptbereich
if not viz_df.empty:
    # Daten für verbessertes Hovering gruppieren
    grouped_viz_df = prepare_grouped_visualization_data(viz_df)

    # Statistiken anzeigen
    col1, col2, col3, col4, col5 = st.columns(5)

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

    with col5:
        num_dp = len(selected_dp_names)
        st.metric("🎯 Design Principles", num_dp)

    st.markdown("---")

    # 2x2 Matrix erstellen
    fig = go.Figure()

    # Quadranten-Hintergrund
    fig.add_shape(
        type="rect",
        x0=5, y0=0, x1=10, y1=5,
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
        x0=0, y0=5, x1=5, y1=10,
        fillcolor="rgba(0,255,0,0.1)",
        line=dict(width=0),
        layer="below"
    )

    # Datenpunkte nach Kategorie gruppieren - mit verbessertem Hovering
    for category in grouped_viz_df['category'].unique():
        category_data = grouped_viz_df[grouped_viz_df['category'] == category]

        # Erstelle Hover-Text mit allen Quellen
        hover_text = []
        for _, row in category_data.iterrows():
            sources_text = ', '.join(row['sources_list'])
            if row['sources_count'] > 1:
                hover_text.append(f"{row['name']}<br>Quellen: {sources_text}<br>({row['sources_count']} Quellen)")
            else:
                hover_text.append(f"{row['name']}<br>Quelle: {sources_text}")

        fig.add_trace(go.Scatter(
            x=category_data['dringlichkeit'],  # x-Achse ist jetzt Dringlichkeit
            y=category_data['relevanz'],      # y-Achse ist jetzt Relevanz
            mode='markers',
            name=category,
            text=hover_text,
            textposition="top center",
            marker=dict(
                size=12 + category_data['sources_count'] * 2,  # Größe basierend auf Anzahl Quellen
                color=category_colors.get(category, '#999999'),
                opacity=0.8,
                line=dict(width=2, color='white'),
                symbol='circle'
            ),
            hovertemplate='<b>%{text}</b><br>Dringlichkeit: %{x}<br>Relevanz: %{y}<extra></extra>'
        ))

    # Layout anpassen
    fig.update_layout(
        title={
            'text': f"Design Principles Matrix - {show_mode}",
            'x': 0.5,
            'font': {'size': 20}
        },
        xaxis_title="Dringlichkeit",  # Titel der x-Achse geändert
        yaxis_title="Relevanz",       # Titel der y-Achse geändert
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
    fig.add_annotation(x=7.5, y=2.5, text="Hoch Dringlich<br>Wenig Relevant", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=7.5, y=7.5, text="Hoch Dringlich<br>Sehr Relevant", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=2.5, y=2.5, text="Wenig Dringlich<br>Wenig Relevant", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")
    fig.add_annotation(x=2.5, y=7.5, text="Wenig Dringlich<br>Sehr Relevant", showarrow=False,
                       font=dict(size=14, color="gray"), bgcolor="rgba(255,255,255,0.8)")

    st.plotly_chart(fig, use_container_width=True)

    # Zusätzliche Info
    st.info(
        "💡 **Hover-Verbesserung**: Punkte mit gleichen Bewertungen für ein Design Principle zeigen alle Quellen an. Größere Punkte = mehr Quellen mit gleichen Werten.")

    # Detailanalyse
    st.markdown("---")
    st.subheader("📊 Detailanalyse")

    # Tabs für verschiedene Ansichten
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Datentabelle", "📈 Verteilungsanalyse", "🔍 Top/Low Performer", "🎯 Konsistenz-Analyse"])

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

    with tab4:
        st.subheader("🎯 Konsistenz zwischen Quellen")

        # Berechne Konsistenz-Metriken
        consistency_data = []
        for dp_name in selected_dp_names:
            dp_data = viz_df[viz_df['name'] == dp_name]
            if len(dp_data) > 1:
                rel_std = dp_data['relevanz'].std()
                dring_std = dp_data['dringlichkeit'].std()
                consistency_data.append({
                    'Design Principle': dp_name,
                    'Anzahl Quellen': len(dp_data),
                    'Relevanz Std': rel_std,
                    'Dringlichkeit Std': dring_std,
                    'Gesamt Konsistenz': (rel_std + dring_std) / 2
                })

        if consistency_data:
            consistency_df = pd.DataFrame(consistency_data)
            consistency_df = consistency_df.sort_values('Gesamt Konsistenz')

            col1, col2 = st.columns(2)

            with col1:
                st.write("**🎯 Konsistenteste Bewertungen** (niedrige Standardabweichung)")
                st.dataframe(consistency_df.head(10).round(2), use_container_width=True)

            with col2:
                st.write("**⚠️ Inkonsistenteste Bewertungen** (hohe Standardabweichung)")
                st.dataframe(consistency_df.tail(10).round(2), use_container_width=True)
        else:
            st.info("Keine Konsistenz-Analyse möglich - nur eine Quelle pro Design Principle ausgewählt.")

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

- **Datenquellen**: Wählen Sie Workshop und/oder Interviews (I1-I5)
- **Design Principles**: Filtern Sie nach spezifischen DPs (32 verfügbar)
- **Durchschnittswerte**: Für aggregierte Sichten
- **Hovering**: Zeigt alle Quellen mit gleichen Werten
- **Punktgröße**: Größere Punkte = mehr übereinstimmende Quellen
- **Konsistenz**: Neue Analyse der Bewertungsunterschiede
- **NEU**: Interview 5 Daten und 5 zusätzliche Design Principles
""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    🔬 Design Principles Forschungsanalyse | 
    Entwickelt für Workshop- und Interview-Datenauswertung | 
    Erweitert mit DP-Filter, Interview 5 und verbessertem Hovering | 
    📊 Jetzt mit 32 Design Principles
    </div>
    """,
    unsafe_allow_html=True
)