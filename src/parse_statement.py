from typing import Dict, List
import pandas as pd
import csv

def parse_statement(csv_path: str) -> Dict[str, pd.DataFrame]:
    def commit_schema():
        df = pd.DataFrame(current_csv_section_data[1:], columns=current_schema_col_names)
        df = df.stack().str.replace(',','').unstack()
        df = df.apply(pd.to_numeric, errors='ignore') # Cast to number (float) when possible
        schema_name = current_schema_col_names[0]

        # The Commissions schema have multiple header lines for different assets categories
        if schema_name == 'Commission Details':
            asset_category = df.iloc[0][2]
            key = f'{schema_name} - {asset_category}'
        else:
            key = schema_name

        dataframes_by_schema_name[key] = df

    dataframes_by_schema_name: Dict[str, pd.DataFrame] = {}
    current_schema_col_names: List[str] = None
    current_schema_name: str = None
    current_csv_section_data: List[List[str]] = []

    with open(csv_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for current_row in reader:
            header = current_row[1]

            # Finalize the previous schema then start a new one
            if header == 'Header':
                if current_schema_col_names is not None:
                    commit_schema()

                current_schema_col_names = current_row
                current_csv_section_data = [current_row]
            elif header == 'Data':
                current_csv_section_data.append(current_row)
            elif header in ['Total', 'SubTotal']:
                pass
            else:
                raise f'Unexpected header {header}'

        # Add the last CSV section
        commit_schema()

    return dataframes_by_schema_name

