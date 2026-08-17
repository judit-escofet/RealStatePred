import requests
import math
import pandas as pd
import urllib.parse
import sys

print("   ╭──────────────────────────────────────╮\n   │   🏡  Barcelona Property Analyzer     │\n   │                                      │\n   │        ✦ explore the local market ✦   │\n   ╰──────────────────────────────────────╯\n")
print("Please enter the property details below:\n")
city = input(" City: ").strip()
neighborhood = input(" Neighborhood: ").strip()
property_type = input(" Property type (apartment/penthouse/studio): ").strip()
sqm = float(input(" Size (m²): "))
bedrooms = int(input("  Bedrooms: "))
bathrooms = int(input(" Bathrooms: "))
address = input(" Address: ").strip()

print("\n Looking for similar properties...\n")

# Use OpenStreetMap Nominatim for global/Barcelona address geocoding
full_address = f"{address}, {neighborhood}, {city}"
url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(full_address)}&format=json"

headers = {
    'User-Agent': 'BarcelonaPropertyAnalyzer/1.0'
}

lat = None
lon = None

try:
    response = requests.get(url, headers=headers).json()
    if response:
        lat = float(response[0]['lat'])
        lon = float(response[0]['lon'])
    else:
        print("⚠️ No geocoding matches found for the provided address.")
        sys.exit()
except Exception as e:
    print(f"⚠️ Geocoding request failed: {e}")
    sys.exit()

df = pd.read_csv("data/barcelona_properties_mock.csv")
df["price_per_sqm"] = df["price"] / df["sqm"]

def haversine(lat1, lon1, lat2, lon2):
    earth_radius = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.asin(math.sqrt(a))

    return earth_radius * c

df["distance_km"] = df.apply(
    lambda row: haversine(
        lat,
        lon,
        row["latitude"],
        row["longitude"]
    ),
    axis=1
)

comparables = df[
    df["distance_km"] <= 2
].copy()

comparables = comparables[
    comparables["property_type"].str.lower()
    == property_type.lower()
]

min_size = sqm * 0.80
max_size = sqm * 1.20

comparables = comparables[
    (comparables["sqm"] >= min_size)
    & (comparables["sqm"] <= max_size)
]

size_difference = (
    abs(comparables["sqm"] - sqm) / sqm
)

comparables["size_score"] = (
    1 - size_difference
).clip(lower=0)

comparables["bedroom_score"] = (
    1 - abs(
        comparables["bedrooms"] - bedrooms
    ) / 3
).clip(lower=0)

comparables["bathroom_score"] = (
    1 - abs(
        comparables["bathrooms"] - bathrooms
    ) / 3
).clip(lower=0)

comparables["distance_score"] = (
    1 - comparables["distance_km"] / 2
).clip(lower=0)

comparables["score"] = (
    comparables["size_score"] * 0.35
    + comparables["bedroom_score"] * 0.20
    + comparables["bathroom_score"] * 0.15
    + comparables["distance_score"] * 0.30
)

comparables = comparables.sort_values(
    by="score",
    ascending=False
)

top_comparables = comparables.head(10).copy()

if len(top_comparables) == 0:
    print("\nNo comparable properties were found.")
    print("Try increasing the search radius or changing the property characteristics.")
    sys.exit()

estimated_price_per_sqm = (
    top_comparables["price_per_sqm"].median()
)

estimated_price = (
    estimated_price_per_sqm * sqm
)

price_per_sqm_low = (
    top_comparables["price_per_sqm"]
    .quantile(0.25)
)

price_per_sqm_high = (
    top_comparables["price_per_sqm"]
    .quantile(0.75)
)

estimated_low = (
    price_per_sqm_low * sqm
)

estimated_high = (
    price_per_sqm_high * sqm
)

print("\n")
print("==========================================================")
print("                        RESULTS")
print("==========================================================")

print("\nProperty:")
print(
    f"  {sqm:.0f} m² | "
    f"{bedrooms} bedrooms | "
    f"{bathrooms} bathrooms"
)

print(f"  {neighborhood}, {city}")

print("\nEstimated market price:")
print(f"  €{estimated_price:,.0f}")

print("\nEstimated price per m²:")
print(f"  €{estimated_price_per_sqm:,.0f}/m²")

print("\nEstimated price range:")
print(
    f"  €{estimated_low:,.0f} - "
    f"€{estimated_high:,.0f}"
)

print("\nComparable properties used:")
print(f"  {len(top_comparables)}")

print("\n")
print("==========================================================")
print("                  TOP COMPARABLES")
print("==========================================================")

for _, row in top_comparables.iterrows():
    print(
        f"""
Property:
  {row['sqm']:.0f} m² | {int(row['bedrooms'])} bedrooms | {int(row['bathrooms'])} bathrooms

Price:
  €{row['price']:,.0f}

Price per m²:
  €{row['price_per_sqm']:,.0f}

Distance:
  {row['distance_km']:.2f} km

Similarity:
  {row['score'] * 100:.1f}%
----------------------------------------------------------
"""
    )

print("==========================================================")
print("                        SUMMARY")
print("==========================================================")

print(
    f"""
Your property:

  Size:       {sqm:.0f} m²
  Bedrooms:   {bedrooms}
  Bathrooms:  {bathrooms}

Based on the {len(top_comparables)} most similar properties:

  Estimated value:
  €{estimated_price:,.0f}

  Estimated €/m²:
  €{estimated_price_per_sqm:,.0f}

  Estimated range:
  €{estimated_low:,.0f} - €{estimated_high:,.0f}
"""
)

print(
    "Note: This is an estimate based on comparable "
    "property listings, not an official valuation."
)