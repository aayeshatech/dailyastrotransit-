import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date

# Set page configuration
st.set_page_config(page_title="Astro Transit For Daily Transit", layout="wide")

# Create header
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Astro Transit For Daily Transit</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state variables
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = date(2025, 8, 4)
if 'planetary_options' not in st.session_state:
    st.session_state.planetary_options = {
        'Planetary Transit': True,
        'Planetary Aspect': True,
        'Planetary Retrograde': True,
        'Moon Phases': True
    }

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Input Date", "Planetary Report", "Planetary Effect", "Upcoming Planetary Transit"])

# Sample data for planetary events
planetary_data = {
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

df = pd.DataFrame(planetary_data)

# Detailed planetary data
planetary_details = {
    'Planetary Transit': [
        {'name': 'Mercury in Virgo', 'start': '2025-07-25', 'end': '2025-08-14', 'effect': 'Bullish', 'description': 'Analytical clarity, communication efficiency'},
        {'name': 'Venus in Libra', 'start': '2025-07-31', 'end': '2025-09-06', 'effect': 'Bullish', 'description': 'Diplomatic stability, social harmony'},
        {'name': 'Mars in Gemini', 'start': '2025-07-20', 'end': '2025-09-04', 'effect': 'Bearish', 'description': 'Volatile energy, scattered focus'},
        {'name': 'Jupiter in Gemini', 'start': '2025-05-25', 'end': '2025-06-09', 'effect': 'Bullish', 'description': 'Expansion in communication, learning'},
        {'name': 'Saturn in Pisces', 'start': '2023-03-07', 'end': '2025-05-24', 'effect': 'Bearish', 'description': 'Restructuring, spiritual challenges'}
    ],
    'Planetary Aspect': [
        {'name': 'Jupiter Trine Saturn', 'start': '2025-08-01', 'end': '2025-08-15', 'effect': 'Bullish', 'description': 'Growth with discipline, balanced expansion'},
        {'name': 'Mars Square Pluto', 'start': '2025-08-03', 'end': '2025-08-31', 'effect': 'Bearish', 'description': 'Power struggles, institutional conflicts'},
        {'name': 'Venus Sextile Jupiter', 'start': '2025-08-04', 'end': '2025-08-04', 'effect': 'Bullish', 'description': 'Positive social mood, consumer spending'},
        {'name': 'Sun Oppose Saturn', 'start': '2025-08-13', 'end': '2025-08-13', 'effect': 'Bearish', 'description': 'Authority challenges, limitations'},
        {'name': 'Mercury Conjunct Venus', 'start': '2025-08-19', 'end': '2025-08-19', 'effect': 'Bullish', 'description': 'Harmonious communication, financial discussions'}
    ],
    'Planetary Retrograde': [
        {'name': 'Mercury Retrograde', 'start': '2025-08-01', 'end': '2025-08-25', 'effect': 'Bearish', 'description': 'Communication issues, tech volatility, delays'},
        {'name': 'Saturn Retrograde', 'start': '2025-06-29', 'end': '2025-11-15', 'effect': 'Bearish', 'description': 'Restructuring delays, karmic lessons'},
        {'name': 'Neptune Retrograde', 'start': '2025-06-30', 'end': '2025-12-07', 'effect': 'Bearish', 'description': 'Uncertainty, deception, spiritual confusion'},
        {'name': 'Pluto Retrograde', 'start': '2025-05-02', 'end': '2025-10-11', 'effect': 'Bullish', 'description': 'Transformational opportunities, deep changes'},
        {'name': 'Jupiter Retrograde', 'start': '2025-10-09', 'end': '2026-02-04', 'effect': 'Bearish', 'description': 'Reassessment of beliefs, growth slowdown'}
    ],
    'Moon Phases': [
        {'name': 'New Moon', 'date': '2025-08-01', 'effect': 'Bullish', 'description': 'New beginnings, fresh momentum, ideal for starting new projects'},
        {'name': 'First Quarter', 'date': '2025-08-08', 'effect': 'Neutral', 'description': 'Decision point, overcoming challenges, building momentum'},
        {'name': 'Full Moon', 'date': '2025-08-15', 'effect': 'Bearish', 'description': 'Emotional peaks, culmination, profit-taking, increased volatility'},
        {'name': 'Last Quarter', 'date': '2025-08-23', 'effect': 'Neutral', 'description': 'Release, letting go, reflection, preparation for new cycle'},
        {'name': 'New Moon', 'date': '2025-08-30', 'effect': 'Bullish', 'description': 'Renewed optimism, fresh energy, new opportunities'}
    ]
}

# Planetary effects on markets
planetary_effects = {
    'Mercury Retrograde': {
        'Sectors': ['Technology', 'Communication', 'Transportation'],
        'Indices': ['NASDAQ', 'NYSE ARCA'],
        'Assets': ['Bonds', 'Currencies'],
        'Commodities': ['Silver', 'Copper'],
        'Effect': 'Bearish - Communication breakdowns, tech glitches, travel delays'
    },
    'Jupiter Trine Saturn': {
        'Sectors': ['Finance', 'Real Estate', 'Infrastructure'],
        'Indices': ['S&P 500', 'Dow Jones'],
        'Assets': ['Blue-chip stocks', 'Government bonds'],
        'Commodities': ['Gold', 'Industrial metals'],
        'Effect': 'Bullish - Balanced growth, stable expansion, long-term investments'
    },
    'Mars Square Pluto': {
        'Sectors': ['Energy', 'Defense', 'Mining'],
        'Indices': ['Russell 2000', 'Volatility Index'],
        'Assets': ['Commodity currencies', 'Small-cap stocks'],
        'Commodities': ['Oil', 'Platinum'],
        'Effect': 'Bearish - Power struggles, conflicts, institutional sell-offs'
    },
    'Venus Sextile Jupiter': {
        'Sectors': ['Retail', 'Entertainment', 'Luxury goods'],
        'Indices': ['Consumer Discretionary', 'Hospitality'],
        'Assets': ['Retail stocks', 'Entertainment stocks'],
        'Commodities': ['Wine', 'Luxury metals'],
        'Effect': 'Bullish - Positive social mood, consumer spending, social harmony'
    },
    'New Moon': {
        'Sectors': ['Technology', 'Biotech', 'Startups'],
        'Indices': ['NASDAQ', 'Small-cap indices'],
        'Assets': ['Growth stocks', 'IPOs'],
        'Commodities': ['Rare earth elements', 'Lithium'],
        'Effect': 'Bullish - New beginnings, fresh momentum, ideal for new investments'
    },
    'Full Moon': {
        'Sectors': ['Healthcare', 'Utilities', 'Consumer staples'],
        'Indices': ['Volatility Index', 'Defensive sectors'],
        'Assets': ['Defensive stocks', 'Safe-haven assets'],
        'Commodities': ['Gold', 'Silver'],
        'Effect': 'Bearish - Emotional peaks, profit-taking, increased volatility'
    }
}

# Intraday moon aspects
intraday_moon_aspects = {
    '2025-08-04': [
        {'time': '09:30', 'aspect': 'Moon Trine Sun', 'effect': 'Bullish', 'description': 'Confident market open, positive sentiment'},
        {'time': '11:15', 'aspect': 'Mercury Oppose Neptune', 'effect': 'Bearish', 'description': 'Confusion, misinformation, tech volatility'},
        {'time': '13:45', 'aspect': 'Venus Sextile Jupiter', 'effect': 'Bullish', 'description': 'Positive news flow, consumer spending'},
        {'time': '15:20', 'aspect': 'Mars Square Pluto', 'effect': 'Bearish', 'description': 'Power struggles, institutional conflicts'}
    ],
    '2025-08-05': [
        {'time': '10:00', 'aspect': 'Moon Conjunct Mars', 'effect': 'Bearish', 'description': 'Aggressive energy, impulsive decisions'},
        {'time': '12:30', 'aspect': 'Moon Trine Uranus', 'effect': 'Bullish', 'description': 'Innovation, tech rally, unexpected opportunities'},
        {'time': '14:45', 'aspect': 'Moon Oppose Saturn', 'effect': 'Bearish', 'description': 'Restrictions, limitations, conservative approach'},
        {'time': '16:00', 'aspect': 'Moon Sextile Venus', 'effect': 'Bullish', 'description': 'Harmony, social connections, positive close'}
    ]
}

# Tab 1: Input Date
with tab1:
    st.header("Select Date for Report")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        selected_date = st.date_input(
            "Select a date:",
            value=st.session_state.selected_date,
            min_value=date(2025, 8, 1),
            max_value=date(2025, 8, 31),
            format="YYYY-MM-DD"
        )
        st.session_state.selected_date = selected_date
        
        if st.button("Generate Report"):
            st.success(f"Report will be generated for {selected_date.strftime('%Y-%m-%d')}")

# Tab 2: Planetary Report
with tab2:
    st.header("Planetary Report")
    
    # Options for what to display
    st.subheader("Select Report Options")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.planetary_options['Planetary Transit'] = st.checkbox("Planetary Transit", value=st.session_state.planetary_options['Planetary Transit'])
        st.session_state.planetary_options['Planetary Aspect'] = st.checkbox("Planetary Aspect", value=st.session_state.planetary_options['Planetary Aspect'])
    
    with col2:
        st.session_state.planetary_options['Planetary Retrograde'] = st.checkbox("Planetary Retrograde", value=st.session_state.planetary_options['Planetary Retrograde'])
        st.session_state.planetary_options['Moon Phases'] = st.checkbox("Moon Phases", value=st.session_state.planetary_options['Moon Phases'])
    
    # Display selected options
    st.markdown("---")
    st.subheader("Planetary Details")
    
    if st.session_state.planetary_options['Planetary Transit']:
        st.markdown("### Planetary Transit")
        transit_df = pd.DataFrame(planetary_details['Planetary Transit'])
        st.dataframe(transit_df, use_container_width=True)
    
    if st.session_state.planetary_options['Planetary Aspect']:
        st.markdown("### Planetary Aspect")
        aspect_df = pd.DataFrame(planetary_details['Planetary Aspect'])
        st.dataframe(aspect_df, use_container_width=True)
    
    if st.session_state.planetary_options['Planetary Retrograde']:
        st.markdown("### Planetary Retrograde")
        retrograde_df = pd.DataFrame(planetary_details['Planetary Retrograde'])
        st.dataframe(retrograde_df, use_container_width=True)
    
    if st.session_state.planetary_options['Moon Phases']:
        st.markdown("### Moon Phases")
        moon_df = pd.DataFrame(planetary_details['Moon Phases'])
        st.dataframe(moon_df, use_container_width=True)

# Tab 3: Planetary Effect
with tab3:
    st.header("Planetary Effect on Markets")
    selected_date_str = st.session_state.selected_date.strftime('%Y-%m-%d')
    st.subheader(f"Effects for {selected_date_str}")
    
    # Find active events for the selected date
    active_events = []
    
    # Convert selected_date to datetime for comparison
    selected_datetime = datetime.combine(st.session_state.selected_date, datetime.min.time())
    
    # Check planetary transits
    for transit in planetary_details['Planetary Transit']:
        start_date = datetime.strptime(transit['start'], '%Y-%m-%d')
        end_date = datetime.strptime(transit['end'], '%Y-%m-%d')
        if start_date <= selected_datetime <= end_date:
            active_events.append(transit['name'])
    
    # Check planetary aspects
    for aspect in planetary_details['Planetary Aspect']:
        start_date = datetime.strptime(aspect['start'], '%Y-%m-%d')
        end_date = datetime.strptime(aspect['end'], '%Y-%m-%d')
        if start_date <= selected_datetime <= end_date:
            active_events.append(aspect['name'])
    
    # Check planetary retrogrades
    for retrograde in planetary_details['Planetary Retrograde']:
        start_date = datetime.strptime(retrograde['start'], '%Y-%m-%d')
        end_date = datetime.strptime(retrograde['end'], '%Y-%m-%d')
        if start_date <= selected_datetime <= end_date:
            active_events.append(retrograde['name'])
    
    # Check moon phases
    for moon in planetary_details['Moon Phases']:
        moon_date = datetime.strptime(moon['date'], '%Y-%m-%d')
        if moon_date.date() == st.session_state.selected_date:
            active_events.append(moon['name'])
    
    if active_events:
        st.markdown("### Active Planetary Events")
        for event in active_events:
            if event in planetary_effects:
                st.markdown(f"#### {event}")
                effect_data = planetary_effects[event]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Sectors:**")
                    for sector in effect_data['Sectors']:
                        st.markdown(f"- {sector}")
                    
                    st.markdown("**Indices:**")
                    for index in effect_data['Indices']:
                        st.markdown(f"- {index}")
                
                with col2:
                    st.markdown("**Assets:**")
                    for asset in effect_data['Assets']:
                        st.markdown(f"- {asset}")
                    
                    st.markdown("**Commodities:**")
                    for commodity in effect_data['Commodities']:
                        st.markdown(f"- {commodity}")
                
                st.markdown(f"**Overall Effect:** {effect_data['Effect']}")
                st.markdown("---")
    else:
        st.info("No significant planetary events for the selected date.")

# Tab 4: Upcoming Planetary Transit
with tab4:
    st.header("Upcoming Planetary Transit")
    
    # Create sub-tabs for different categories
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6 = st.tabs([
        "Planetary Timeline", 
        "Planetary Aspect", 
        "Planetary Retrograde", 
        "Planetary Transit", 
        "Moon Aspect", 
        "Moon Transit"
    ])
    
    # Planetary Timeline
    with subtab1:
        st.subheader("Planetary Timeline")
        fig = go.Figure()
        
        # Add events to timeline
        events = []
        
        # Add planetary aspects
        for aspect in planetary_details['Planetary Aspect']:
            events.append({
                'Date': aspect['start'],
                'Event': aspect['name'],
                'Type': 'Aspect',
                'Effect': aspect['effect']
            })
        
        # Add planetary retrogrades
        for retrograde in planetary_details['Planetary Retrograde']:
            events.append({
                'Date': retrograde['start'],
                'Event': f"{retrograde['name']} Begins",
                'Type': 'Retrograde',
                'Effect': retrograde['effect']
            })
            events.append({
                'Date': retrograde['end'],
                'Event': f"{retrograde['name']} Ends",
                'Type': 'Retrograde',
                'Effect': 'Neutral'
            })
        
        # Add moon phases
        for moon in planetary_details['Moon Phases']:
            events.append({
                'Date': moon['date'],
                'Event': moon['name'],
                'Type': 'Moon Phase',
                'Effect': moon['effect']
            })
        
        # Convert to DataFrame and sort by date
        events_df = pd.DataFrame(events)
        events_df['Date'] = pd.to_datetime(events_df['Date'])
        events_df = events_df.sort_values('Date')
        
        # Create scatter plot
        colors = {'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray'}
        symbols = {'Aspect': 'circle', 'Retrograde': 'diamond', 'Moon Phase': 'star'}
        
        for event_type in events_df['Type'].unique():
            for effect in events_df['Effect'].unique():
                subset = events_df[(events_df['Type'] == event_type) & (events_df['Effect'] == effect)]
                if not subset.empty:
                    fig.add_trace(go.Scatter(
                        x=subset['Date'],
                        y=[event_type] * len(subset),
                        mode='markers',
                        marker=dict(
                            color=colors[effect],
                            symbol=symbols[event_type],
                            size=15,
                            line=dict(width=1, color='black')
                        ),
                        text=subset['Event'],
                        hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Type: %{y}<extra></extra>',
                        name=f"{event_type} - {effect}"
                    ))
        
        fig.update_layout(
            title="Upcoming Planetary Events Timeline",
            xaxis_title="Date",
            yaxis_title="Event Type",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Planetary Aspect
    with subtab2:
        st.subheader("Planetary Aspect")
        aspect_df = pd.DataFrame(planetary_details['Planetary Aspect'])
        st.dataframe(aspect_df, use_container_width=True)
    
    # Planetary Retrograde
    with subtab3:
        st.subheader("Planetary Retrograde")
        retrograde_df = pd.DataFrame(planetary_details['Planetary Retrograde'])
        st.dataframe(retrograde_df, use_container_width=True)
    
    # Planetary Transit
    with subtab4:
        st.subheader("Planetary Transit")
        transit_df = pd.DataFrame(planetary_details['Planetary Transit'])
        st.dataframe(transit_df, use_container_width=True)
    
    # Moon Aspect
    with subtab5:
        st.subheader("Moon Aspect")
        
        # Select date for intraday moon aspects
        intraday_date = st.date_input(
            "Select date for intraday moon aspects:",
            value=st.session_state.selected_date,
            min_value=date(2025, 8, 1),
            max_value=date(2025, 8, 5),
            format="YYYY-MM-DD",
            key="intraday_date"
        )
        
        intraday_date_str = intraday_date.strftime('%Y-%m-%d')
        
        if intraday_date_str in intraday_moon_aspects:
            st.markdown(f"### Moon Aspects for {intraday_date_str}")
            
            aspects_df = pd.DataFrame(intraday_moon_aspects[intraday_date_str])
            st.dataframe(aspects_df, use_container_width=True)
            
            # Create a timeline chart for intraday aspects
            fig = go.Figure()
            
            colors = {'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray'}
            
            for _, aspect in aspects_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[aspect['time']],
                    y=[aspect['aspect']],
                    mode='markers',
                    marker=dict(
                        color=colors[aspect['effect']],
                        size=20,
                        symbol='diamond',
                        line=dict(width=1, color='black')
                    ),
                    text=f"{aspect['description']}<br>Effect: {aspect['effect']}",
                    hovertemplate='<b>%{y}</b><br>Time: %{x}<br>%{text}<extra></extra>',
                    name=aspect['aspect']
                ))
            
            fig.update_layout(
                title=f"Intraday Moon Aspects for {intraday_date_str}",
                xaxis_title="Time",
                yaxis_title="Moon Aspect",
                height=500,
                hovermode='closest'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No intraday moon aspects data available for the selected date.")
    
    # Moon Transit
    with subtab6:
        st.subheader("Moon Transit")
        
        # Create a chart showing moon transit through zodiac signs
        fig = go.Figure()
        
        # Get unique dates and moon transits
        moon_transit_data = df[['Date', 'Moon Transit']].copy()
        
        # Create a categorical plot for moon signs
        moon_signs = moon_transit_data['Moon Transit'].unique()
        
        for i, sign in enumerate(moon_signs):
            sign_data = moon_transit_data[moon_transit_data['Moon Transit'] == sign]
            fig.add_trace(go.Scatter(
                x=sign_data['Date'],
                y=[i] * len(sign_data),
                mode='markers',
                marker=dict(size=15, color='blue'),
                text=[f"Moon in {sign}"] * len(sign_data),
                hovertemplate='<b>%{text}</b><br>Date: %{x}<extra></extra>',
                name=sign,
                showlegend=False
            ))
        
        fig.update_layout(
            title="Moon Transit Through Zodiac Signs - August 2025",
            xaxis_title="Date",
            yaxis=dict(
                tickmode='array',
                tickvals=list(range(len(moon_signs))),
                ticktext=moon_signs
            ),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show moon transit data in a table
        st.markdown("### Moon Transit Schedule")
        st.dataframe(moon_transit_data, use_container_width=True)
