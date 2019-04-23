# Extract data from marketplace and hospitality services operating within the town

## hospitality-python

### Goal 
Create a script that can pull current listings from AirBnB and VRBO to a spreadsheet with Geo coordinates

### Purpose 
Business Analysts would like to know more about locations of short term rental units in the town.
Internal use only - experimental and not for redistribution

### Methodology 
Currently there are two scripts:
1. extract-airbnb-properties.py, which uses the unsupported API and has unpredictable results
2. extract-vrbo-properties.py, does rudimentary screen scraping.

### Data Source
AirBnB API - unsupported 
Accessed via (https://github.com/nderkach/airbnb-python)[nderkach/airbnb-python]

### Output 
Aggregated CSV file
### Transformations
TBD
### Constraints
needs refactoring if we intend to have a scheduled refresh and reliable results
manual cleanup of data required before upload
data quality is low
