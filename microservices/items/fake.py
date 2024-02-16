import mysql.connector
import datetime
import random


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def generate_datetime(start_date):
    random_days = random.randint(1, 30)
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    new_date = start_date + \
        datetime.timedelta(
            days=random_days, hours=random_hours, minutes=random_minutes)
    return new_date


start_date = datetime.datetime.now()
auction_deadline_dates = []
auction_start_dates = []
for _ in range(40):
    auction_start = generate_datetime(start_date)
    auction_duration = datetime.timedelta(days=random.randint(1, 7))
    auction_deadline = auction_start + auction_duration
    auction_start_dates.append(auction_start.strftime(
        '%Y-%m-%d %H:%M:%S'))
    auction_deadline_dates.append(
        auction_deadline.strftime('%Y-%m-%d %H:%M:%S'))
# Hardcoded data for each field
user_ids = [
    'user123', 'user456', 'user789', 'user101', 'user102', 'user103', 'user104', 'user105', 'user106', 'user107',
    'user108', 'user109', 'user110', 'user111', 'user112', 'user113', 'user114', 'user115', 'user116', 'user117',
    'user118', 'user119', 'user120', 'user121', 'user122', 'user123', 'user124', 'user125', 'user126', 'user127',
    'user128', 'user129', 'user130', 'user131', 'user132', 'user133', 'user134', 'user135', 'user136', 'user137'
]

item_names = [
    'Vintage Timepiece', 'Elegant Chronograph', 'Diver’s Watch', 'Pilot’s Watch', 'Classic Dress Watch', 'Modern Smartwatch', 'Limited Edition Model', 'Sports Watch', 'Luxury Gold Watch', 'Sapphire Crystal Watch',
    'Antique Pocket Watch', 'Navigator’s Watch', 'Military Grade Watch', 'Designer Women’s Watch', 'Solar Powered Watch', 'Titanium Watch', 'Automatic Watch', 'Handcrafted Watch', 'World Time Watch', 'Racing Chronograph',
    'Adventure Explorer Watch', 'Oceanic Depth Watch', 'Mountaineer’s Watch', 'Urban Style Watch', 'Retro Classic Watch', 'Futuristic Tech Watch', 'Minimalist Watch', 'Professional Pilot Watch', 'Artisan Crafted Watch', 'High Precision Chronometer',
    'Tactical Field Watch', 'Eco-Friendly Watch', 'Aviation Inspired Watch', 'Luxury Dress Watch', 'Ultra-Thin Watch', 'Heavy-Duty Diver Watch', 'Digital Sports Watch', 'Casual Everyday Watch', 'Sophisticated Dress Watch', 'Anniversary Edition Watch'
]

descriptions = [
    'A beautifully crafted vintage watch with a leather strap.',
    'An elegant and sophisticated chronograph with a stainless steel case.',
    'Water-resistant diver’s watch with a durable rubber strap.',
    'High-precision pilot’s watch with multiple time zones.',
    'A timeless dress watch with a minimalist design.',
    'Feature-rich smartwatch with health tracking capabilities.',
    'A rare and collectible watch model, only 100 made worldwide.',
    'Durable sports watch with a stopwatch and countdown timer.',
    '18K gold watch with diamond encrusted bezel.',
    'Scratch-resistant watch with sapphire crystal glass.',
    'An 18th-century pocket watch with intricate engravings.',
    'Specialized navigator’s watch with compass functionality.',
    'Rugged military watch with night vision and GPS tracking.',
    'Fashionable designer watch with a sleek, modern look.',
    'Eco-friendly solar-powered watch with long battery life.',
    'Lightweight titanium watch, resistant to corrosion.',
    'Self-winding automatic watch with a transparent back.',
    'Handcrafted watch with custom engraving options.',
    'Watch with world time feature for international travel.',
    'High-performance chronograph designed for racing enthusiasts.',
    'Elegant timepiece with a moon phase complication.',
    'Robust field watch with an ultra-durable casing.',
    'Luxurious tourbillon watch showcasing fine craftsmanship.',
    'Sleek urban design with a cutting-edge OLED display.',
    'Vintage-inspired watch with a mechanical movement.',
    'Contemporary minimalist watch with a clean, uncluttered dial.',
    'Exquisite dress watch with a unique art deco design.',
    'Innovative hybrid watch combining analog and digital features.',
    'Professional-grade dive watch with depth sensor technology.',
    'Classic pilot watch with a historic aviation heritage.',
    'Sophisticated watch with a perpetual calendar function.',
    'High-tech fitness watch with advanced activity tracking.',
    'Chic and stylish watch perfect for fashion-forward individuals.',
    'Durable and rugged, ideal for outdoor adventures.',
    'Ultra-modern smartwatch with voice command features.',
    'Limited edition luxury watch with exclusive design elements.',
    'Versatile unisex watch suitable for all occasions.',
    'Premium quality watch with a signature brand design.',
    'Functional and practical, perfect for everyday wear.',
    'Artistically designed watch with a unique, contemporary look.'
]

watch_reference_numbers = [
    'WAT1010', 'WAT2020', 'WAT3030', 'WAT4040', 'WAT5050', 'WAT6060', 'WAT7070', 'WAT8080', 'WAT9090',
    'WAT1001', 'WAT1102', 'WAT1203', 'WAT1304', 'WAT1405', 'WAT1506', 'WAT1607', 'WAT1708', 'WAT1809', 'WAT1910', 'WAT2011',
    'WAT2112', 'WAT2213', 'WAT2314', 'WAT2415', 'WAT2516', 'WAT2617', 'WAT2718', 'WAT2819', 'WAT2920', 'WAT3021',
    'WAT3122', 'WAT3223', 'WAT3324', 'WAT3425', 'WAT3526', 'WAT3627', 'WAT3728', 'WAT3829', 'WAT3930', 'WAT4031'
]

watch_models = [
    'Rolex Submariner', 'Omega Seamaster', 'Tag Heuer Carrera', 'Patek Philippe Nautilus', 'Audemars Piguet Royal Oak', 'Breitling Navitimer', 'Cartier Santos', 'IWC Portuguese', 'Panerai Luminor', 'Bulgari Octo',
    'Seiko Presage', 'Longines Heritage', 'Tudor Black Bay', 'Hublot Big Bang', 'Zenith El Primero', 'Vacheron Constantin Overseas', 'Jaeger-LeCoultre Reverso', 'Chopard Mille Miglia', 'Piaget Altiplano', 'Girard-Perregaux Laureato',
    'Rolex Daytona', 'Rolex Oyster Perpetual', 'Rolex GMT-Master II', 'Rolex Datejust', 'Rolex Explorer', 'Rolex Milgauss', 'Rolex Yacht-Master', 'Rolex Sky-Dweller', 'Rolex Air-King', 'Rolex Sea-Dweller',
    'Omega Speedmaster', 'Omega Constellation', 'Omega De Ville', 'Omega Aqua Terra', 'Omega Railmaster', 'Omega Globemaster', 'Omega Moonwatch', 'Omega Planet Ocean', 'Omega Flightmaster', 'Omega Dynamic Chronograph'
]

watch_years = [
    1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020, 1955,
    1965, 1975, 1985, 1995, 2005, 2015, 2021, 1958, 1968, 1978, 1988,
    1945, 1952, 1962, 1972, 1982, 1992, 2002, 2012, 2022, 1953,
    1963, 1973, 1983, 1993, 2003, 2013, 2023, 1954, 1964, 1974
]

brands = [
    'Rolex', 'Omega', 'Tag Heuer', 'Patek Philippe', 'Audemars Piguet', 'Breitling', 'Cartier', 'IWC', 'Panerai', 'Bulgari',
    'Seiko', 'Longines', 'Tudor', 'Hublot', 'Zenith', 'Vacheron Constantin', 'Jaeger-LeCoultre', 'Chopard', 'Piaget', 'Girard-Perregaux',
    'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex', 'Rolex',
    'Omega', 'Omega', 'Omega', 'Omega', 'Omega', 'Omega', 'Omega', 'Omega', 'Omega', 'Omega'
]

auction_won = [
    0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1
]

item_condition = [
    'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new',
    'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used',
    'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new', 'new',
    'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used', 'used',
]

bid_amounts = [
    5000,
    10000,
    15000,
    20000,
    25000,
    30000,
    35000,
    40000,
    45000,
    50000,
    55000,
    60000,
    65000,
    70000,
    75000,
    80000,
    85000,
    90000,
    95000,
    100000,
    5000,
    10000,
    15000,
    20000,
    25000,
    30000,
    35000,
    40000,
    45000,
    50000,
    55000,
    60000,
    65000,
    70000,
    75000,
    80000,
    85000,
    90000,
    95000,
    100000
]

starting_bid_amounts = [
    500,
    1000,
    1500,
    2000,
    2500,
    3000,
    3500,
    4000,
    4500,
    5000,
    5500,
    6000,
    6500,
    7000,
    7500,
    8000,
    8500,
    9000,
    9500,
    10000,
    500,
    1000,
    1500,
    2000,
    2500,
    3000,
    3500,
    4000,
    4500,
    5000,
    5500,
    6000,
    6500,
    7000,
    7500,
    8000,
    8500,
    9000,
    9500,
    10000
]

watch_images = ['./microservices/items/fake-watch-images/watch.jpg']

# add item_condition
# add starting_price
# add current bid amount

conn = mysql.connector.connect(
    host="localhost",
    port=6001,
    user="user",
    password="password",
    database="mysql"
)

cursor = conn.cursor()
random_image = [random.randint(1, 3) for _ in range(40)]
for i in range(40):
    query = """
    INSERT INTO items (user_id, item_name, description, watch_reference_number, watch_model, watch_year, brand, item_image, auction_won, bid_amount, starting_price, item_condition, auction_start, auction_deadline)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (user_ids[i], item_names[i], descriptions[i], watch_reference_numbers[i],
              watch_models[i], watch_years[i], brands[i], convertToBinaryData(
                  f'./microservices/items/watch-images/watch{random_image[i]}.jpg'), auction_won[i],
              bid_amounts[i], starting_bid_amounts[i], item_condition[i], auction_start_dates[i], auction_deadline_dates[i])

    cursor.execute(query, values)
item_ids = list(range(1, 11))
random_prices = [random.randint(10000, 100000) for _ in range(10)]
for i in range(10):
    query = """
    INSERT INTO purchases (user_id, item_id, status, purchase_date, purchase_amount)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (2, item_ids[i], "in-cart",
              auction_start_dates[i], random_prices[i])
    cursor.execute(query, values)
conn.commit()
cursor.close()
conn.close()

print(f"Inserted 40 records into the items database.")
print(f"Inserted 10 records into the user_purchases database.")
