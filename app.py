import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Astrological data for August 2025
astro_data = {
    'Date': pd.date_range(start='2025-08-01', end='2025-08-31'),
    'Mercury Retro': [False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False],
    'Moon Phase': ['New Moon', 'Waxing Crescent', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 'Waning Gibbous', 'Waning Gibbous', 'Waning Gibbous', 'Waning Gibbous', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'Waning Crescent', 'New Moon'],
    'Moon Transit': ['Cancer', 'Leo', 'Leo', 'Virgo', 'Virgo', 'Libra', 'Libra', 'Scorpio', 'Scorpio', 'Sagittarius', 'Sagittarius', 'Capricorn', 'Capricorn', 'Aquarius', 'Aquarius', 'Pisces', 'Pisces', 'Aries', 'Aries', 'Taurus', 'Taurus', 'Gemini', 'Gemini', 'Cancer', 'Cancer', 'Leo', 'Leo', 'Virgo', 'Virgo', 'Libra', 'Libra'],
    'Jupiter Trine Saturn': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    'Mars Square Pluto': [False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
    'Venus Sextile Jupiter': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
    'Bullish': [0.7, 0.5, 0.4, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.8],
    'Bearish': [0.3, 0.5, 0.6, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.2]
}

df = pd.DataFrame(astro_data)

def plot_astro_events(planets_to_show):
    # Create figure
    fig = go.Figure()
    
    # Add Bullish/Bearish indicators
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Bullish'],
        name='Bullish',
        line=dict(color='green', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Bearish'],
        name='Bearish',
        line=dict(color='red', width=2)
    ))
    
    # Plot Moon Phases
    moon_phase_colors = {
        'New Moon': 'black',
        'Full Moon': 'gray',
        'First Quarter': 'lightgray',
        'Last Quarter': 'darkgray',
        'Waxing Crescent': 'blue',
        'Waxing Gibbous': 'cyan',
        'Waning Gibbous': 'orange',
        'Waning Crescent': 'yellow'
    }
    
    # Collect unique moon phases to avoid duplicate legend entries
    unique_phases = []
    for i, phase in enumerate(df['Moon Phase']):
        if phase in moon_phase_colors:
            if phase not in unique_phases:
                unique_phases.append(phase)
                show_legend = True
            else:
                show_legend = False
                
            fig.add_trace(go.Scatter(
                x=[df['Date'][i]],
                y=[0.5],
                mode='markers',
                marker=dict(color=moon_phase_colors[phase], size=15),
                name=phase,
                showlegend=show_legend
            ))
    
    # Plot selected planetary events
    planet_colors = {
        'Mercury Retro': 'purple',
        'Jupiter Trine Saturn': 'blue',
        'Mars Square Pluto': 'red',
        'Venus Sextile Jupiter': 'green'
    }
    
    for planet in planets_to_show:
        if planet in df.columns:
            event_dates = df[df[planet] == True]['Date']
            if len(event_dates) > 0:
                fig.add_trace(go.Scatter(
                    x=event_dates,
                    y=[0.8] * len(event_dates),
                    mode='markers',
                    marker=dict(color=planet_colors.get(planet, 'black'), size=20, symbol='star'),
                    name=planet,
                    showlegend=True
                ))
    
    # Update layout
    fig.update_layout(
        title='Astrological Events & Market Sentiment - August 2025',
        xaxis_title='Date',
        yaxis_title='Market Sentiment',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600
    )
    
    # Update y-axes
    fig.update_yaxes(range=[0, 1])
    
    return fig

def generate_report(planets_to_show):
    st.header("Astrological Market Analysis Report")
    st.write(f"Selected Planetary Events: {', '.join(planets_to_show)}")
    
    st.subheader("Key Events")
    for i, row in df.iterrows():
        date_str = row['Date'].strftime('%Y-%m-%d')
        moon_phase = row['Moon Phase']
        moon_transit = row['Moon Transit']
        bullish = row['Bullish']
        bearish = row['Bearish']
        
        with st.expander(f"Date: {date_str}"):
            st.write(f"**Moon Phase:** {moon_phase} (Transit: {moon_transit})")
            st.write(f"**Market Sentiment:** Bullish {bullish:.1%} | Bearish {bearish:.1%}")
            
            events = []
            for planet in planets_to_show:
                if planet in df.columns and row[planet]:
                    events.append(planet)
            
            if events:
                st.write("**Active Events:**")
                for event in events:
                    st.write(f"- {event}")
    
    st.subheader("Moon Phase Impact")
    st.write("- **New Moon:** Bullish for new positions, growth stocks")
    st.write("- **Full Moon:** Bearish, profit-taking, increased volatility")
    st.write("- **Waxing Phases:** Gradually building bullish energy")
    st.write("- **Waning Phases:** Gradually building bearish energy")
    
    st.subheader("Planetary Influences")
    st.write("- **Mercury Retrograde:** Communication issues, tech volatility")
    st.write("- **Jupiter Trine Saturn:** Growth with structure, bullish")
    st.write("- **Mars Square Pluto:** Power struggles, institutional conflicts, bearish")
    st.write("- **Venus Sextile Jupiter:** Positive social mood, consumer spending, bullish")

# Streamlit app
st.title('Astrological Market Analysis')

# Select which planetary events to display
selected_planets = st.multiselect(
    'Select Planetary Events to Display',
    ['Mercury Retro', 'Jupiter Trine Saturn', 'Mars Square Pluto', 'Venus Sextile Jupiter'],
    ['Mercury Retro', 'Jupiter Trine Saturn', 'Mars Square Pluto']
)

if st.button('Generate Report'):
    generate_report(selected_planets)

# Plot events
fig = plot_astro_events(selected_planets)
st.plotly_chart(fig, use_container_width=True)
