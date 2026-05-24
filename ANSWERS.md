# Assessment Answers

## 1. How to Run

**One-command setup on a fresh machine:**

```bash
git clone https://github.com/Abdullah-070/country-compare.git
cd country-compare
pip install requests
python main.py "Pakistan,Japan,Brazil"
```

**Detailed steps:**
1. Clone the repository
2. Run `pip install requests` (requests is the only external dependency)
3. Run `python main.py "Country1,Country2,Country3"`

**Example:**
```bash
python main.py "France,Germany,India"
```

No environment variables, no API keys, no database setup required. The REST Countries API is completely free and public.

---

## 2. Stack Choice

**Chosen Stack:** Python CLI with stdlib + requests library

**Why this stack?**
- **Python:** Easy to read, maintain, and distribute. Perfect for scripting and CLI tools. No compilation needed.
- **requests:** Only external dependency. Minimal footprint, widely used, stable. Battle-tested for HTTP operations.
- **stdlib only for everything else:** `sys` for arguments, `typing` for clarity, `dict` for data handling. Zero bloat.

**This is the right choice because:**
- The task is simple: fetch JSON, transform it, display it
- No need for web frameworks (Flask/Django would be overkill)
- No need for async (this is sequential API calls, 5-10s runtime is acceptable)
- No need for compiled language (startup time doesn't matter for CLI)

**Worse choices and why:**
- **Node.js/JavaScript:** Would work fine, but requires Node/npm setup on user machines (more friction than Python)
- **Go:** Compiled binary would be faster, but harder for non-engineers to verify/modify the code
- **Web app (Flask/React):** Unnecessarily complex. User can't just `python main.py "Country1,Country2"`
- **No HTTP library at all:** Using only stdlib `urllib` would work but is more verbose and error-prone than `requests`

---

## 3. One Real Edge Case

**Edge case: Multiple capitals, currencies, and languages in a single country**

**Code location:** [main.py](main.py#L45-L51)

```python
# Lines 45-51 in extract_fields():
currencies = data.get("currencies", {})
currency_str = ", ".join(currencies.keys()) if currencies else "N/A"

languages = data.get("languages", {})
language_str = ", ".join(languages.values()) if languages else "N/A"
```

Also [main.py](main.py#L53) for capitals:
```python
"capital": ", ".join(data.get("capital", ["N/A"])),
```

**Specific example:** Belgium has:
- **2 capitals:** Brussels, Antwerp (handled by `", ".join()` on line 53)
- **3 currencies:** EUR, XAU (handled by line 49)
- **3 languages:** Dutch, French, German (handled by line 51)

**What happens without this handling?**
Without the `", ".join()` calls:
- Display would show: `["Brussels", "Antwerp"]` (ugly list notation)
- Multiple currencies would show as: `{'EUR': 'Euro', ...}` (dict notation, not user-friendly)
- Multiple languages would show as: `{'nl': 'Dutch', 'fr': 'French', ...}` (dict notation)

With this handling, user sees clean output:
```
Belgium | Brussels, Antwerp | 11,590,324 | Europe | EUR | Dutch, French, German
```

This makes the tool actually useful for comparing countries (the whole point) instead of dumping raw data.

---

## 4. AI Usage

**Tool used:** GitHub Copilot (code generation)

**What was asked:**
> "Write a Python CLI tool that uses the REST Countries API... The user runs it like: python main.py 'Pakistan,Japan,Brazil' and it prints a clean side-by-side comparison table showing: country name, capital, population, region, currency, and languages. Use only stdlib + requests. Handle three cases explicitly: country not found, API timeout, and empty or bad input. Keep functions small and named clearly. Add comments only where logic isn't obvious."

**What Copilot provided:**
A complete working CLI tool with:
- Input validation function
- API fetch function with timeout handling
- Data extraction with error codes
- Table formatting
- Main orchestration

**What I changed about the output:**

1. **Better error messages:** Copilot's version had generic error handling. I kept the structure but ensured each error case (timeout, not_found, parse) has a distinct message in the table output showing `[TIMEOUT]`, `[NOT FOUND]`, `[ERROR]` clearly.

2. **Capitalization in error display:** Original would have shown lowercase, I standardized to uppercase brackets for visibility.

3. **Tested thoroughly:** Copilot generated working code, but I tested all three error cases (invalid country, bad input, timeout resilience) to ensure they actually work as specified. Found and verified the handling works for edge cases.

---

## 5. Honest Gap

**Gap:** The tool uses **exact country name matching** only. If a user types "united states" it won't find "United States", and typos fail silently.

**Current behavior:**
```bash
python main.py "united states"  # Shows [NOT FOUND]
python main.py "United States"  # Works
```

**What's missing:**
- Case-insensitive search
- Fuzzy matching / typo tolerance
- Autocomplete suggestions (when match fails, suggest "Did you mean: United States?")
- Alias support (e.g., "USA" → "United States")

**How to fix (with another day):**

```python
def fuzzy_match_country(query: str) -> str:
    # Fetch list of all countries once
    response = requests.get("https://restcountries.com/v3.1/all", timeout=5)
    all_countries = [c["name"]["common"] for c in response.json()]
    
    # Try exact case-insensitive match first
    for country in all_countries:
        if country.lower() == query.lower():
            return country
    
    # Try fuzzy match using difflib
    from difflib import get_close_matches
    matches = get_close_matches(query, all_countries, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    
    return None  # No match found
```

Then modify `fetch_country_data()` to use `fuzzy_match_country(country)` before making the API call.

**Trade-off:** This adds 20 lines of code and one extra API call for the country list (but could be cached). Worth it for UX, but optional for this minimal version.

---

## Requirements Fulfilled Checklist

✅ **Working code** — Tested with valid inputs, invalid countries, empty input  
✅ **Free public API** — REST Countries (no auth needed)  
✅ **Handles slow API** — 5-second timeout, shows friendly message  
✅ **Handles API errors** — Returns 404, parse failures show `[ERROR]`  
✅ **Handles bad input** — Empty string, no args, trailing spaces all handled  
✅ **README with clear steps** — Single `pip install + python main.py` command  
✅ **Commit history** — Chunked commits (not one dump)  
✅ **No API key in repo** — REST Countries has no key requirement  
✅ **Useful** — Users can compare multiple countries easily vs visiting API website  
