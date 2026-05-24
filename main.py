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

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        if "_error" not in row:
            for i, key in enumerate(header_keys):
                widths[i] = max(widths[i], len(str(row.get(key, ""))))

    # Build table
    lines = []
    header_line = " | ".join(h.ljust(w) for h, w in zip(headers, widths))
    lines.append(header_line)
    lines.append("-" * len(header_line))

    for row in rows:
        if "_error" in row:
            error = row["_error"]
            country = row.get("country", "Unknown")
            if error == "timeout":
                lines.append(f"[TIMEOUT] {country} - Request timed out")
            elif error == "not_found":
                lines.append(f"[NOT FOUND] {country} - Country not found")
            elif error == "parse":
                lines.append(f"[ERROR] {country} - Failed to parse data")
        else:
            values = [str(row.get(key, "")) for key in header_keys]
            line = " | ".join(v.ljust(w) for v, w in zip(values, widths))
            lines.append(line)

    return "\n".join(lines)


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
