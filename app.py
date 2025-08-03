# Function to get planetary positions for a specific date
def get_planetary_positions(selected_date):
    # Specific data for August 4, 2025 (updated with correct real-time data)
    if selected_date == date(2025, 8, 4):
        return [
            {'Planet': 'Sun', 'Lord': 'Moon', 'Sublord': 'Mercury', 'Degree': 17.49, 'House': 2, 'Nakshatra': 'Ashlesha', 'Effect': 'Positive'},
            {'Planet': 'Moon', 'Lord': 'Mercury', 'Sublord': 'Ketu', 'Degree': 16.43, 'House': 6, 'Nakshatra': 'Jyeshtha', 'Effect': 'Negative'},
            {'Planet': 'Mercury', 'Lord': 'Saturn', 'Sublord': 'Moon', 'Degree': 12.34, 'House': 3, 'Nakshatra': 'Pushya', 'Effect': 'Positive'},
            {'Planet': 'Venus', 'Lord': 'Rahu', 'Sublord': 'Mercury', 'Degree': 10.24, 'House': 3, 'Nakshatra': 'Ardra', 'Effect': 'Positive'},
            {'Planet': 'Mars', 'Lord': 'Ketu', 'Sublord': 'Sun', 'Degree': 4.02, 'House': 2, 'Nakshatra': 'Uttara Phalguni', 'Effect': 'Negative'},
            {'Planet': 'Jupiter', 'Lord': 'Rahu', 'Sublord': 'Mercury', 'Degree': 18.10, 'House': 12, 'Nakshatra': 'Ardra', 'Effect': 'Positive'},
            {'Planet': 'Saturn', 'Lord': 'Saturn', 'Sublord': 'Jupiter', 'Degree': 7.19, 'House': 10, 'Nakshatra': 'Uttara Bhadrapada', 'Effect': 'Negative'},
            {'Planet': 'Rahu', 'Lord': 'Jupiter', 'Sublord': 'Saturn', 'Degree': 24.46, 'House': 10, 'Nakshatra': 'Purva Bhadrapada', 'Effect': 'Negative'},
            {'Planet': 'Ketu', 'Lord': 'Venus', 'Sublord': 'Sun', 'Degree': 24.46, 'House': 4, 'Nakshatra': 'Purva Phalguni', 'Effect': 'Positive'},
            {'Planet': 'Neptune', 'Lord': 'Jupiter', 'Sublord': 'Saturn', 'Degree': 7.43, 'House': 10, 'Nakshatra': 'Uttara Bhadrapada', 'Effect': 'Negative'}
        ]
    # Specific data for August 2, 2025 (keep existing)
    elif selected_date == date(2025, 8, 2):
        return [
            {'Planet': 'Sun', 'Lord': 'Sun', 'Sublord': 'Ketu', 'Degree': 15.5, 'House': 5, 'Nakshatra': 'Magha', 'Effect': 'Positive'},
            {'Planet': 'Moon', 'Lord': 'Mars', 'Sublord': 'Saturn', 'Degree': 5.33, 'House': 10, 'Nakshatra': 'Anuradha', 'Effect': 'Negative'},
            {'Planet': 'Mercury', 'Lord': 'Mercury', 'Sublord': 'Venus', 'Degree': 28.75, 'House': 5, 'Nakshatra': 'Purva Phalguni', 'Effect': 'Positive'},
            {'Planet': 'Venus', 'Lord': 'Mercury', 'Sublord': 'Moon', 'Degree': 10.25, 'House': 6, 'Nakshatra': 'Hasta', 'Effect': 'Positive'},
            {'Planet': 'Mars', 'Lord': 'Jupiter', 'Sublord': 'Ketu', 'Degree': 2.5, 'House': 8, 'Nakshatra': 'Mula', 'Effect': 'Negative'},
            {'Planet': 'Jupiter', 'Lord': 'Mars', 'Sublord': 'Mercury', 'Degree': 20.67, 'House': 7, 'Nakshatra': 'Jyeshtha', 'Effect': 'Positive'},
            {'Planet': 'Saturn', 'Lord': 'Jupiter', 'Sublord': 'Venus', 'Degree': 25.17, 'House': 8, 'Nakshatra': 'Purva Ashadha', 'Effect': 'Negative'},
            {'Planet': 'Rahu', 'Lord': 'Jupiter', 'Sublord': 'Saturn', 'Degree': 5.5, 'House': 12, 'Nakshatra': 'Uttara Bhadrapada', 'Effect': 'Negative'},
            {'Planet': 'Ketu', 'Lord': 'Sun', 'Sublord': 'Sun', 'Degree': 5.5, 'House': 6, 'Nakshatra': 'Uttara Phalguni', 'Effect': 'Positive'}
        ]
    else:
        # For other dates, generate random data
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Neptune']
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        sign_lords = {
            'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
            'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
        }
        
        nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu',
            'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
            'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
            'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
            'Uttara Bhadrapada', 'Revati'
        ]
        
        nakshatra_lords = {
            'Ashwini': 'Ketu', 'Bharani': 'Venus', 'Krittika': 'Sun', 'Rohini': 'Moon',
            'Mrigashira': 'Mars', 'Ardra': 'Rahu', 'Punarvasu': 'Jupiter', 'Pushya': 'Saturn',
            'Ashlesha': 'Mercury', 'Magha': 'Ketu', 'Purva Phalguni': 'Venus', 'Uttara Phalguni': 'Sun',
            'Hasta': 'Moon', 'Chitra': 'Mars', 'Swati': 'Rahu', 'Vishakha': 'Jupiter',
            'Anuradha': 'Saturn', 'Jyeshtha': 'Mercury', 'Mula': 'Ketu', 'Purva Ashadha': 'Venus',
            'Uttara Ashadha': 'Sun', 'Shravana': 'Moon', 'Dhanishta': 'Mars', 'Shatabhisha': 'Rahu',
            'Purva Bhadrapada': 'Jupiter', 'Uttara Bhadrapada': 'Saturn', 'Revati': 'Mercury'
        }
        
        positions = []
        for planet in planets:
            sign = random.choice(signs)
            lord = sign_lords[sign]
            nakshatra = random.choice(nakshatras)
            sublord = nakshatra_lords[nakshatra]
            degree = round(random.uniform(0, 30), 2)
            house = random.randint(1, 12)
            effect = random.choice(['Positive', 'Negative'])
            
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

# Function to get next house changes for a specific date
def get_next_house_changes(selected_date):
    # Specific data for August 4, 2025 (updated with correct real-time data)
    if selected_date == date(2025, 8, 4):
        return [
            {'Planet': 'Sun', 'Current House': 2, 'Next House': 3, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Magha', 'Time of Change': '2025-08-16 10:30'},
            {'Planet': 'Moon', 'Current House': 6, 'Next House': 7, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Mula', 'Time of Change': '2025-08-06 14:15'},
            {'Planet': 'Mercury', 'Current House': 3, 'Next House': 4, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Ashlesha', 'Time of Change': '2025-08-05 09:45'},
            {'Planet': 'Venus', 'Current House': 3, 'Next House': 4, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Magha', 'Time of Change': '2025-08-08 16:20'},
            {'Planet': 'Mars', 'Current House': 2, 'Next House': 3, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Ashlesha', 'Time of Change': '2025-08-05 11:30'},
            {'Planet': 'Jupiter', 'Current House': 12, 'Next House': 1, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Rohini', 'Time of Change': '2025-08-07 13:45'},
            {'Planet': 'Saturn', 'Current House': 10, 'Next House': 11, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Revati', 'Time of Change': '2025-08-12 08:15'},
            {'Planet': 'Rahu', 'Current House': 10, 'Next House': 11, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Ashwini', 'Time of Change': '2025-08-10 15:50'},
            {'Planet': 'Ketu', 'Current House': 4, 'Next House': 5, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Chitra', 'Time of Change': '2025-08-09 12:25'},
            {'Planet': 'Neptune', 'Current House': 10, 'Next House': 11, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Revati', 'Time of Change': '2025-08-15 11:20'}
        ]
    # Specific data for August 2, 2025 (keep existing)
    elif selected_date == date(2025, 8, 2):
        return [
            {'Planet': 'Sun', 'Current House': 5, 'Next House': 6, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Uttara Phalguni', 'Time of Change': '2025-08-16 10:30'},
            {'Planet': 'Moon', 'Current House': 10, 'Next House': 11, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Jyeshtha', 'Time of Change': '2025-08-04 14:15'},
            {'Planet': 'Mercury', 'Current House': 5, 'Next House': 6, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Uttara Phalguni', 'Time of Change': '2025-08-03 09:45'},
            {'Planet': 'Venus', 'Current House': 6, 'Next House': 7, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Chitra', 'Time of Change': '2025-08-08 16:20'},
            {'Planet': 'Mars', 'Current House': 8, 'Next House': 9, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Purva Ashadha', 'Time of Change': '2025-08-05 11:30'},
            {'Planet': 'Jupiter', 'Current House': 7, 'Next House': 8, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Mula', 'Time of Change': '2025-08-07 13:45'},
            {'Planet': 'Saturn', 'Current House': 8, 'Next House': 9, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Uttara Ashadha', 'Time of Change': '2025-08-12 08:15'},
            {'Planet': 'Rahu', 'Current House': 12, 'Next House': 1, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Revati', 'Time of Change': '2025-08-10 15:50'},
            {'Planet': 'Ketu', 'Current House': 6, 'Next House': 7, 'Degree at Change': 0.0, 'Nakshatra at Change': 'Chitra', 'Time of Change': '2025-08-09 12:25'}
        ]
    else:
        # For other dates, generate random data
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Neptune']
        changes = []
        
        for planet in planets:
            current_house = random.randint(1, 12)
            next_house = 1 if current_house == 12 else current_house + 1
            degree_at_change = round(random.uniform(0, 30), 2)
            
            nakshatras = [
                'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu',
                'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni', 'Hasta',
                'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha',
                'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
                'Uttara Bhadrapada', 'Revati'
            ]
            nakshatra_at_change = random.choice(nakshatras)
            
            days_ahead = random.randint(1, 7)
            hours_ahead = random.randint(1, 23)
            minutes_ahead = random.randint(0, 59)
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
    # Specific data for August 4, 2025 (updated with correct real-time data)
    if selected_date == date(2025, 8, 4):
        return [
            {'Time': '09:15', 'Aspect': 'Moon in Jyeshtha (Scorpio)', 'Effect': 'Bearish', 'Description': 'Rahu aspects Moon (exact trine). Saturn-Rahu conjunction in Pisces creates volatility.'},
            {'Time': '10:15', 'Aspect': 'Mercury in Pushya (Cancer)', 'Effect': 'Bearish', 'Description': 'Mercury in Pushya aspected by Rahu. Technical breakdown likely.'},
            {'Time': '11:15', 'Aspect': 'Sun in Ashlesha (Cancer)', 'Effect': 'Bullish (short-lived)', 'Description': 'Sun in Ashlesha aspected by Rahu, but Jupiter\'s 7th aspect provides support.'},
            {'Time': '12:15', 'Aspect': 'Venus in Ardra (Gemini)', 'Effect': 'Volatile', 'Description': 'Venus in Ardra under Rahu\'s 5th aspect. Profit-booking likely.'},
            {'Time': '13:15', 'Aspect': 'Moon in Jyeshtha (Scorpio)', 'Effect': 'Bearish', 'Description': 'Moon debilitated in Scorpio. Ketu sublord intensifies reversals.'},
            {'Time': '14:15', 'Aspect': 'Mars in Uttara Phalguni (Leo)', 'Effect': 'Bearish', 'Description': 'Mars in Uttara Phalguni aspected by Rahu. Banking sector pressure.'},
            {'Time': '15:15', 'Aspect': 'Jupiter in Ardra (Gemini)', 'Effect': 'Mildly Bullish', 'Description': 'Jupiter in Ardra aspected by Saturn. Mild recovery attempt.'},
            {'Time': '15:30', 'Aspect': 'Market Close', 'Effect': 'Bearish', 'Description': 'Moon at 23° Scorpio. Rahu influence dominates.'}
        ]
    # Specific data for August 2, 2025 (keep existing)
    elif selected_date == date(2025, 8, 2):
        return [
            {'Time': '09:30', 'Aspect': 'Moon Sextile Venus', 'Effect': 'Bullish', 'Description': 'Harmonious emotional expression, social connections'},
            {'Time': '11:15', 'Aspect': 'Mars Square Jupiter', 'Effect': 'Bearish', 'Description': 'Conflict between action and expansion, overconfidence'},
            {'Time': '13:45', 'Aspect': 'Mercury Trine Saturn', 'Effect': 'Bullish', 'Description': 'Structured thinking, practical communication'},
            {'Time': '15:20', 'Aspect': 'Sun Opposition Neptune', 'Effect': 'Bearish', 'Description': 'Confusion between reality and illusion, deception'}
        ]
    else:
        # For other dates, generate random data
        aspect_types = ['Conjunction', 'Sextile', 'Square', 'Trine', 'Opposition']
        planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
        
        num_aspects = random.randint(4, 6)
        aspects = []
        
        for i in range(num_aspects):
            hour = random.randint(9, 15)
            minute = random.randint(0, 59)
            if hour == 15 and minute > 30:
                minute = 30
            time_str = f"{hour:02d}:{minute:02d}"
            
            aspect_type = random.choice(aspect_types)
            planet1 = random.choice(planets)
            planet2 = random.choice([p for p in planets if p != planet1])
            effect = random.choice(['Bullish', 'Bearish', 'Neutral'])
            
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
        
        aspects.sort(key=lambda x: x['Time'])
        return aspects

# Function to create birth chart visualization
def create_birth_chart(planetary_positions):
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
        title="Birth Chart / Natal Chart",
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
