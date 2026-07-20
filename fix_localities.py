import pandas as pd
import numpy as np
import random
import os

# Load the original unmodified dataset if possible, or the current one.
# Since the current one already has localities replaced, we need to make sure we map the *current* unique localities 
# back to a diverse set per city.
df = pd.read_csv('predictor/india_housing_prices.csv')

city_localities = {
    'Lucknow': ['Gomti Nagar', 'Indira Nagar', 'Hazratganj', 'Alambagh', 'Ashiyana', 'Mahanagar', 'Vikas Nagar', 'Jankipuram', 'Chowk', 'Gomti Nagar Extension', 'Sushant Golf City', 'Vrindavan Yojna', 'Aminabad'],
    'Noida': ['Sector 15', 'Sector 18', 'Sector 62', 'Sector 137', 'Sector 150', 'Noida Extension', 'Greater Noida West', 'Sector 44', 'Sector 93A', 'Sector 128'],
    'New Delhi': ['Connaught Place', 'Vasant Kunj', 'Dwarka', 'Hauz Khas', 'Saket', 'Karol Bagh', 'Lajpat Nagar', 'Rohini', 'Janakpuri', 'Pitampura', 'Greater Kailash'],
    'Mumbai': ['Andheri West', 'Bandra West', 'Juhu', 'Powai', 'Goregaon East', 'Malad West', 'Borivali West', 'South Mumbai', 'Dadar', 'Worli', 'Lower Parel'],
    'Bangalore': ['Koramangala', 'Indiranagar', 'Whitefield', 'HSR Layout', 'BTM Layout', 'Jayanagar', 'JP Nagar', 'Electronic City', 'Marathahalli', 'Bellandur'],
    'Pune': ['Koregaon Park', 'Kalyani Nagar', 'Viman Nagar', 'Hinjewadi', 'Wakad', 'Baner', 'Kothrud', 'Magarpatta', 'Kharadi', 'Shivajinagar'],
    'Chennai': ['Adyar', 'Anna Nagar', 'Besant Nagar', 'T Nagar', 'Velachery', 'Mylapore', 'OMR', 'Guindy', 'Tambaram', 'Nungambakkam'],
    'Hyderabad': ['Banjara Hills', 'Jubilee Hills', 'HITEC City', 'Gachibowli', 'Kondapur', 'Madhapur', 'Kukatpally', 'Secunderabad', 'Begumpet', 'Ameerpet'],
    'Kolkata': ['Salt Lake', 'Rajarhat', 'New Town', 'Ballygunge', 'Alipore', 'Park Street', 'Jadavpur', 'Dum Dum', 'Tollygunge', 'Behala'],
    'Ahmedabad': ['Vastrapur', 'Satellite', 'Bodakdev', 'Thaltej', 'Navrangpura', 'Prahlad Nagar', 'Bopal', 'SG Highway', 'Maninagar', 'Chandkheda'],
    'Jaipur': ['Malviya Nagar', 'Vaishali Nagar', 'Mansarovar', 'C Scheme', 'Bani Park', 'Raja Park', 'Jagatpura', 'Civil Lines', 'Tonk Road', 'Ajmer Road']
}

generic_prefixes = ['New', 'Old', 'Central', 'North', 'South', 'West', 'East', 'Greater', 'Upper', 'Lower']
generic_suffixes = ['Nagar', 'Vihar', 'Enclave', 'Phase 1', 'Phase 2', 'Sector 1', 'Sector 2', 'Sector 3', 'Colony', 'Heights', 'Layout', 'Road', 'Avenue', 'Market', 'Bazar', 'Park']
generic_names = ['Gandhi', 'Shastri', 'Subhash', 'Patel', 'Nehru', 'Shivaji', 'Azad', 'Tagore', 'Bhagat', 'Ambedkar', 'Model', 'Defense', 'Railway', 'Station', 'Civil', 'Vidya', 'Sanjay', 'Kisan', 'Green', 'Diamond', 'Silver', 'Golden', 'Royal']

def generate_city_specific_pool(city_name):
    # Generates a large pool of 150+ unique looking localities for any given city
    pool = set()
    random.seed(hash(city_name))
    
    # 1. Hardcoded major localities if they exist
    if city_name in city_localities:
        for loc in city_localities[city_name]:
            pool.add(loc)
            pool.add(f"{loc} Phase 1")
            pool.add(f"{loc} Phase 2")
            pool.add(f"{loc} Extension")
            
    # 2. Sectors attached to City or Generic Name
    for i in range(1, 20):
        pool.add(f"{city_name} Sector {i}")
        pool.add(f"{random.choice(generic_names)} Nagar Sector {i}")
        
    # 3. Blocks/Phases attached to City or Generic Name
    for phase in range(1, 10):
        pool.add(f"{city_name} Phase {phase}")
        pool.add(f"{random.choice(generic_names)} Vihar Phase {phase}")
    for block in 'ABCDEF':
        pool.add(f"{city_name} Block {block}")
        pool.add(f"{random.choice(generic_names)} Enclave Block {block}")
        
    # 4. City Name + Suffix 
    for suffix in ['Central', 'North', 'South', 'West', 'East', 'Heights', 'Enclave', 'Valley', 'Town', 'City']:
        pool.add(f"{city_name} {suffix}")
    
    # 5. Generic Name + Suffix 
    while len(pool) < 250:
        pool.add(f"{random.choice(generic_names)} {random.choice(generic_suffixes)}")
        
    return list(pool)

print("Replacing mock localities with massive realistic pools...")

mapping_dict = {}

def get_mapped_loc(city, loc):
    key = city + "_" + loc
    if key not in mapping_dict:
        pool = generate_city_specific_pool(city)
        seed_val = hash(key) % (10**8)
        random.seed(seed_val)
        mapping_dict[key] = random.choice(pool)
    return mapping_dict[key]

# Since we already replaced the original Locality_XX with generic names in the previous run,
# doing it again will just map "Gandhi Nagar" to something else based on the city. 
# Which is totally fine, it will restore diversity per city!
df['Locality'] = df.apply(lambda row: get_mapped_loc(row['City'], row['Locality']), axis=1)

df.to_csv('predictor/india_housing_prices.csv', index=False)
print("Updated india_housing_prices.csv successfully!")
