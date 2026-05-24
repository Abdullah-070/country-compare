# Country Compare

A CLI tool that fetches and compares country data from the [REST Countries API](https://restcountries.com).

## Features

- Fetch data for multiple countries in one command
- Display side-by-side comparison table with key metrics
- Graceful error handling (invalid countries, timeouts, bad input)
- No API key required

## How to Run

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup on Fresh Machine

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abdullah-070/country-compare.git
   cd country-compare
   ```

2. **Create and activate virtual environment** (optional but recommended)
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests
   ```

### Run the Tool

```bash
python main.py "Pakistan,Japan,Brazil"
```

**Input format:** Comma-separated country names (spaces are trimmed automatically)

**Example outputs:**

```bash
# Multiple countries
python main.py "France,Germany,India"

# Handle invalid countries gracefully
python main.py "Pakistan,InvalidCountryXYZ,Japan"

# With whitespace
python main.py "United States, United Kingdom , Canada"
```

## Data Displayed

- **Country:** Official common name
- **Capital:** Capital city/cities
- **Population:** Population (comma-formatted)
- **Region:** Geographic region
- **Currency:** Currency code(s)
- **Languages:** Languages spoken (language names)

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Country not found | Shows `[NOT FOUND]` message, continues with other countries |
| API timeout (>5s) | Shows `[TIMEOUT]` message, continues with other countries |
| Empty/bad input | Displays usage hint and exits cleanly |
| Network error | Treats as not found, continues processing |

## No Configuration Needed

The REST Countries API is free and requires no API key or configuration. The tool works out of the box.
