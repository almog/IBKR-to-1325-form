from typing import Dict, List
import pandas as pd
import csv

def parse_statement(csv_path: str) -> Dict[str, pd.DataFrame]:
    dataframes_by_schema_name: Dict[str, pd.DataFrame] = {}
    current_schema_col_names: List[str] = None
    current_schema_name: str = None
    current_csv_section_data: List[List[str]] = []

    with open(csv_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for current_row in reader:
            # Construct a new section
            if current_schema_col_names is None or current_row[0] != current_schema_name:
                if current_schema_col_names is not None:
                    df = pd.DataFrame(current_csv_section_data[1:], columns=current_schema_col_names)
                    df = df.apply(pd.to_numeric, errors='ignore') # Cast to number (float) when possible
                    dataframes_by_schema_name[current_schema_name] = df
                # Start a new CSV section
                current_schema_col_names = current_row
                current_schema_name = current_row[0]
                current_csv_section_data = [current_row]
            else:
                current_csv_section_data.append(current_row)

        # Add the last CSV section
        df = pd.DataFrame(current_csv_section_data[1:], columns=current_schema_col_names)
        df = df.apply(pd.to_numeric, errors='ignore')
        dataframes_by_schema_name[current_schema_name] = df

    return dataframes_by_schema_name

