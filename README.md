# Real State Property Analyzer

A lightweight Python tool that estimates the market price of a property by finding similar properties from a local dataset.

The application takes basic property characteristics and an address, converts the address into geographic coordinates using OpenStreetMap Nominatim, finds nearby comparable properties, ranks them by similarity, and calculates an estimated market price based on their €/m².

> **Note:** This project uses synthetic/mock property data. The result is an estimate based on comparable listings and is **not an official property valuation or professional appraisal**.

## Features

* Interactive command-line interface
* Address-to-coordinate geocoding using OpenStreetMap Nominatim
* Property comparison based on:

  * Geographic distance
  * Property size
  * Number of bedrooms
  * Number of bathrooms
  * Property type
* Haversine distance calculation
* Comparable-property similarity scoring
* Estimated price per square meter
* Estimated property price
* Estimated price range
* Display of the 10 most similar properties

## How It Works

The program follows this process:

```text
User enters property information
            ↓
Address is geocoded
            ↓
Latitude + longitude obtained
            ↓
CSV property dataset loaded
            ↓
Properties within 2 km selected
            ↓
Properties filtered by type and size
            ↓
Similarity score calculated
            ↓
Top 10 comparable properties selected
            ↓
Median €/m² calculated
            ↓
Estimated property price calculated
```

## Similarity Calculation

Each comparable property receives a similarity score based on four factors:

| Factor              | Weight |
| ------------------- | -----: |
| Size similarity     |    35% |
| Geographic distance |    30% |
| Bedroom similarity  |    20% |
| Bathroom similarity |    15% |

The final score is calculated as:

```text
Similarity =
    Size Score × 0.35
  + Bedroom Score × 0.20
  + Bathroom Score × 0.15
  + Distance Score × 0.30
```

The 10 highest-scoring properties are used for the final estimate.

## Price Estimation

For every property in the dataset, the application calculates:

```text
Price per m² = Property Price / Property Size
```

The estimated market €/m² is the **median €/m² of the top comparable properties**.

The estimated property value is then:

```text
Estimated Price =
Estimated €/m² × Target Property Size
```

The application also calculates an estimated range using the 25th and 75th percentiles of the comparable properties' €/m².

## Dataset

The current project uses:

```text
data/barcelona_properties_mock.csv
```

The dataset contains synthetic Barcelona property listings with information such as:

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

The data is intended for development and demonstration purposes and should not be interpreted as real market data.

## Requirements

Python 3.9+ is recommended.

Install the required packages:

```bash
pip install pandas requests
```

Or create a `requirements.txt` file containing:

```text
pandas
requests
```

Then install:

```bash
pip install -r requirements.txt
```

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

## Running the Application

From the project directory:

```bash
python main.py
```

The program will ask for:

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
Property type: apartment
Size (m²): 85
Bedrooms: 3
Bathrooms: 2
Address: Carrer de Mallorca 200
```

The address is combined with the neighborhood and city and sent to the OpenStreetMap Nominatim geocoding service.

## Geocoding

The application uses **OpenStreetMap Nominatim** to convert the supplied address into latitude and longitude.

The coordinates are then used to calculate the distance between the target property and every property in the dataset.

The project identifies nearby properties using the Haversine formula, which calculates the approximate distance between two points on Earth's surface.

A maximum radius of **2 km** is currently used.

## Example Output

```text
==========================================================
                        RESULTS
==========================================================

Property:
  85 m² | 3 bedrooms | 2 bathrooms
  Eixample, Barcelona

Estimated market price:
  €450,000

Estimated price per m²:
  €5,294/m²

Estimated price range:
  €430,000 - €470,000

Comparable properties used:
  10
```

The application then displays the comparable properties and their:

* Size
* Bedrooms
* Bathrooms
* Price
* €/m²
* Distance from the target
* Similarity score

### Running the Example

```bash
python main.py

## Limitations

This is a simplified comparable-property estimator.

It does not currently account for many factors that can significantly affect property prices, such as:

* Exact street/location quality
* Views
* Terrace or balcony
* Parking
* Elevator
* Building age
* Renovation quality
* Energy efficiency
* Natural light
* Historical market trends
* Actual transaction prices versus asking prices

The dataset is also synthetic, so the estimates should not be used for real purchasing, selling, financing, taxation, or professional valuation decisions.

###Example Output

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

## Future Improvements

Possible next steps include:

1. Replace the mock CSV with a regularly updated and legally obtained property dataset.
2. Improve the comparable-property algorithm.
3. Add additional property characteristics.
4. Add an interactive map.
5. Build a Streamlit web interface.
6. Add historical market-price analysis.
7. Compare different neighborhoods.
8. Experiment with machine-learning price prediction.
9. Add an AI-generated explanation of the estimate.

## Disclaimer

This project is an educational software project designed to demonstrate data analysis, geospatial calculations, and comparable-property estimation.

The output is an **estimated market price**, not an official valuation, appraisal, or professional *tasación*.

The current dataset consists of synthetic data and should not be treated as real Barcelona property-market information.
