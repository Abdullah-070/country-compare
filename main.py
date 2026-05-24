import sys
import requests
from typing import List, Dict, Optional

API_URL = "https://restcountries.com/v3.1/name/{country}"
API_TIMEOUT = 5


def validate_input(args: List[str]) -> Optional[List[str]]:
    if len(args) < 2:
        print("Usage: python main.py \"Country1,Country2,Country3\"")
        return None

    countries_str = args[1].strip()
    if not countries_str:
        print("Usage: python main.py \"Country1,Country2,Country3\"")
        return None

    countries = [c.strip() for c in countries_str.split(",")]
    return [c for c in countries if c]


def fetch_country_data(country: str) -> Dict:
    try:
        response = requests.get(
            API_URL.format(country=country), timeout=API_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if data else {"_error": "not_found"}
    except requests.Timeout:
        return {"_error": "timeout"}
    except requests.RequestException:
        return {"_error": "not_found"}


def extract_fields(country: str, data: Dict) -> Dict:
    if "_error" in data:
        return {"country": country, "_error": data["_error"]}

    try:
        currencies = data.get("currencies", {})
        currency_str = ", ".join(currencies.keys()) if currencies else "N/A"

        languages = data.get("languages", {})
        language_str = ", ".join(languages.values()) if languages else "N/A"

        return {
            "country": data["name"]["common"],
            "capital": ", ".join(data.get("capital", ["N/A"])),
            "population": f"{data.get('population', 0):,}",
            "region": data.get("region", "N/A"),
            "currency": currency_str,
            "languages": language_str,
        }
    except (KeyError, TypeError):
        return {"country": country, "_error": "parse"}


def format_table(rows: List[Dict]) -> str:
    if not rows:
        return ""

    headers = ["Country", "Capital", "Population", "Region", "Currency", "Languages"]
    header_keys = [h.lower() for h in headers]
    
    lines = [" | ".join(headers)]
    lines.append("-" * 80)
    
    for row in rows:
        if "_error" in row:
            error_line = format_error_row(row)
            lines.append(error_line)
        else:
            values = [str(row.get(key, "N/A")) for key in header_keys]
            lines.append(" | ".join(values))
    
    return "\n".join(lines)


def format_error_row(row: Dict) -> str:
    error = row["_error"]
    country = row.get("country", "Unknown")
    
    messages = {
        "timeout": "[TIMEOUT]",
        "not_found": "[NOT FOUND]",
        "parse": "[ERROR]",
    }
    prefix = messages.get(error, "[ERROR]")
    return f"{prefix} {country}"


def main():
    countries = validate_input(sys.argv)
    if not countries:
        sys.exit(1)

    rows = []
    for country in countries:
        data = fetch_country_data(country)
        row = extract_fields(country, data)
        rows.append(row)

    table = format_table(rows)
    print(table)


if __name__ == "__main__":
    main()
