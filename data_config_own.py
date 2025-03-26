# data config
import pandas as pd

# creating and saving metadata from a given dataset
def save_info(df, fname):
    dataset_info = pd.DataFrame(columns = ['Num', 'Data Attributes', 'Column Name', 'Data Type', 'Description'])
    dataset_info['Num'] = range(1, len(df.columns)+1)
    dataset_info['Data Attributes'] = [col.capitalize().replace('_', ' ') for col in df.columns]
    dataset_info['Column Name'] = df.columns
    dataset_info['Data Type'] = df.dtypes.values
    print(df.dtypes.values)
    data_type_map = {'int64' : 'Numeric', 'float64' : 'Numeric', 'object' : 'Text'}
    dataset_info['Data Type'] = dataset_info['Data Type'].astype(str).map(data_type_map)
    description = ['Month and Year of sale', 'Designated residential area',
            'Classification of units by room size.',
            'The Block number where the unit sold located',
            'Stree name of the unit sold located',
            'Estimated range of floors the unit sold was located on',
            'Total interior space within the unit, measured in square meters',
            'Classification of units by generation',
            'Starting point of a lease agreement (Year)',
            'Remaining amount of time left on the lease (Years and Months)',
            'Resale Price of the flat sold'
        ]
    dataset_info['Description'] = description
    dataset_info.to_csv('./data/'+fname, index=False)



df_raw = pd.read_csv('./data/SGHDB2017-2024.csv')
#print(df_raw.dtypes.values);
save_info(df_raw, fname='dataset_info.csv')


def read_resale_price_index():
    df_RPI = pd.read_csv('./data/HDBRPIMonthly.csv')
    df_RPI = df_RPI.iloc[:-3, :].copy()
    extended_date_range = pd.date_range(start='2023-01', end='2024-03', freq='MS') # Month Start
    extended_formatted_dates = extended_date_range.strftime('%Y-%m').tolist()
    rpi_data = [183.7, 180.4, 178.5, 176.2, 173.6][::-1] #24 t0 23 first quarter
    monthly_rpi_values = [value for value in rpi_data for _ in range(3)]
    df_RPI_new = pd.DataFrame({
        'month': extended_formatted_dates,
        'index': monthly_rpi_values
    })
    df_RPI_combined = pd.concat([df_RPI, df_RPI_new], ignore_index=True)
    df_RPI_combined['month'] = pd.to_datetime(df_RPI_combined['month'], format='%Y-%m')
    return df_RPI_combined


df_RPI_combined = read_resale_price_index()
print(df_RPI_combined.head())  # Check the first few rows of the result




