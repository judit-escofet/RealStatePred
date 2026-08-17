# Barcelona Property Analyzer

A lightweight Python command-line application that estimates the market price of a property by finding similar properties from a local dataset.

The application takes basic property characteristics and an address, converts the address into geographic coordinates using OpenStreetMap Nominatim, finds nearby comparable properties, ranks them according to similarity, and estimates the property's market price based on the €/m² of the most comparable listings.

> **Disclaimer:** This project uses synthetic/mock property data. The result is an estimate based on comparable listings and is **not an official property valuation or professional appraisal**.

---

## Features

- Interactive command-line interface
- Address-to-coordinate geocoding using OpenStreetMap Nominatim
- Geographic distance calculation using latitude and longitude
- Comparable-property search within a 2 km radius
- Filtering by property type
- Filtering by similar property size
- Similarity scoring based on:
  - Property size
  - Geographic distance
  - Bedrooms
  - Bathrooms
- Top 10 comparable-property selection
- Median €/m² calculation
- Estimated property value
- Estimated price range
- Detailed comparable-property results

---

## How It Works

The application follows this process:

```text
User enters property information
            |
            v
Address is sent to Nominatim
            |
            v
Latitude + Longitude obtained
            |
            v
CSV property dataset loaded
            |
            v
Distance to every property calculated
            |
            v
Properties within 2 km selected
            |
            v
Properties filtered by type and size
            |
            v
Similarity score calculated
            |
            v
Top 10 comparable properties selected
            |
            v
Median €/m² calculated
            |
            v
Estimated property price calculated
````

---

## Similarity Algorithm

Each comparable property receives a similarity score based on four factors.

| Factor              | Weight |
| ------------------- | -----: |
| Size similarity     |    35% |
| Geographic distance |    30% |
| Bedroom similarity  |    20% |
| Bathroom similarity |    15% |

The final score is calculated as:

```text
Similarity Score =
    Size Score × 0.35
  + Distance Score × 0.30
  + Bedroom Score × 0.20
  + Bathroom Score × 0.15
```

A higher score means that the property is more similar to the user's property.

The application then selects the **10 highest-scoring properties** as the final comparable properties.

---

## Price Estimation

For every property in the dataset, the application calculates its price per square meter:

```text
Price per m² = Property Price / Property Size
```

The estimated market price per square meter is calculated using the **median €/m² of the top 10 comparable properties**.

The estimated property value is then:

```text
Estimated Price =
Estimated €/m² × Target Property Size
```

### Price Range

The application also calculates a price range using the 25th and 75th percentiles of the comparable properties' €/m².

```text
Lower Estimate =
25th Percentile €/m² × Target Property Size

Upper Estimate =
75th Percentile €/m² × Target Property Size
```

Using the median and percentiles makes the estimate less sensitive to unusually cheap or expensive individual listings.

---

## Geocoding

Instead of asking the user to provide latitude and longitude manually, the application accepts an address:

```text
Address: Carrer de Mallorca, 200, Barcelona
```

The address is combined with the neighborhood and city and sent to the **OpenStreetMap Nominatim** geocoding service.

Nominatim returns coordinates such as:

```text
Latitude: 41.xxxxx
Longitude: 2.xxxxx
```

These coordinates are then used to calculate the distance between the target property and the properties in the dataset.

---

## Geographic Distance

The application uses the **Haversine formula** to calculate the approximate distance between two points on Earth.

For example:

```text
Target property
       |
       | 0.38 km
       |
Comparable property
```

Properties closer to the target receive a higher distance score.

The current application uses a maximum search radius of:

```text
2 km
```

---

## Dataset

The application currently uses:

```text
data/barcelona_properties_mock.csv
```

The dataset contains synthetic property listings with fields including:

* ID
* City
* Neighborhood
* Price
* Size
* Bedrooms
* Bathrooms
* Property type
* Latitude
* Longitude
* Floor
* Condition

Example:

```csv
id,city,neighborhood,price,sqm,bedrooms,bathrooms,property_type,latitude,longitude
1,Barcelona,Eixample,431500,84,3,2,apartment,41.394,2.162
2,Barcelona,Eixample,453000,83,3,2,apartment,41.395,2.158
```

### Important

The dataset is **synthetic/mock data created for this project**.

It is not scraped from a real estate website and should not be interpreted as real Barcelona property-market data.

---

## Technologies

The project uses:

* **Python**
* **Pandas** — data loading, filtering, calculations, and analysis
* **Requests** — HTTP requests to the geocoding service
* **OpenStreetMap Nominatim** — address geocoding
* **Math** — geographic distance calculations
* **CSV** — property dataset storage

---

## Requirements

Python 3.9+ is recommended.

Install the dependencies:

```bash
pip install pandas requests
```

Alternatively, create a `requirements.txt` file:

```text
pandas
requests
```

Then run:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```text
barcelona-property-analyzer/
│
├── main.py
├── requirements.txt
├── README.md
│
└── data/
    └── barcelona_properties_mock.csv
```

---

## Running the Application

From the project directory, run:

```bash
python main.py
```

The application will ask for:

```text
City
Neighborhood
Property type
Size
Bedrooms
Bathrooms
Address
```

For example:

```text
City: Barcelona
Neighborhood: Eixample
Property type (apartment/penthouse/studio): apartment
Size (m²): 85
Bedrooms: 3
Bathrooms: 2
Address: Carrer de Mallorca, 200, Barcelona
```

---

# Example

The following example estimates the market price of an 85 m² apartment in Barcelona's Eixample neighborhood.

### Input

```text
City: Barcelona
Neighborhood: Eixample
Property type (apartment/penthouse/studio): apartment
Size (m²): 85
Bedrooms: 3
Bathrooms: 2
Address: Carrer de Mallorca, 200, Barcelona
```

The application geocodes the address, finds nearby comparable properties, ranks them by similarity, and calculates an estimated market price.

### Example Output

```text
   ╭──────────────────────────────────────╮
   │   🏡  Barcelona Property Analyzer     │
   │                                      │
   │        ✦ explore the local market ✦   │
   ╰──────────────────────────────────────╯

Please enter the property details below:

 City: Barcelona
 Neighborhood: Eixample
 Property type (apartment/penthouse/studio): apartment
 Size (m²): 85
 Bedrooms: 3
 Bathrooms: 2
 Address: Carrer de Mallorca, 200, Barcelona

 Looking for similar properties...


==========================================================
                        RESULTS
==========================================================

Property:
  85 m² | 3 bedrooms | 2 bathrooms
  Eixample, Barcelona

Estimated market price:
  €455,679

Estimated price per m²:
  €5,361/m²

Estimated price range:
  €442,947 - €463,736

Comparable properties used:
  10


==========================================================
                  TOP COMPARABLES
==========================================================

Property:
  84 m² | 3 bedrooms | 2 bathrooms

Price:
  €431,500

Price per m²:
  €5,137

Distance:
  0.38 km

Similarity:
  93.8%
----------------------------------------------------------


Property:
  83 m² | 3 bedrooms | 2 bathrooms

Price:
  €453,000

Price per m²:
  €5,458

Distance:
  0.55 km

Similarity:
  91.0%
----------------------------------------------------------


Property:
  89 m² | 3 bedrooms | 3 bathrooms

Price:
  €463,000

Price per m²:
  €5,202

Distance:
  0.31 km

Similarity:
  88.7%
----------------------------------------------------------


Property:
  75 m² | 3 bedrooms | 2 bathrooms

Price:
  €398,500

Price per m²:
  €5,313

Distance:
  0.63 km

Similarity:
  86.5%
----------------------------------------------------------


Property:
  93 m² | 3 bedrooms | 2 bathrooms

Price:
  €524,500

Price per m²:
  €5,640

Distance:
  0.70 km

Similarity:
  86.2%
----------------------------------------------------------


Property:
  82 m² | 3 bedrooms | 2 bathrooms

Price:
  €429,500

Price per m²:
  €5,238

Distance:
  0.84 km

Similarity:
  86.1%
----------------------------------------------------------


Property:
  75 m² | 3 bedrooms | 1 bathrooms

Price:
  €351,000

Price per m²:
  €4,680

Distance:
  0.32 km

Similarity:
  86.1%
----------------------------------------------------------


Property:
  78 m² | 3 bedrooms | 2 bathrooms

Price:
  €489,000

Price per m²:
  €6,269

Distance:
  0.76 km

Similarity:
  85.8%
----------------------------------------------------------


Property:
  82 m² | 3 bedrooms | 2 bathrooms

Price:
  €443,500

Price per m²:
  €5,409

Distance:
  0.91 km

Similarity:
  85.1%
----------------------------------------------------------


Property:
  79 m² | 2 bedrooms | 1 bathrooms

Price:
  €430,500

Price per m²:
  €5,449

Distance:
  0.17 km

Similarity:
  83.3%
----------------------------------------------------------

==========================================================
                        SUMMARY
==========================================================

Your property:

  Size:       85 m²
  Bedrooms:   3
  Bathrooms:  2

Based on the 10 most similar properties:

  Estimated value:
  €455,679

  Estimated €/m²:
  €5,361

  Estimated range:
  €442,947 - €463,736

Note: This is an estimate based on comparable property listings,
not an official valuation.
```

> **Note:** The example above uses synthetic property data and is intended only to demonstrate the application's functionality. The prices shown should not be interpreted as actual Barcelona market prices.

---

## Limitations

This is a simplified comparable-property estimator rather than a professional valuation system.

The current version does not account for many factors that can affect property prices, including:

* Exact street characteristics
* Views
* Natural light
* Balcony or terrace
* Parking
* Elevator
* Building age
* Renovation quality
* Energy efficiency
* Property orientation
* Historical price trends
* Market conditions
* Actual transaction prices
* Differences between asking prices and final sale prices

The geographic search is also relatively simple, using a fixed 2 km radius.

Most importantly, the current dataset is synthetic.

---

## Future Improvements

The project could be expanded in several directions.

### Data

* Replace the mock CSV with a regularly updated, legally obtained dataset
* Add more neighborhoods
* Add more property characteristics
* Include historical listings
* Distinguish asking prices from transaction prices

### Geospatial Analysis

* Add an interactive map
* Improve location weighting
* Consider walking distance
* Analyze proximity to public transportation
* Consider schools, parks, shops, and other amenities

### User Interface

* Build a Streamlit web application
* Add interactive filters
* Display comparable properties on a map
* Add charts showing local €/m²

### Machine Learning

A future version could compare the current similarity-based approach with a machine-learning model.

Possible models could include:

* Linear Regression
* Random Forest
* Gradient Boosting

The machine-learning model could use features such as:

```text
Size
Bedrooms
Bathrooms
Latitude
Longitude
Neighborhood
Property Type
Floor
Condition
```

The current rule-based approach is intentionally simple and explainable, making it a useful baseline before introducing machine learning.

### AI

An AI layer could eventually generate a natural-language explanation of the estimate, for example:

```text
The estimated market price is approximately €455,679.
The estimate is based on 10 comparable properties within 2 km.
Most comparable properties are similar in size and bedroom count,
with prices ranging from approximately €4,680 to €6,269 per m².
```

The AI should explain the calculated results rather than independently inventing a property valuation.

---

## Disclaimer

This project is an educational software project demonstrating:

* Data analysis
* Pandas
* Geospatial calculations
* Address geocoding
* Comparable-property analysis
* Basic statistical estimation

The output is an **estimated market price**, not an official property valuation, appraisal, *tasación*, or professional real-estate advice.

The current dataset consists of synthetic data and should not be used for actual purchasing, selling, financing, taxation, or investment decisions.

---

## Author

Built as a personal Python/data-analysis project exploring how geospatial data and comparable-property analysis can be used to create a simple real-estate valuation tool.
