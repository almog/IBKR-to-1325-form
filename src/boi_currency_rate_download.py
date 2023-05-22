#!/usr/bin/env python3

import pandas as pd
from datetime import datetime

def fetch_currency_rates(currency: str, from_date: str, to_date: str) -> pd.DataFrame:
    boi_api_uri = f"https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_{currency}_ILS?DATA_TYPE=OF00&format=csv&startperiod={from_date}&endperiod={to_date}"

    COLUMNS_MAPPING = {"TIME_PERIOD": "DATE", "OBS_VALUE": "RATE"}
    df = pd.read_csv(boi_api_uri, usecols=["TIME_PERIOD", "OBS_VALUE"]) \
            .rename(columns={"TIME_PERIOD": "DATE", "OBS_VALUE": "RATE"})

    # Fill holidays gaps with the previous business day's rate
    df['DATE'] = pd.to_datetime(df['DATE'])
    df.set_index('DATE', inplace=True)
    df = df.asfreq('D', method='ffill').reset_index()

    return df

def download_usd_ils_for_current_tax_year():
    default_tax_year = str(datetime.now().year - 1)
    default_currency = "USD"

    tax_year = input(f"Enter the tax year (default: {default_tax_year}): ") or default_tax_year
    currency = 'USD'

    rates = fetch_currency_rates(currency, f'{tax_year}-01-01', f'{tax_year}-12-31')
    output_file = f"{currency.lower()}_ils.csv"
    rates.to_csv(output_file, index=False)
    print(f"CSV file '{output_file}' saved successfully.")

if __name__ == "__main__":
    download_usd_ils_for_current_tax_year()

