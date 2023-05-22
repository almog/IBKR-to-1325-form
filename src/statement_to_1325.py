import pandas as pd

from columns import ColumnNames as Cols

EMPTY_CELL = ''

def statement_to_1325_form(df_statement, rate_csv_path):
    df_rate = pd.read_csv(rate_csv_path)
    date_to_rate = pd.Series(df_rate.RATE.values, index=df_rate.DATE).to_dict()

    df_statement = df_statement[df_statement['DataDiscriminator'].isin(['Trade', 'ClosedLot'])].reset_index(drop=True)

    df_statement["Date"] = pd.to_datetime(df_statement["Date/Time"]).dt.date
    df_statement['Quantity'] = df_statement['Quantity'].astype(float)

    result = []

    for index, row in df_statement.iterrows():
        if row['DataDiscriminator'] == 'Trade':
            is_short_sale = row['Basis'] > 0
            asset_symbol = row['Symbol']
            commission_fee = row['Comm/Fee']
            commission_deducted = False

            if is_short_sale:
                buy_price_per_unit = row['T. Price']
                buy_date = row['Date']
                buy_day_usd_ils = date_to_rate.get(str(buy_date))
            else:
                sell_price_per_unit = row['T. Price']
                sell_date = row['Date']
                sell_day_usd_ils = date_to_rate.get(str(sell_date))

            closedlot_start_index = df_statement[(df_statement['DataDiscriminator'] == 'ClosedLot') & (df_statement.index > index)].index.min()

            if pd.isnull(closedlot_start_index):
                raise ValueError(f"No 'ClosedLot' found after 'Trade' at index {index}")

            for i in range(closedlot_start_index, len(df_statement)):
                if df_statement.loc[i, 'DataDiscriminator'] == 'ClosedLot':

                    closed_lot = df_statement.loc[i]
                    quantity = closed_lot['Quantity']

                    if is_short_sale:
                        sell_date = closed_lot['Date']
                        sell_day_usd_ils = date_to_rate[str(sell_date)]
                        buy_price_usd = abs(quantity) * buy_price_per_unit
                        sell_price_usd = abs(closed_lot['Basis'])

                        if not commission_deducted:
                            sell_price_usd += commission_fee
                            commission_deducted = True
                    else:
                        buy_date = closed_lot['Date']
                        buy_day_usd_ils = date_to_rate[str(buy_date)]
                        sell_price_usd = quantity * sell_price_per_unit # Calculate sell price for non-short sale
                        buy_price_usd = closed_lot['Basis']

                        if not commission_deducted:
                            sell_price_usd += commission_fee
                            commission_deducted = True

                    buy_price_ils = buy_price_usd * buy_day_usd_ils

                    index_gain = sell_day_usd_ils / buy_day_usd_ils
                    adjusted_buy_price = buy_price_ils * index_gain
                    sell_price_ils = sell_price_usd * sell_day_usd_ils

                    is_profit = sell_price_usd - buy_price_usd > 0
                    real_profit_ils = max(min(sell_price_ils - adjusted_buy_price, sell_price_ils - buy_price_ils), 0) if is_profit else 0
                    real_loss_ils = 0 if is_profit else min(max(sell_price_ils - adjusted_buy_price, sell_price_ils - buy_price_ils), 0)
                    result.append([
                        real_loss_ils,
                        real_profit_ils,
                        sell_price_ils,
                        sell_date,
                        adjusted_buy_price,
                        index_gain,
                        sell_day_usd_ils,
                        buy_day_usd_ils,
                        buy_price_ils,
                        buy_price_usd,
                        buy_date,
                        sell_price_usd,
                        EMPTY_CELL,
                        asset_symbol
                    ])
                else:
                    break


    result_df = pd.DataFrame(result, columns=[col.value for col in Cols])
    result_df[Cols.SELL_DATE.value] = pd.to_datetime(result_df[Cols.SELL_DATE.value])  # Convert 'Sell date' column to datetime type
    result_df = result_df.sort_values(Cols.SELL_DATE.value)

    return result_df
