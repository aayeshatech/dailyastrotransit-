import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date, time
import calendar
import random
import math
import pytz
# Set page configuration
st.set_page_config(page_title="Astro Transit For Daily Transit", layout="wide")
# Create header
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Astro Transit For Daily Transit</h1>", unsafe_allow_html=True)
st.markdown("---")
# Initialize session state variables
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = date(2025, 8, 4)
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = time(9, 15)
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Mumbai, India"
if 'planetary_options' not in st.session_state:
    st.session_state.planetary_options = {
        'Planetary Transit': True,
        'Planetary Aspect': True,
        'Planetary Retrograde': True,
        'Moon Phases': True
    }
# City coordinates for location-based calculations
city_coordinates = {
    "Mumbai, India": (19.0760, 72.8777),
    "Delhi, India": (28.7041, 77.1025),
    "Bangalore, India": (12.9716, 77.5946),
    "Kolkata, India": (22.5726, 88.3639),
    "Chennai, India": (13.0827, 80.2707),
    "New York, USA": (40.7128, -74.0060),
    "London, UK": (51.5074, -0.1278),
    "Tokyo, Japan": (35.6762, 139.6503),
    "Sydney, Australia": (-33.8688, 151.2093),
    "Dubai, UAE": (25.2048, 55.2708),
}
# Zodiac signs and nakshatras
zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
nakshatras = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu',
    'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
    'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
    'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
    'Uttara Bhadrapada', 'Revati'
]
# Sign lords
sign_lords = {
    'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
    'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
}
# Nakshatra lords
nakshatra_lords = {
    'Ashwini': 'Ketu', 'Bharani': 'Venus', 'Krittika': 'Sun', 'Rohini': 'Moon',
    'Mrigashira': 'Mars', 'Ardra': 'Rahu', 'Punarvasu': 'Jupiter', 'Pushya': 'Saturn',
    'Ashlesha': 'Mercury', 'Magha': 'Ketu', 'Purva Phalguni': 'Venus', 'Uttara Phalguni': 'Sun',
    'Hasta': 'Moon', 'Chitra': 'Mars', 'Swati': 'Rahu', 'Vishakha': 'Jupiter',
    'Anuradha': 'Saturn', 'Jyeshtha': 'Mercury', 'Mula': 'Ketu', 'Purva Ashadha': 'Venus',
    'Uttara Ashadha': 'Sun', 'Shravana': 'Moon', 'Dhanishta': 'Mars', 'Shatabhisha': 'Rahu',
    'Purva Bhadrapada': 'Jupiter', 'Uttara Bhadrapada': 'Saturn', 'Revati': 'Mercury'
}
# Exaltation and debilitation signs
exaltation = {
    'Sun': ('Aries', 10),
    'Moon': ('Taurus', 3),
    'Mercury': ('Virgo', 15),
    'Venus': ('Pisces', 27),
    'Mars': ('Capricorn', 28),
    'Jupiter': ('Cancer', 5),
    'Saturn': ('Libra', 20),
}
debilitation = {
    'Sun': ('Libra', 10),
    'Moon': ('Scorpio', 3),
    'Mercury': ('Pisces', 15),
    'Venus': ('Virgo', 27),
    'Mars': ('Cancer', 28),
    'Jupiter': ('Capricorn', 5),
    'Saturn': ('Aries', 20),
}
# Own signs
own_sign_lords = {
    'Sun': 'Leo',
    'Moon': 'Cancer',
    'Mercury': ['Gemini', 'Virgo'],
    'Venus': ['Taurus', 'Libra'],
    'Mars': ['Aries', 'Scorpio'],
    'Jupiter': ['Sagittarius', 'Pisces'],
    'Saturn': ['Capricorn', 'Aquarius'],
}
# Global variable to track if skyfield is available
SKYFIELD_AVAILABLE = False
# Function to check if skyfield is available and initialize it
def check_skyfield():
    global SKYFIELD_AVAILABLE
    try:
        from skyfield.api import load, Topos
        SKYFIELD_AVAILABLE = True
        return load, Topos
    except ImportError:
        SKYFIELD_AVAILABLE = False
        return None, None
# Initialize ephemeris (cached) if skyfield is available
def initialize_ephemeris():
    if not SKYFIELD_AVAILABLE:
        return None, None, None
    
    load, _ = check_skyfield()
    if load is None:
        return None, None, None
        
    eph = load('de421.bsp')
    ts = load.timescale()
    earth = eph['earth']
    return eph, ts, earth
# Calculate planetary positions for a given date and time
def calculate_planetary_positions(selected_date, selected_time, selected_city):
    # Check if skyfield is available
    load, Topos = check_skyfield()
    if not SKYFIELD_AVAILABLE or load is None:
        # Fallback to static data if skyfield is not available
        return get_planetary_positions_fallback(selected_date)
    
    # Get ephemeris data
    eph, ts, earth = initialize_ephemeris()
    if eph is None:
        return get_planetary_positions_fallback(selected_date)
    
    # Get city coordinates
    lat, lon = city_coordinates.get(selected_city, (19.0760, 72.8777))
    location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    # Create datetime object
    dt = datetime.combine(selected_date, selected_time)
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
    # Define planets
    planets = {
        'Sun': eph['sun'],
        'Moon': eph['moon'],
        'Mercury': eph['mercury'],
        'Venus': eph['venus'],
        'Mars': eph['mars'],
        'Jupiter': eph['jupiter barycenter'],
        'Saturn': eph['saturn barycenter'],
        'Uranus': eph['uranus barycenter'],
        'Neptune': eph['neptune barycenter'],
        'Pluto': eph['pluto barycenter'],
    }
    
    positions = []
    for name, planet in planets.items():
        # Calculate the geocentric ecliptic longitude
        astrometric = location.at(t).observe(planet)
        lon, lat, distance = astrometric.ecliptic_latlon()
        degrees = lon.degrees % 360
        
        # Convert to sign and degree in sign
        sign_index = int(degrees / 30)
        sign = zodiac_signs[sign_index]
        degree_in_sign = degrees % 30
        
        # Calculate nakshatra
        nakshatra_index = int(degrees / (360/27)) % 27
        nakshatra = nakshatras[nakshatra_index]
        
        # Get lord and sublord
        lord = sign_lords[sign]
        sublord = nakshatra_lords[nakshatra]
        
        # Determine effect
        effect = 'Neutral'
        if name in exaltation:
            exalt_sign, exalt_degree = exaltation[name]
            if sign == exalt_sign:
                effect = 'Positive'
        if name in debilitation:
            debil_sign, debil_degree = debilitation[name]
            if sign == debil_sign:
                effect = 'Negative'
        
        # If the planet is in its own sign, set to positive (unless already negative)
        if name in own_sign_lords:
            own_signs = own_sign_lords[name]
            if isinstance(own_signs, list):
                if sign in own_signs and effect != 'Negative':
                    effect = 'Positive'
            else:
                if sign == own_signs and effect != 'Negative':
                    effect = 'Positive'
        
        positions.append({
            'Planet': name,
            'Lord': lord,
            'Sublord': sublord,
            'Degree': round(degree_in_sign, 2),
            'House': 0,  # We'll set to 0 for now
            'Nakshatra': nakshatra,
            'Effect': effect
        })
    
    return positions
# Fallback function for planetary positions when skyfield is not available
def get_planetary_positions_fallback(selected_date):
    # Create a seed based on the date for consistent results
    date_seed = int(selected_date.strftime('%Y%m%d'))
    
    # Always generate data for any date
    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Neptune']
    positions = []
    
    # Use the seed to ensure consistent results for the same date
    for i, planet in enumerate(planets):
        # Create a local random generator with the seed
        local_random = random.Random()
        local_random.seed(date_seed + i)
        
        # Get sign index based on date and planet
        sign_index = (date_seed + i) % 12
        sign = zodiac_signs[sign_index]
        
        lord = sign_lords[sign]
        
        # Get nakshatra index
        nakshatra_index = (date_seed + i * 2) % 27
        nakshatra = nakshatras[nakshatra_index]
        
        sublord = nakshatra_lords[nakshatra]
        
        # Generate degree
        degree = round(local_random.uniform(0, 30), 2)
        
        # Generate house
        house = (date_seed + i) % 12 + 1
        
        # Determine effect based on planet and sign
        effect = 'Neutral'
        if planet in exaltation and sign == exaltation[planet][0]:
            effect = 'Positive'
        elif planet in debilitation and sign == debilitation[planet][0]:
            effect = 'Negative'
        elif planet in own_sign_lords:
            own_signs = own_sign_lords[planet]
            if isinstance(own_signs, list):
                if sign in own_signs:
                    effect = 'Positive'
            else:
                if sign == own_signs:
                    effect = 'Positive'
        
        positions.append({
            'Planet': planet,
            'Lord': lord,
            'Sublord': sublord,
            'Degree': degree,
            'House': house,
            'Nakshatra': nakshatra,
            'Effect': effect
        })
    
    return positions
# Check if a planet is retrograde
def is_retrograde(planet_name, t, eph, earth):
    # Skip Sun and Moon as they are never retrograde
    if planet_name in ['Sun', 'Moon']:
        return False
    
    # Get planet
    planet = eph[planet_name.lower() if planet_name != 'Pluto' else 'pluto barycenter']
    
    # Calculate position at current time and 1 hour later
    t1 = t
    t2 = t + timedelta(hours=1)
    
    astrometric1 = earth.at(t1).observe(planet)
    lon1, _, _ = astrometric1.ecliptic_latlon()
    lon1 = lon1.degrees % 360
    
    astrometric2 = earth.at(t2).observe(planet)
    lon2, _, _ = astrometric2.ecliptic_latlon()
    lon2 = lon2.degrees % 360
    
    # Calculate the difference, accounting for the 0-360 boundary
    diff = (lon2 - lon1) % 360
    if diff > 180:
        diff -= 360
    
    # If diff is negative, the planet is retrograde
    return diff < 0
# Get retrograde planets for a given date and time
def get_retrograde_planets_calculated(selected_date, selected_time, selected_city):
    # Check if skyfield is available
    load, Topos = check_skyfield()
    if not SKYFIELD_AVAILABLE or load is None:
        # Fallback to static method if skyfield is not available
        return get_retrograde_planets_fallback(selected_date)
    
    # Get ephemeris data
    eph, ts, earth = initialize_ephemeris()
    if eph is None:
        return get_retrograde_planets_fallback(selected_date)
    
    # Get city coordinates
    lat, lon = city_coordinates.get(selected_city, (19.0760, 72.8777))
    location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    
    # Create datetime object
    dt = datetime.combine(selected_date, selected_time)
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    
    # Define planets to check (skip Sun and Moon)
    planets_to_check = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    
    retrogrades = []
    for planet_name in planets_to_check:
        if is_retrograde(planet_name, t, eph, earth):
            retrogrades.append(f'{planet_name} Retrograde')
    
    return retrogrades
# Fallback function for retrograde planets when skyfield is not available
def get_retrograde_planets_fallback(selected_date):
    retrogrades = []
    
    # Mercury Retrograde periods
    mercury_periods = [
        {'start': '2025-01-01', 'end': '2025-01-25'},
        {'start': '2025-05-18', 'end': '2025-06-11'},
        {'start': '2025-09-09', 'end': '2025-10-02'},
        {'start': '2026-01-02', 'end': '2026-01-26'},
        {'start': '2026-05-19', 'end': '2026-06-12'},
        {'start': '2026-09-10', 'end': '2026-10-03'}
    ]
    
    # Venus Retrograde periods
    venus_periods = [
        {'start': '2025-03-22', 'end': '2025-04-30'},
        {'start': '2026-03-23', 'end': '2026-05-01'}
    ]
    
    # Mars Retrograde periods
    mars_periods = [
        {'start': '2024-12-06', 'end': '2025-02-23'},
        {'start': '2025-07-11', 'end': '2025-09-29'},
        {'start': '2026-12-07', 'end': '2027-02-24'}
    ]
    
    # Jupiter Retrograde periods
    jupiter_periods = [
        {'start': '2025-11-04', 'end': '2026-03-14'},
        {'start': '2026-11-05', 'end': '2027-03-15'}
    ]
    
    # Saturn Retrograde periods
    saturn_periods = [
        {'start': '2025-06-29', 'end': '2025-11-15'},
        {'start': '2026-06-29', 'end': '2026-11-15'}
    ]
    
    # Uranus Retrograde periods
    uranus_periods = [
        {'start': '2025-08-29', 'end': '2026-01-27'},
        {'start': '2026-08-29', 'end': '2027-01-27'}
    ]
    
    # Neptune Retrograde periods
    neptune_periods = [
        {'start': '2025-07-02', 'end': '2025-12-08'},
        {'start': '2026-07-02', 'end': '2026-12-08'}
    ]
    
    # Pluto Retrograde periods
    pluto_periods = [
        {'start': '2025-05-02', 'end': '2025-10-11'},
        {'start': '2026-05-02', 'end': '2026-10-11'}
    ]
    
    # Check if selected date falls within any retrograde period
    for period in mercury_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Mercury Retrograde')
    
    for period in venus_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Venus Retrograde')
    
    for period in mars_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Mars Retrograde')
    
    for period in jupiter_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Jupiter Retrograde')
    
    for period in saturn_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Saturn Retrograde')
    
    for period in uranus_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Uranus Retrograde')
    
    for period in neptune_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Neptune Retrograde')
    
    for period in pluto_periods:
        start_date = datetime.strptime(period['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(period['end'], '%Y-%m-%d').date()
        if start_date <= selected_date <= end_date:
            retrogrades.append('Pluto Retrograde')
    
    return retrogrades
# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Input Date", "Planetary Report", "Planetary Effect", "Upcoming Planetary Transit", "Today Transit"])
# Function to generate moon phases for any month
def generate_moon_phases(year, month):
    phases = []
    
    # New moon (approximate)
    new_moon_day = 1
    phases.append({
        'name': 'New Moon',
        'date': f'{year}-{month:02d}-{new_moon_day:02d}',
        'effect': 'Bullish',
        'description': 'New beginnings, fresh momentum, ideal for starting new projects'
    })
    
    # First quarter (approximate)
    first_quarter_day = 7
    phases.append({
        'name': 'First Quarter',
        'date': f'{year}-{month:02d}-{first_quarter_day:02d}',
        'effect': 'Neutral',
        'description': 'Decision point, overcoming challenges, building momentum'
    })
    
    # Full moon (approximate)
    full_moon_day = 15
    phases.append({
        'name': 'Full Moon',
        'date': f'{year}-{month:02d}-{full_moon_day:02d}',
        'effect': 'Bearish',
        'description': 'Emotional peaks, culmination, profit-taking, increased volatility'
    })
    
    # Last quarter (approximate)
    last_quarter_day = 23
    phases.append({
        'name': 'Last Quarter',
        'date': f'{year}-{month:02d}-{last_quarter_day:02d}',
        'effect': 'Neutral',
        'description': 'Release, letting go, reflection, preparation for new cycle'
    })
    
    return phases
# Function to generate moon transits for any month
def generate_moon_transits(year, month):
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
             'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    days_in_month = calendar.monthrange(year, month)[1]
    transits = []
    current_sign_index = 0
    
    for day in range(1, days_in_month + 1):
        if day % 3 == 1 and day > 1:
            current_sign_index = (current_sign_index + 1) % 12
        
        transits.append({
            'Date': f'{year}-{month:02d}-{day:02d}',
            'Moon Transit': signs[current_sign_index]
        })
    
    return transits
# Function to generate planetary aspects for any month
def generate_planetary_aspects(year, month):
    aspects = []
    
    # Generate some example aspects
    aspects.append({
        'name': 'Jupiter Trine Saturn',
        'start': f'{year}-{month:02d}-01',
        'end': f'{year}-{month:02d}-15',
        'effect': 'Bullish',
        'description': 'Growth with discipline, balanced expansion'
    })
    
    aspects.append({
        'name': 'Mars Square Pluto',
        'start': f'{year}-{month:02d}-03',
        'end': f'{year}-{month:02d}-31',
        'effect': 'Bearish',
        'description': 'Power struggles, institutional conflicts'
    })
    
    if month == 8:  # Special case for August
        aspects.append({
            'name': 'Venus Sextile Jupiter',
            'start': f'{year}-{month:02d}-02',
            'end': f'{year}-{month:02d}-02',
            'effect': 'Bullish',
            'description': 'Positive social mood, consumer spending'
        })
    
    aspects.append({
        'name': 'Sun Oppose Saturn',
        'start': f'{year}-{month:02d}-13',
        'end': f'{year}-{month:02d}-13',
        'effect': 'Bearish',
        'description': 'Authority challenges, limitations'
    })
    
    aspects.append({
        'name': 'Mercury Conjunct Venus',
        'start': f'{year}-{month:02d}-19',
        'end': f'{year}-{month:02d}-19',
        'effect': 'Bullish',
        'description': 'Harmonious communication, financial discussions'
    })
    
    return aspects
# Function to get planetary positions for a specific date
def get_planetary_positions(selected_date):
    return calculate_planetary_positions(
        selected_date, 
        st.session_state.selected_time, 
        st.session_state.selected_city
    )
# Function to get next house changes for a specific date
def get_next_house_changes(selected_date):
    # Create a seed based on the date for consistent results
    date_seed = int(selected_date.strftime('%Y%m%d'))
    
    # Always generate data for any date
    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Neptune']
    changes = []
    
    for i, planet in enumerate(planets):
        # Create a local random generator with the seed
        local_random = random.Random()
        local_random.seed(date_seed + i)
        
        current_house = (date_seed + i) % 12 + 1
        next_house = 1 if current_house == 12 else current_house + 1
        degree_at_change = round(local_random.uniform(0, 30), 2)
        
        nakshatra_index = (date_seed + i * 2) % 27
        nakshatra_at_change = nakshatras[nakshatra_index]
        
        # Generate a future date within 7 days
        days_ahead = (date_seed + i) % 7 + 1
        hours_ahead = (date_seed + i * 3) % 24
        minutes_ahead = (date_seed + i * 5) % 60
        change_datetime = selected_date + timedelta(days=days_ahead, hours=hours_ahead, minutes=minutes_ahead)
        
        changes.append({
            'Planet': planet,
            'Current House': current_house,
            'Next House': next_house,
            'Degree at Change': degree_at_change,
            'Nakshatra at Change': nakshatra_at_change,
            'Time of Change': change_datetime.strftime('%Y-%m-%d %H:%M')
        })
    
    return changes
# Function to get intraday aspects for a specific date
def get_intraday_aspects(selected_date):
    # Create a seed based on the date for consistent results
    date_seed = int(selected_date.strftime('%Y%m%d'))
    
    # Always generate data for any date
    aspect_types = ['Conjunction', 'Sextile', 'Square', 'Trine', 'Opposition']
    planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
    
    # Determine number of aspects based on date seed
    num_aspects = (date_seed % 3) + 4  # Between 4-6 aspects
    aspects = []
    
    for i in range(num_aspects):
        # Create a local random generator with the seed
        local_random = random.Random()
        local_random.seed(date_seed + i)
        
        # Generate time
        hour = 9 + (date_seed + i) % 7  # Between 9-15
        minute = (date_seed + i * 7) % 60
        if hour == 15 and minute > 30:
            minute = 30
        time_str = f"{hour:02d}:{minute:02d}"
        
        aspect_type = aspect_types[(date_seed + i) % len(aspect_types)]
        planet1_index = (date_seed + i) % len(planets)
        planet1 = planets[planet1_index]
        planet2_index = (date_seed + i * 2) % (len(planets) - 1)
        if planet2_index >= planet1_index:
            planet2_index += 1
        planet2 = planets[planet2_index]
        
        effect_options = ['Bullish', 'Bearish', 'Neutral', 'Volatile', 'Mildly Bullish']
        effect = effect_options[(date_seed + i * 3) % len(effect_options)]
        
        if aspect_type == 'Conjunction':
            description = f"Combining energies of {planet1} and {planet2}"
        elif aspect_type == 'Sextile':
            description = f"Harmonious opportunity between {planet1} and {planet2}"
        elif aspect_type == 'Square':
            description = f"Tension between {planet1} and {planet2}"
        elif aspect_type == 'Trine':
            description = f"Flowing energy between {planet1} and {planet2}"
        else:  # Opposition
            description = f"Polarity between {planet1} and {planet2}"
        
        aspects.append({
            'Time': time_str,
            'Aspect': f"{planet1} {aspect_type} {planet2}",
            'Effect': effect,
            'Description': description
        })
    
    # Sort aspects by time
    aspects.sort(key=lambda x: x['Time'])
    return aspects
# Function to create birth chart visualization
def create_birth_chart(planetary_positions, title="Birth Chart / Natal Chart"):
    # Define zodiac signs and their degrees
    zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    
    # Create a figure with polar coordinates
    fig = go.Figure()
    
    # Add the outer circle for the zodiac
    theta = np.linspace(0, 2*np.pi, 100)
    r = np.ones_like(theta) * 12
    
    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=theta * 180/np.pi,
        mode='lines',
        line=dict(color='black', width=2),
        showlegend=False
    ))
    
    # Add zodiac sign labels
    for i, sign in enumerate(zodiac_signs):
        angle = i * 30  # Each sign spans 30 degrees
        fig.add_trace(go.Scatterpolar(
            r=[13],
            theta=[angle],
            mode='text',
            text=sign,
            textfont=dict(size=12, color='black'),
            showlegend=False
        ))
    
    # Add house lines
    for i in range(12):
        angle = i * 30
        fig.add_trace(go.Scatterpolar(
            r=[0, 12],
            theta=[angle, angle],
            mode='lines',
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=False
        ))
    
    # Add house numbers
    for i in range(12):
        angle = i * 30 + 15  # Middle of the house
        fig.add_trace(go.Scatterpolar(
            r=[6],
            theta=[angle],
            mode='text',
            text=str(i+1),
            textfont=dict(size=10, color='gray'),
            showlegend=False
        ))
    
    # Define planet symbols
    planet_symbols = {
        'Sun': '☉',
        'Moon': '☽',
        'Mercury': '☿',
        'Venus': '♀',
        'Mars': '♂',
        'Jupiter': '♃',
        'Saturn': '♄',
        'Rahu': '☊',
        'Ketu': '☋',
        'Neptune': '♆'
    }
    
    # Add planets to the chart
    for planet in planetary_positions:
        # Calculate position based on house and degree
        house = planet['House']
        degree = planet['Degree']
        
        # Convert to angle (0-360 degrees)
        angle = (house - 1) * 30 + degree
        
        # Add planet symbol
        fig.add_trace(go.Scatterpolar(
            r=[10],
            theta=[angle],
            mode='markers+text',
            marker=dict(size=20, color='blue'),
            text=planet_symbols.get(planet['Planet'], planet['Planet'][0]),
            textfont=dict(size=14, color='white'),
            name=f"{planet['Planet']} (House {house}, {degree}°)",
            showlegend=True
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 14]
            ),
            angularaxis=dict(
                visible=False,
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title=title,
        title_x=0.5,
        height=600
    )
    
    return fig
# Function to get all planetary transits for a year
def get_all_planetary_transits(year):
    transits = []
    
    # Mercury transits
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Capricorn',
        'To': 'Aquarius',
        'Start': f'{year}-01-25',
        'End': f'{year}-02-13',
        'Effect': 'Bullish',
        'Description': 'Clear communication, intellectual growth'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Aquarius',
        'To': 'Pisces',
        'Start': f'{year}-02-13',
        'End': f'{year}-03-01',
        'Effect': 'Bullish',
        'Description': 'Intuitive thinking, creative expression'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aries',
        'Start': f'{year}-03-01',
        'End': f'{year}-03-16',
        'Effect': 'Bullish',
        'Description': 'Assertive communication, new ideas'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Aries',
        'To': 'Taurus',
        'Start': f'{year}-03-16',
        'End': f'{year}-05-03',
        'Effect': 'Bullish',
        'Description': 'Practical thinking, financial focus'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Retrograde',
        'From': 'Taurus',
        'To': 'Aries',
        'Start': f'{year}-05-18',
        'End': f'{year}-06-11',
        'Effect': 'Bearish',
        'Description': 'Communication issues, tech problems'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Aries',
        'To': 'Taurus',
        'Start': f'{year}-06-11',
        'End': f'{year}-06-26',
        'Effect': 'Bullish',
        'Description': 'Clear thinking, practical decisions'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Taurus',
        'To': 'Gemini',
        'Start': f'{year}-06-26',
        'End': f'{year}-07-10',
        'Effect': 'Bullish',
        'Description': 'Social communication, networking'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Gemini',
        'To': 'Cancer',
        'Start': f'{year}-07-10',
        'End': f'{year}-07-25',
        'Effect': 'Bullish',
        'Description': 'Emotional communication, family focus'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Cancer',
        'To': 'Leo',
        'Start': f'{year}-07-25',
        'End': f'{year}-09-09',
        'Effect': 'Bullish',
        'Description': 'Creative expression, leadership'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Retrograde',
        'From': 'Leo',
        'To': 'Cancer',
        'Start': f'{year}-09-09',
        'End': f'{year}-10-02',
        'Effect': 'Bearish',
        'Description': 'Communication breakdowns, tech issues'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Cancer',
        'To': 'Leo',
        'Start': f'{year}-10-02',
        'End': f'{year}-10-17',
        'Effect': 'Bullish',
        'Description': 'Clear communication, emotional intelligence'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Leo',
        'To': 'Virgo',
        'Start': f'{year}-10-17',
        'End': f'{year}-11-01',
        'Effect': 'Bullish',
        'Description': 'Analytical thinking, attention to detail'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Libra',
        'Start': f'{year}-11-01',
        'End': f'{year}-11-19',
        'Effect': 'Bullish',
        'Description': 'Diplomatic communication, social harmony'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Libra',
        'To': 'Scorpio',
        'Start': f'{year}-11-19',
        'End': f'{year}-12-07',
        'Effect': 'Bullish',
        'Description': 'Deep communication, investigation'
    })
    transits.append({
        'Planet': 'Mercury',
        'Event': 'Direct',
        'From': 'Scorpio',
        'To': 'Sagittarius',
        'Start': f'{year}-12-07',
        'End': f'{year}-12-26',
        'Effect': 'Bullish',
        'Description': 'Philosophical thinking, big ideas'
    })
    
    # Venus transits
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Capricorn',
        'To': 'Aquarius',
        'Start': f'{year}-01-01',
        'End': f'{year}-01-27',
        'Effect': 'Bullish',
        'Description': 'Social progress, humanitarian values'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Aquarius',
        'To': 'Pisces',
        'Start': f'{year}-01-27',
        'End': f'{year}-02-20',
        'Effect': 'Bullish',
        'Description': 'Romantic idealism, artistic inspiration'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aries',
        'Start': f'{year}-02-20',
        'End': f'{year}-03-16',
        'Effect': 'Bullish',
        'Description': 'Passionate relationships, bold actions'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Retrograde',
        'From': 'Aries',
        'To': 'Pisces',
        'Start': f'{year}-03-22',
        'End': f'{year}-04-30',
        'Effect': 'Bearish',
        'Description': 'Relationship issues, financial reevaluation'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aries',
        'Start': f'{year}-04-30',
        'End': f'{year}-05-23',
        'Effect': 'Bullish',
        'Description': 'Renewed passion, relationship clarity'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Aries',
        'To': 'Taurus',
        'Start': f'{year}-05-23',
        'End': f'{year}-06-17',
        'Effect': 'Bullish',
        'Description': 'Stable relationships, financial growth'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Taurus',
        'To': 'Gemini',
        'Start': f'{year}-06-17',
        'End': f'{year}-07-11',
        'Effect': 'Bullish',
        'Description': 'Social connections, communication in love'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Gemini',
        'To': 'Cancer',
        'Start': f'{year}-07-11',
        'End': f'{year}-08-05',
        'Effect': 'Bullish',
        'Description': 'Emotional bonds, nurturing relationships'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Cancer',
        'To': 'Leo',
        'Start': f'{year}-08-05',
        'End': f'{year}-08-29',
        'Effect': 'Bullish',
        'Description': 'Romantic expression, creative love'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Leo',
        'To': 'Virgo',
        'Start': f'{year}-08-29',
        'End': f'{year}-09-22',
        'Effect': 'Bullish',
        'Description': 'Practical love, attention to detail'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Libra',
        'Start': f'{year}-09-22',
        'End': f'{year}-10-17',
        'Effect': 'Bullish',
        'Description': 'Harmonious relationships, social grace'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Libra',
        'To': 'Scorpio',
        'Start': f'{year}-10-17',
        'End': f'{year}-11-11',
        'Effect': 'Bullish',
        'Description': 'Deep connections, passionate love'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Scorpio',
        'To': 'Sagittarius',
        'Start': f'{year}-11-11',
        'End': f'{year}-12-06',
        'Effect': 'Bullish',
        'Description': 'Adventurous relationships, philosophical love'
    })
    transits.append({
        'Planet': 'Venus',
        'Event': 'Direct',
        'From': 'Sagittarius',
        'To': 'Capricorn',
        'Start': f'{year}-12-06',
        'End': f'{year}-12-31',
        'Effect': 'Bullish',
        'Description': 'Committed relationships, long-term planning'
    })
    
    # Mars transits
    transits.append({
        'Planet': 'Mars',
        'Event': 'Retrograde',
        'From': 'Cancer',
        'To': 'Gemini',
        'Start': f'{year}-01-01',
        'End': f'{year}-02-23',
        'Effect': 'Bearish',
        'Description': 'Energy drain, conflicts, delays'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Gemini',
        'To': 'Cancer',
        'Start': f'{year}-02-23',
        'End': f'{year}-04-04',
        'Effect': 'Bullish',
        'Description': 'Renewed energy, communication drive'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Cancer',
        'To': 'Leo',
        'Start': f'{year}-04-04',
        'End': f'{year}-05-15',
        'Effect': 'Bullish',
        'Description': 'Confident action, leadership energy'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Leo',
        'To': 'Virgo',
        'Start': f'{year}-05-15',
        'End': f'{year}-06-27',
        'Effect': 'Bullish',
        'Description': 'Detailed action, service-oriented energy'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Libra',
        'Start': f'{year}-06-27',
        'End': f'{year}-08-08',
        'Effect': 'Bullish',
        'Description': 'Diplomatic action, relationship focus'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Retrograde',
        'From': 'Libra',
        'To': 'Virgo',
        'Start': f'{year}-07-11',
        'End': f'{year}-09-29',
        'Effect': 'Bearish',
        'Description': 'Energy drain, conflicts, delays in action'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Libra',
        'Start': f'{year}-09-29',
        'End': f'{year}-11-10',
        'Effect': 'Bullish',
        'Description': 'Renewed energy, balanced action'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Libra',
        'To': 'Scorpio',
        'Start': f'{year}-11-10',
        'End': f'{year}-12-20',
        'Effect': 'Bullish',
        'Description': 'Intense action, transformative energy'
    })
    transits.append({
        'Planet': 'Mars',
        'Event': 'Direct',
        'From': 'Scorpio',
        'To': 'Sagittarius',
        'Start': f'{year}-12-20',
        'End': f'{year}-12-31',
        'Effect': 'Bullish',
        'Description': 'Adventurous action, philosophical drive'
    })
    
    # Jupiter transits
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Taurus',
        'To': 'Gemini',
        'Start': f'{year}-01-01',
        'End': f'{year}-05-25',
        'Effect': 'Bullish',
        'Description': 'Growth in communication, learning expansion'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Gemini',
        'To': 'Cancer',
        'Start': f'{year}-05-25',
        'End': f'{year}-06-01',
        'Effect': 'Bullish',
        'Description': 'Growth in emotional security, home expansion'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Cancer',
        'To': 'Leo',
        'Start': f'{year}-06-01',
        'End': f'{year}-07-13',
        'Effect': 'Bullish',
        'Description': 'Growth in creativity, self-expression'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Leo',
        'To': 'Virgo',
        'Start': f'{year}-07-13',
        'End': f'{year}-08-27',
        'Effect': 'Bullish',
        'Description': 'Growth in service, health improvement'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Libra',
        'Start': f'{year}-08-27',
        'End': f'{year}-10-09',
        'Effect': 'Bullish',
        'Description': 'Growth in relationships, social harmony'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Direct',
        'From': 'Libra',
        'To': 'Scorpio',
        'Start': f'{year}-10-09',
        'End': f'{year}-11-20',
        'Effect': 'Bullish',
        'Description': 'Growth in depth, transformation'
    })
    transits.append({
        'Planet': 'Jupiter',
        'Event': 'Retrograde',
        'From': 'Scorpio',
        'To': 'Libra',
        'Start': f'{year}-11-04',
        'End': f'{year}-12-31',
        'Effect': 'Bearish',
        'Description': 'Growth slowdown, reassessment of relationships'
    })
    
    # Saturn transits
    transits.append({
        'Planet': 'Saturn',
        'Event': 'Direct',
        'From': 'Aquarius',
        'To': 'Pisces',
        'Start': f'{year}-01-01',
        'End': f'{year}-03-29',
        'Effect': 'Bearish',
        'Description': 'Structural changes, spiritual challenges'
    })
    transits.append({
        'Planet': 'Saturn',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aries',
        'Start': f'{year}-03-29',
        'End': f'{year}-05-24',
        'Effect': 'Bearish',
        'Description': 'Disciplined action, new structures'
    })
    transits.append({
        'Planet': 'Saturn',
        'Event': 'Direct',
        'From': 'Aries',
        'To': 'Taurus',
        'Start': f'{year}-05-24',
        'End': f'{year}-06-29',
        'Effect': 'Bearish',
        'Description': 'Practical discipline, financial stability'
    })
    transits.append({
        'Planet': 'Saturn',
        'Event': 'Retrograde',
        'From': 'Taurus',
        'To': 'Aries',
        'Start': f'{year}-06-29',
        'End': f'{year}-11-15',
        'Effect': 'Bearish',
        'Description': 'Restructuring delays, karmic lessons'
    })
    transits.append({
        'Planet': 'Saturn',
        'Event': 'Direct',
        'From': 'Aries',
        'To': 'Taurus',
        'Start': f'{year}-11-15',
        'End': f'{year}-12-31',
        'Effect': 'Bearish',
        'Description': 'Renewed discipline, practical structures'
    })
    
    # Rahu transits
    transits.append({
        'Planet': 'Rahu',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aquarius',
        'Start': f'{year}-01-01',
        'End': f'{year}-03-29',
        'Effect': 'Bearish',
        'Description': 'Material desires, ambition'
    })
    transits.append({
        'Planet': 'Rahu',
        'Event': 'Direct',
        'From': 'Aquarius',
        'To': 'Pisces',
        'Start': f'{year}-03-29',
        'End': f'{year}-12-31',
        'Effect': 'Bearish',
        'Description': 'Spiritual confusion, illusion'
    })
    
    # Ketu transits
    transits.append({
        'Planet': 'Ketu',
        'Event': 'Direct',
        'From': 'Virgo',
        'To': 'Leo',
        'Start': f'{year}-01-01',
        'End': f'{year}-03-29',
        'Effect': 'Bearish',
        'Description': 'Spiritual detachment, liberation'
    })
    transits.append({
        'Planet': 'Ketu',
        'Event': 'Direct',
        'From': 'Leo',
        'To': 'Virgo',
        'Start': f'{year}-03-29',
        'End': f'{year}-12-31',
        'Effect': 'Bearish',
        'Description': 'Service, healing, perfection'
    })
    
    # Neptune transits
    transits.append({
        'Planet': 'Neptune',
        'Event': 'Direct',
        'From': 'Pisces',
        'To': 'Aries',
        'Start': f'{year}-01-01',
        'End': f'{year}-05-03',
        'Effect': 'Bearish',
        'Description': 'Spiritual confusion, illusion'
    })
    transits.append({
        'Planet': 'Neptune',
        'Event': 'Retrograde',
        'From': 'Aries',
        'To': 'Pisces',
        'Start': f'{year}-05-03',
        'End': f'{year}-12-08',
        'Effect': 'Bearish',
        'Description': 'Uncertainty, deception, spiritual confusion'
    })
    
    return transits
# Function to display upcoming transits in box table format
def display_upcoming_transits(year, month):
    # Get all transits for the year
    all_transits = get_all_planetary_transits(year)
    
    # Group transits by month
    monthly_transits = {i: [] for i in range(1, 13)}
    
    for transit in all_transits:
        start_date = datetime.strptime(transit['Start'], '%Y-%m-%d')
        if start_date.year == year:
            monthly_transits[start_date.month].append(transit)
    
    # Create a grid of 12 boxes (one for each month)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Create a 3x4 grid
    for i in range(0, 12, 3):
        cols = st.columns(3)
        for j in range(3):
            month_idx = i + j
            month_name = months[month_idx]
            month_transits = monthly_transits[month_idx + 1]  # +1 because months are 1-indexed
            
            with cols[j]:
                # Highlight the selected month
                if month_idx + 1 == month:
                    st.markdown(f"#### :blue[{month_name} {year}]")
                else:
                    st.markdown(f"#### {month_name} {year}")
                
                if month_transits:
                    for transit in month_transits:
                        # Format the date range
                        start_date = datetime.strptime(transit['Start'], '%Y-%m-%d').strftime('%b %d')
                        end_date = datetime.strptime(transit['End'], '%Y-%m-%d').strftime('%b %d')
                        
                        # Create a box for each transit
                        with st.container():
                            st.markdown(f"""
                            <div style="background-color: {'#d4edda' if transit['Effect'] == 'Bullish' else '#f8d7da'}; 
                                        padding: 10px; 
                                        border-radius: 5px; 
                                        margin-bottom: 10px;">
                                <b>{transit['Planet']} {transit['Event']}</b><br>
                                {transit['From']} → {transit['To']}<br>
                                {start_date} - {end_date}<br>
                                <i>{transit['Description']}</i>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No major transits this month")
# Tab 1: Input Date
with tab1:
    st.header("Select Date for Report")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create date selection with year, month, and day
        selected_year = st.selectbox("Select Year", range(2020, 2031), index=5)
        selected_month = st.selectbox("Select Month", range(1, 13), index=7)
        
        # Get days in selected month
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]
        selected_day = st.selectbox("Select Day", range(1, days_in_month + 1), index=3)  # Changed default to 4th day
        
        selected_date = date(selected_year, selected_month, selected_day)
        st.session_state.selected_date = selected_date
        
        # Add time selection
        selected_time = st.time_input("Select Time", value=st.session_state.selected_time)
        st.session_state.selected_time = selected_time
        
        # City selection
        cities = ["Mumbai, India", "Delhi, India", "Bangalore, India", "Kolkata, India", "Chennai, India", 
                 "New York, USA", "London, UK", "Tokyo, Japan", "Sydney, Australia", "Dubai, UAE"]
        selected_city = st.selectbox("Select City", cities, index=0)
        st.session_state.selected_city = selected_city
        
        st.markdown(f"**Selected Date:** {selected_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**Selected Time:** {selected_time.strftime('%H:%M')}")
        st.markdown(f"**Location:** {selected_city}")
        
        if st.button("Generate Report"):
            st.success(f"Report will be generated for {selected_date.strftime('%Y-%m-%d')} at {selected_time.strftime('%H:%M')} in {selected_city}")
    
    # Add birth chart visualization
    st.markdown("---")
    st.header("Birth Chart / Natal Chart")
    
    # Get planetary positions for the selected date
    planetary_positions = get_planetary_positions(st.session_state.selected_date)
    
    # Create title with date and time
    chart_title = f"Birth Chart / Natal Chart - {st.session_state.selected_date.strftime('%Y-%m-%d')} {st.session_state.selected_time.strftime('%H:%M')}"
    
    # Create and display the birth chart
    birth_chart = create_birth_chart(planetary_positions, title=chart_title)
    st.plotly_chart(birth_chart, use_container_width=True)
    
    # Display planetary positions data
    st.markdown("### Planetary Positions")
    positions_df = pd.DataFrame(planetary_positions)
    st.dataframe(positions_df, use_container_width=True)
    
    # Add upcoming transits section
    st.markdown("---")
    st.header(f"Upcoming Planetary Transits {selected_year}")
    st.markdown(f"Showing transits for {selected_city}")
    
    # Display upcoming transits in box table format
    display_upcoming_transits(selected_year, selected_month)
# Generate dynamic data based on selected date
selected_year = st.session_state.selected_date.year
selected_month = st.session_state.selected_date.month
# Generate moon phases for selected month
moon_phases = generate_moon_phases(selected_year, selected_month)
# Generate moon transits for selected month
moon_transits = generate_moon_transits(selected_year, selected_month)
moon_transit_df = pd.DataFrame(moon_transits)
moon_transit_df['Date'] = pd.to_datetime(moon_transit_df['Date'])
# Generate planetary aspects for selected month
planetary_aspects = generate_planetary_aspects(selected_year, selected_month)
# Get retrograde planets for selected date (now uses live calculation or fallback)
retrograde_planets = get_retrograde_planets_calculated(
    st.session_state.selected_date,
    st.session_state.selected_time,
    st.session_state.selected_city
)
# Create planetary details dictionary with dynamic data
planetary_details = {
    'Planetary Transit': [
        {'name': 'Mercury in Virgo', 'start': f'{selected_year}-{selected_month:02d}-25', 'end': f'{selected_year}-{selected_month:02d}-14', 'effect': 'Bullish', 'description': 'Analytical clarity, communication efficiency'},
        {'name': 'Venus in Libra', 'start': f'{selected_year}-{selected_month:02d}-31', 'end': f'{selected_year}-{selected_month:02d}-06', 'effect': 'Bullish', 'description': 'Diplomatic stability, social harmony'},
        {'name': 'Mars in Gemini', 'start': f'{selected_year}-{selected_month:02d}-20', 'end': f'{selected_year}-{selected_month:02d}-04', 'effect': 'Bearish', 'description': 'Volatile energy, scattered focus'},
        {'name': 'Jupiter in Gemini', 'start': f'{selected_year}-{selected_month:02d}-25', 'end': f'{selected_year}-{selected_month:02d}-09', 'effect': 'Bullish', 'description': 'Expansion in communication, learning'},
        {'name': 'Saturn in Pisces', 'start': f'{selected_year}-{selected_month:02d}-07', 'end': f'{selected_year}-{selected_month:02d}-24', 'effect': 'Bearish', 'description': 'Restructuring, spiritual challenges'}
    ],
    'Planetary Aspect': planetary_aspects,
    'Planetary Retrograde': [
        {'name': 'Mercury Retrograde', 'start': '2025-01-01', 'end': '2025-01-25', 'effect': 'Bearish', 'description': 'Communication issues, tech volatility, delays'},
        {'name': 'Mercury Retrograde', 'start': '2025-05-18', 'end': '2025-06-11', 'effect': 'Bearish', 'description': 'Communication issues, tech volatility, delays'},
        {'name': 'Mercury Retrograde', 'start': '2025-09-09', 'end': '2025-10-02', 'effect': 'Bearish', 'description': 'Communication issues, tech volatility, delays'},
        {'name': 'Venus Retrograde', 'start': '2025-03-22', 'end': '2025-04-30', 'effect': 'Bearish', 'description': 'Relationship issues, financial reevaluation'},
        {'name': 'Mars Retrograde', 'start': '2024-12-06', 'end': '2025-02-23', 'effect': 'Bearish', 'description': 'Energy drain, conflicts, delays in action'},
        {'name': 'Mars Retrograde', 'start': '2025-07-11', 'end': '2025-09-29', 'effect': 'Bearish', 'description': 'Energy drain, conflicts, delays in action'},
        {'name': 'Jupiter Retrograde', 'start': '2025-11-04', 'end': '2026-03-14', 'effect': 'Bearish', 'description': 'Growth slowdown, reassessment of beliefs'},
        {'name': 'Saturn Retrograde', 'start': '2025-06-29', 'end': '2025-11-15', 'effect': 'Bearish', 'description': 'Restructuring delays, karmic lessons'},
        {'name': 'Uranus Retrograde', 'start': '2025-08-29', 'end': '2026-01-27', 'effect': 'Bearish', 'description': 'Rebellion against change, technological disruptions'},
        {'name': 'Neptune Retrograde', 'start': '2025-07-02', 'end': '2025-12-08', 'effect': 'Bearish', 'Description': 'Uncertainty, deception, spiritual confusion'},
        {'name': 'Pluto Retrograde', 'start': '2025-05-02', 'end': '2025-10-11', 'effect': 'Bullish', 'description': 'Transformational opportunities, deep changes'}
    ],
    'Moon Phases': moon_phases
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
    },
    'Mars Retrograde': {
        'Sectors': ['Energy', 'Defense', 'Automotive'],
        'Indices': ['Russell 2000', 'Volatility Index'],
        'Assets': ['Commodity currencies', 'Small-cap stocks'],
        'Commodities': ['Oil', 'Steel'],
        'Effect': 'Bearish - Energy drain, conflicts, delays in action'
    },
    'Saturn Retrograde': {
        'Sectors': ['Banking', 'Government', 'Infrastructure'],
        'Indices': ['S&P 500', 'Dow Jones'],
        'Assets': ['Government bonds', 'Blue-chip stocks'],
        'Commodities': ['Gold', 'Industrial metals'],
        'Effect': 'Bearish - Restructuring delays, karmic lessons'
    },
    'Uranus Retrograde': {
        'Sectors': ['Technology', 'Aerospace', 'Renewable Energy'],
        'Indices': ['NASDAQ', 'Clean Energy Index'],
        'Assets': ['Tech stocks', 'Growth stocks'],
        'Commodities': ['Uranium', 'Rare earth elements'],
        'Effect': 'Bearish - Rebellion against change, technological disruptions'
    },
    'Neptune Retrograde': {
        'Sectors': ['Pharmaceuticals', 'Oil & Gas', 'Media'],
        'Indices': ['Healthcare Index', 'Energy Index'],
        'Assets': ['Pharma stocks', 'Energy stocks'],
        'Commodities': ['Oil', 'Natural gas'],
        'Effect': 'Bearish - Uncertainty, deception, spiritual confusion'
    },
    'Pluto Retrograde': {
        'Sectors': ['Finance', 'Mining', 'Psychology'],
        'Indices': ['Financial Index', 'Gold Index'],
        'Assets': ['Financial stocks', 'Gold'],
        'Commodities': ['Gold', 'Platinum'],
        'Effect': 'Bullish - Transformational opportunities, deep changes'
    }
}
# Intraday moon aspects (updated with correct real-time data for August 4, 2025)
intraday_moon_aspects = {
    '2025-08-04': [
        {'time': '09:15', 'aspect': 'Moon in Jyeshtha (Scorpio)', 'effect': 'Bearish', 'description': 'Rahu aspects Moon (exact trine). Saturn-Rahu conjunction in Pisces creates volatility.'},
        {'time': '10:15', 'aspect': 'Mercury in Pushya (Cancer)', 'effect': 'Bearish', 'description': 'Mercury in Pushya aspected by Rahu. Technical breakdown likely.'},
        {'time': '11:15', 'aspect': 'Sun in Ashlesha (Cancer)', 'effect': 'Bullish (short-lived)', 'description': 'Sun in Ashlesha aspected by Rahu, but Jupiter\'s 7th aspect provides support.'},
        {'time': '12:15', 'aspect': 'Venus in Ardra (Gemini)', 'effect': 'Volatile', 'description': 'Venus in Ardra under Rahu\'s 5th aspect. Profit-booking likely.'},
        {'time': '13:15', 'aspect': 'Moon in Jyeshtha (Scorpio)', 'effect': 'Bearish', 'description': 'Moon debilitated in Scorpio. Ketu sublord intensifies reversals.'},
        {'time': '14:15', 'aspect': 'Mars in Uttara Phalguni (Leo)', 'effect': 'Bearish', 'description': 'Mars in Uttara Phalguni aspected by Rahu. Banking sector pressure.'},
        {'time': '15:15', 'aspect': 'Jupiter in Ardra (Gemini)', 'effect': 'Mildly Bullish', 'description': 'Jupiter in Ardra aspected by Saturn. Mild recovery attempt.'},
        {'time': '15:30', 'aspect': 'Market Close', 'effect': 'Bearish', 'description': 'Moon at 23° Scorpio. Rahu influence dominates.'}
    ],
    '2025-08-05': [
        {'time': '10:00', 'aspect': 'Moon Conjunct Mars', 'effect': 'Bearish', 'description': 'Aggressive energy, impulsive decisions'},
        {'time': '12:30', 'aspect': 'Moon Trine Uranus', 'effect': 'Bullish', 'description': 'Innovation, tech rally, unexpected opportunities'},
        {'time': '14:45', 'aspect': 'Moon Oppose Saturn', 'effect': 'Bearish', 'description': 'Restrictions, limitations, conservative approach'},
        {'time': '16:00', 'aspect': 'Moon Sextile Venus', 'effect': 'Bullish', 'description': 'Harmony, social connections, positive close'}
    ]
}
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
    selected_time_str = st.session_state.selected_time.strftime('%H:%M')
    st.subheader(f"Effects for {selected_date_str} at {selected_time_str}")
    
    # Find active events for the selected date
    active_events = []
    
    # Convert selected_date to datetime for comparison
    selected_datetime = datetime.combine(st.session_state.selected_date, st.session_state.selected_time)
    
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
    for retrograde in retrograde_planets:
        active_events.append(retrograde)
    
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
        st.info("No significant planetary events for the selected date and time.")
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
            
            colors = {'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray', 'Volatile': 'orange', 'Mildly Bullish': 'lightgreen', 'Bullish (short-lived)': 'lightgreen'}
            
            for _, aspect in aspects_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[aspect['time']],
                    y=[aspect['aspect']],
                    mode='markers',
                    marker=dict(
                        color=colors.get(aspect['effect'], 'blue'),
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
        
        # Create a categorical plot for moon signs
        moon_signs = moon_transit_df['Moon Transit'].unique()
        
        for i, sign in enumerate(moon_signs):
            sign_data = moon_transit_df[moon_transit_df['Moon Transit'] == sign]
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
            title=f"Moon Transit Through Zodiac Signs - {selected_year} {calendar.month_name[selected_month]}",
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
        st.dataframe(moon_transit_df, use_container_width=True)
# Tab 5: Today Transit
with tab5:
    st.header("Today Transit")
    selected_date_str = st.session_state.selected_date.strftime('%Y-%m-%d')
    selected_time_str = st.session_state.selected_time.strftime('%H:%M')
    st.subheader(f"Planetary Transit Details for {selected_date_str} at {selected_time_str}")
    
    # Get planetary positions for the selected date
    planetary_positions = get_planetary_positions(st.session_state.selected_date)
    
    # Part 1: Planetary positions
    st.markdown("### Planetary Positions")
    positions_df = pd.DataFrame(planetary_positions)
    st.dataframe(positions_df, use_container_width=True)
    
    # Get next house changes
    next_house_changes = get_next_house_changes(st.session_state.selected_date)
    
    # Part 2: Next house changes
    st.markdown("### Upcoming House Changes")
    changes_df = pd.DataFrame(next_house_changes)
    st.dataframe(changes_df, use_container_width=True)
    
    # Get intraday aspects
    intraday_aspects = get_intraday_aspects(st.session_state.selected_date)
    
    # Part 3: Intraday aspects
    st.markdown("### Intraday Planetary Aspects")
    intraday_df = pd.DataFrame(intraday_aspects)
    st.dataframe(intraday_df, use_container_width=True)
    
    # Create a timeline chart for intraday aspects
    fig = go.Figure()
    
    colors = {'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray', 'Volatile': 'orange', 'Mildly Bullish': 'lightgreen', 'Bullish (short-lived)': 'lightgreen'}
    
    for _, aspect in intraday_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[aspect['Time']],
            y=[aspect['Aspect']],
            mode='markers',
            marker=dict(
                color=colors.get(aspect['Effect'], 'blue'),
                size=20,
                symbol='diamond',
                line=dict(width=1, color='black')
            ),
            text=f"{aspect['Description']}<br>Effect: {aspect['Effect']}",
            hovertemplate='<b>%{y}</b><br>Time: %{x}<br>%{text}<extra></extra>',
            name=aspect['Aspect']
        ))
    
    fig.update_layout(
        title=f"Intraday Planetary Aspects for {selected_date_str}",
        xaxis_title="Time",
        yaxis_title="Planetary Aspect",
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show a message if skyfield is not available
    if not SKYFIELD_AVAILABLE:
        st.warning("""
        **Note**: The skyfield library is not installed in this environment. 
        The app is using fallback data for planetary positions and retrograde calculations.
        
        For live planetary calculations, please install the skyfield library:
        ```
        pip install skyfield
        ```
        """)
# Add a footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Astro Transit For Daily Transit &copy; 2025</p>", unsafe_allow_html=True)
