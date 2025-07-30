#  TradeIndia Product & Company Scraper

This project scrapes aluminum extrusion product listings from **[TradeIndia](https://www.tradeindia.com)** and extracts additional details such as company name, city/state, full address, and GST number.

---

##  Features

- Scrapes product names and URLs from multiple pages
- Visits individual product pages to extract:
  - Company Name
  - City and State
  - Full Address
  - GST Number (validated via regex)
- Saves the scraped data into a clean CSV file

---

## Technologies Used

- Python 3
- `requests`
- `BeautifulSoup` (bs4)
- `pandas`
- `re` (Regex)

---

## Installation

1. **Clone the repository** (or copy the script files):
   ```bash
   git clone https://github.com/yourusername/tradeindia-scraper.git
   cd tradeindia-scraper
