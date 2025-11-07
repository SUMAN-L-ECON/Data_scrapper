import httpx
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time

def fetch_agmarknet_yearwise(commodity_code, state_code, start_year, end_year):
    base_url = "https://www.agmarknet.gov.in/SearchCmmMkt.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    all_data = []

    for year in range(start_year, end_year + 1):
        from_date = f"01-Jun-{year}"
        to_date = f"30-Jun-{year+1}"

        params = {
            "Tx_Commodity": commodity_code,
            "Tx_State": state_code,
            "Tx_District": 0,
            "Tx_Market": 0,
            "DateFrom": from_date,
            "DateTo": to_date,
            "Fr_Date": from_date,
            "To_Date": to_date,
            "Tx_Trend": 2,
            "Tx_CommodityHead": "Tomato",     # Adjust if needed
            "Tx_StateHead": "Haryana",        # Adjust if needed
            "Tx_DistrictHead": "--Select--",
            "Tx_MarketHead": "--Select--"
        }

        print(f"📥 Fetching data for: {from_date} to {to_date}")
        try:
            with httpx.Client(http2=False, timeout=30.0, verify=True) as client:
                response = client.get(base_url, params=params, headers=headers)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"id": "cphBody_GridViewBoth"})
            if table:
                df = pd.read_html(StringIO(str(table)))[0]
                df["Year"] = year  # Add year for reference
                all_data.append(df)
                print(f"✅ Success for {year}: {len(df)} rows")
            else:
                print(f"⚠️ No table found for {year}.")

        except Exception as e:
            print(f"❌ Error for {year}: {e}")
        
        time.sleep(2)  # Be polite to the server

    # Combine all years into a single DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    else:
        return pd.DataFrame()

# ▶️ Example usage:
df_all = fetch_agmarknet_yearwise(commodity_code=78, state_code="WB", start_year=2010, end_year=2025)
# Remove rows where 'Group' contains subtotal or total indicators
df_all = df_all[~df_all["Group"].str.contains("Sub Total|Total", na=False)]
df_all.loc[:, "Reported Date"] = pd.to_datetime(df_all["Reported Date"], format="%d %b %Y", errors="coerce")
