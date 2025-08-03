import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np

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
    plt.figure(figsize=(15, 10))
    
    # Plot Bullish/Bearish indicators
    plt.plot(df['Date'], df['Bullish'], 'g-', label='Bullish', linewidth=2)
    plt.plot(df['Date'], df['Bearish'], 'r-', label='Bearish', linewidth=2)
    
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
    
    for i, phase in enumerate(df['Moon Phase']):
        if phase in moon_phase_colors:
            plt.scatter(df['Date'][i], 0.5, color=moon_phase_colors[phase], s=100, alpha=0.7)
    
    # Plot selected planetary events
    planet_colors = {
        'Mercury Retro': 'purple',
        'Jupiter Trine Saturn': 'blue',
        'Mars Square Pluto': 'red',
        'Venus Sextile Jupiter': 'green'
    }
    
    for planet in planets_to_show:
        if planet in df.columns:
            for i, event in enumerate(df[planet]):
                if event:
                    plt.scatter(df['Date'][i], 0.8, color=planet_colors.get(planet, 'black'), 
                               marker='*', s=200, alpha=0.8, label=planet)
    
    # Format plot
    plt.title('Astrological Events & Market Sentiment - August 2025', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Market Sentiment', fontsize=12)
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.gcf().autofmt_xdate()
    
    # Create legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper left')
    
    plt.tight_layout()
    plt.show()

def generate_report(planets_to_show):
    print("="*80)
    print(f"ASTROLOGICAL MARKET ANALYSIS - AUGUST 2025")
    print("="*80)
    print(f"Selected Planetary Events: {', '.join(planets_to_show)}")
    print("\nKEY EVENTS:")
    
    for i, row in df.iterrows():
        date_str = row['Date'].strftime('%Y-%m-%d')
        moon_phase = row['Moon Phase']
        moon_transit = row['Moon Transit']
        bullish = row['Bullish']
        bearish = row['Bearish']
        
        print(f"\nDate: {date_str}")
        print(f"  Moon Phase: {moon_phase} (Transit: {moon_transit})")
        print(f"  Market Sentiment: Bullish {bullish:.1%} | Bearish {bearish:.1%}")
        
        for planet in planets_to_show:
            if planet in df.columns and row[planet]:
                print(f"  • {planet}: ACTIVE")
    
    print("\nMOON PHASE IMPACT:")
    print("  New Moon: Bullish for new positions, growth stocks")
    print("  Full Moon: Bearish, profit-taking, increased volatility")
    print("  Waxing Phases: Gradually building bullish energy")
    print("  Waning Phases: Gradually building bearish energy")
    
    print("\nPLANETARY INFLUENCES:")
    print("  Mercury Retrograde: Communication issues, tech volatility")
    print("  Jupiter Trine Saturn: Growth with structure, bullish")
    print("  Mars Square Pluto: Power struggles, institutional conflicts, bearish")
    print("  Venus Sextile Jupiter: Positive social mood, consumer spending, bullish")

# Example usage
if __name__ == "__main__":
    # Select which planetary events to display
    selected_planets = ['Mercury Retro', 'Jupiter Trine Saturn', 'Mars Square Pluto']
    
    # Generate report
    generate_report(selected_planets)
    
    # Plot events
    plot_astro_events(selected_planets)
