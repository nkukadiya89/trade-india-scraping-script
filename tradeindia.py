import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# GST Format: 15 alphanumeric characters
GST_PATTERN = re.compile(r'\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}\b')

# Product Data (full merged list)
data = [
    {"Product Name": "Grey Aluminum Extrusion - Color: Silver", "Product URL": "https://www.starrail.co.in"},
    {"Product Name": "Aluminum Extrusion Sections - Premium Quality Alloy, Square Shape , Polished Surface Finish With Custom Color Options And Warranty", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-sections-c9126698.html"},
    {"Product Name": "Aluminum Extrusion Billet - Round Alloy Silver | Polished Surface Treatment, Industrial Grade", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-billet-c9114694.html"},
    {"Product Name": "Gray Aluminum Extrusions", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusions-c8665486.html"},
    {"Product Name": "Silver S40 80l Aluminum Extrusion", "Product URL": "https://www.tradeindia.com/products/s40-80l-aluminum-extrusion-c8668903.html"},
    {"Product Name": "Aluminum Extrusions - Custom Profiles For Architectural And Industrial Applications | Sleek Silver Design, Unmatched Strength And Versatility", "Product URL": "https://www.tradeindia.com/products/inconel-800-pipes-4182147.html"},
    {"Product Name": "Rectangular Aluminum Extrusion - Custom Size, Rose Gold, 5mm Thickness | High-grade, Anodized Finish, Corrosion Resistant, Industrial & Commercial Use", "Product URL": "https://www.tradeindia.com/products/rectangular-aluminum-extrusion-c9075163.html"},
    {"Product Name": "Silver 90x90 Mm Aluminium Profile", "Product URL": "https://www.tradeindia.com/products/90x90-mm-aluminium-profile-c4152383.html"},
    {"Product Name": "Aluminium Extrusion Sections - Alloy, Rectangular Shape, Silver Color | Strong Build, Highly Resistant To Corrosion And Abrasion, Dimensional Accuracy", "Product URL": "https://www.tradeindia.com/products/aluminium-extrusion-sections-c4524044.html"},
    {"Product Name": "Aluminum Extrusion Dies - Tool Steel, High Precision, Customizable Dimensions | Cost Effective, Durable Design, Easy Maintenance, Long Lifespan", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-dies-4121102.html"},
    {"Product Name": "Aluminum U Shape Channel Extrusion - 6061 Alloy, Customized Size Millimeter (Mm) | 70-90 Series Railing, 290 Mpa Strength, 1 Year Warranty", "Product URL": "https://www.tradeindia.com/products/aluminum-u-shape-channel-extrusion-7124273.html"},
    {"Product Name": "Aluminum Extrusion Housing Heatsink - Customized Size, Silver Or Black Finish | Effective Led Heat Dissipation Solution", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-housing-heatsink-led-heat-sink-c7805177.html"},
    {"Product Name": "Hindalco Aluminum Extrusions - Custom-sized Industrial Components | High-quality Aluminum, Galvanized For Corrosion Resistance, Warranty Included", "Product URL": "https://www.tradeindia.com/products/hindalco-aluminum-extrusions-c9238004.html"},
    {"Product Name": "80x80 Mm Aluminum Extrusion - Color: Silver", "Product URL": "https://www.tradeindia.com/products/80x80-mm-aluminum-extrusion-c10195202.html"},
    {"Product Name": "Aluminum Extrusion For Boat - Color: White", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-for-boat-c10241149.html"},
    {"Product Name": "Aluminum Extrusion Die Nitriding Furnace", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-die-nitriding-furnace-c5757112.html"},
    {"Product Name": "Aluminum Extrusion Billet", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-billet-c10283548.html"},
    {"Product Name": "Industrial Aluminum Extrusion Rod - Color: Silver", "Product URL": "https://www.tradeindia.com/products/industrial-aluminum-extrusion-rod-c9895583.html"},
    {"Product Name": "Aluminum Extrusion Scrap - Multiple Grades Available, Rigid Hardness & High Strength, Polished Finish, 1 Year Warranty", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-scrap-c9672996.html"},
    {"Product Name": "Aluminium Window Extrusion - Color: Silver", "Product URL": "https://www.tradeindia.com/products/aluminium-window-extrusion-c6612121.html"},
    {"Product Name": "Aluminum Profile Extrusion Section Application: For Industrial Use", "Product URL": "https://www.tradeindia.com/products/aluminum-profile-extrusion-section-c5981310.html"},
    {"Product Name": "Aluminum Profile Led Linear Light Ip65 Pc Diffuser Aluminum Extrusion Profile - Color: White", "Product URL": "https://www.tradeindia.com/products/lamp-housing-c7615665.html"},
    {"Product Name": "Aluminum Extrusion Billet - Custom Sizes, Corrosion-resistant Aluminum Grades 6101/6063, Uncoated/polished Finish, T5/t6 Temper, High Strength-to-weight Ratio", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-billet-c9201284.html"},
    {"Product Name": "Aluminum Extrusion 6063 Scrap Car Polishers Size: 5 Liter", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-6063-scrap-4389820.html"},
    {"Product Name": "Aluminum Profile Section Grade: First Class", "Product URL": "https://www.tradeindia.com/products/aluminum-profile-section-c4306239.html"},
    {"Product Name": "Industrial Ubc Aluminum Extrusion Scrap", "Product URL": "https://www.tradeindia.com/products/industrial-ubc-aluminum-extrusion-scrap-9007080.html"},
    {"Product Name": "29mm Track Cap Aluminum Extrusion - High-quality Aluminum, Various Sizes Available | Durable Bending Process, Industrial Usage, Warranty Included", "Product URL": "https://www.tradeindia.com/products/29mm-track-cap-aluminum-extrusion-c9382393.html"},
    {"Product Name": "Aluminum Extrusion Profile - Grade: Multiple Grades Available", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-profile-c10429407.html"},
    {"Product Name": "Aluminum Extrusion Section - Application: Exterior", "Product URL": "https://www.tradeindia.com/products/aluminum-extrusion-section-c5340292.html"}
]

def extract_info(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Company Name ---
        company_tag = soup.find("a", class_="seller-name-url")
        company_name = company_tag.get_text(strip=True) if company_tag else "N/A"

        # --- Full Address ---
        full_address = city = state = "N/A"
        for tag in soup.find_all("p"):
            text = tag.get_text(strip=True)
            if "India" in text and "," in text:
                full_address = text
                parts = text.split(',')
                if len(parts) >= 2:
                    city = parts[-3].strip() if len(parts) >= 3 else "N/A"
                    state = parts[-2].strip()
                break

        # --- GST Number Detection ---
        gst_number = "N/A"
        for tag in soup.find_all(['p', 'div']):
            match = GST_PATTERN.search(tag.get_text(strip=True))
            if match:
                gst_number = match.group()
                break

        return company_name, city, state, full_address, gst_number

    except Exception as e:
        print(f" Error scraping {url}: {e}")
        return "N/A", "N/A", "N/A", "N/A", "N/A"

# Scrape and save data
output_data = []
for item in data:
    print(f" Scraping: {item['Product Name']}")
    company, city, state, address, gst = extract_info(item["Product URL"])
    output_data.append({
        "Product Name": item["Product Name"],
        "Product URL": item["Product URL"],
        "Company Name": company,
        "City/State": f"{city}, {state}" if city != "N/A" and state != "N/A" else "N/A",
        "Full Address": address,
        "GST Number": gst
    })

# Save to CSV
df = pd.DataFrame(output_data)
df.to_csv("tradeindia.csv", index=False, encoding="utf-8-sig")

print(" Scraping completed. Data saved to 'scraped_product_data_with_gst.csv'")

