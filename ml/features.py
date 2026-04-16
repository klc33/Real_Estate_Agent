FEATURES = [
    "LotFrontage",
    "LotArea",
    "OverallQual",
    "YearBuilt",
    "Street",
    "GrLivArea",
    "FullBath",
    "BedroomAbvGr",
    "GarageCars",
    "Neighborhood",
    "HouseStyle"
]

NUM_FEATURES = [
    "LotFrontage",
    "LotArea",
    "OverallQual",
    "YearBuilt",
    "GrLivArea",
    "FullBath",
    "BedroomAbvGr",
    "GarageCars"
]

CAT_FEATURES = [
    "Neighborhood",
    "HouseStyle",
    "Street"
]

TARGET = "SalePrice"



# Feature descriptions for documentation
FEATURE_DESCRIPTIONS = {
    "LotFrontage": "Linear feet of street connected to property",
    "LotArea": "Lot size in square feet",
    "OverallQual": "Overall material and finish quality (1-10)",
    "YearBuilt": "Original construction date",
    "Street": "Type of road access (Paved/Gravel)",
    "GrLivArea": "Above grade living area in square feet",
    "FullBath": "Full bathrooms above grade",
    "BedroomAbvGr": "Bedrooms above grade (does NOT include basement)",
    "GarageCars": "Garage capacity in number of cars",
    "Neighborhood": "Physical locations within Ames city limits",
    "HouseStyle": "Style of dwelling (1Story, 2Story, Ranch, etc.)"
}