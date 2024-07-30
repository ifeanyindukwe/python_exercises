import pandas as pd
from datetime import datetime, timedelta
import os
import glob

class AnalyzeData:
    def __init__(self):
        self.data_folder = 'data'

    def load_data(self):
        # Get a list of all CSV files starting with 'day_of_week_incident_reports_' in the data folder
        csv_files = glob.glob(os.path.join(self.data_folder, 'day_of_week_incident_reports_*.csv'))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files starting with 'day_of_week_incident_reports_' found in the directory: '{self.data_folder}'")
        
        # Extract the date from the filename and sort the files by date
        csv_files.sort(key=lambda x: datetime.strptime(x.split('_')[-1].replace('.csv', ''), '%d-%m-%Y'), reverse=True)
        
        # Select the latest file
        latest_file = csv_files[0]
        print(f"Reading the latest file: {latest_file}")
        
        # Read the latest CSV file into a DataFrame
        data = pd.read_csv(latest_file)
        
        # Print column names to verify
        print("Columns in CSV:", data.columns)

        # Convert the 'Date and time' column to datetime
        try:
            data['date'] = pd.to_datetime(data['Date and time'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        except Exception as e:
            print(f"Error parsing dates: {e}")

        # Drop rows where date parsing failed
        data = data.dropna(subset=['date'])
        return data

    def analyze(self, data):
        # Get the current date and the date 7 days ago
        current_date = datetime.now()
        seven_days_ago = current_date - timedelta(days=7)

        # Filter the data for the last 7 days
        last_7_days_data = data[data['date'] >= seven_days_ago]

        # a. Count the number of incidents responded to by the Stratford Brigade
        stratford_incidents = last_7_days_data[last_7_days_data['Attending Stations/Brigades'].str.contains('Stratford', case=False)]
        num_stratford_incidents = stratford_incidents.shape[0]

        # b. Count the number of Medical incidents reported in the last 7 days
        medical_incidents = last_7_days_data[last_7_days_data['Call Type'].str.contains('Medical', case=False)]
        num_medical_incidents = medical_incidents.shape[0]

        ## c. Places where Medical incidents were reported in the last 7 days (single column DataFrame)
        #places_medical_incidents_df = medical_incidents[['Attending Stations/Brigades']].drop_duplicates().reset_index(drop=True)
        ## reindex
        #places_medical_incidents_df.index += 1

        # d. Summary of Places where Medical incidents were reported in the last 7 days (two-column DataFrame)
        places_summary_df = medical_incidents['Attending Stations/Brigades'].value_counts().reset_index()
        places_summary_df.columns = ['Attending Stations/Brigades', 'Count']
        # reindex
        places_summary_df.index += 1

        # return num_stratford_incidents, num_medical_incidents, places_medical_incidents_df, places_summary_df
        return num_stratford_incidents, num_medical_incidents, places_summary_df
    

# Example usage
if __name__ == "__main__":
    analyzer = AnalyzeData()
    try:
        data = analyzer.load_data()
        # num_stratford_incidents, num_medical_incidents, places_medical_incidents_df, places_summary_df = analyzer.analyze(data)
        num_stratford_incidents, num_medical_incidents, places_summary_df = analyzer.analyze(data)
        
        print(f"Number of incidents responded to by Stratford Brigade in the last 7 days: {num_stratford_incidents}")
        print(f"Number of Medical incidents reported in the last 7 days: {num_medical_incidents}")
        # print("Places where Medical incidents were reported in the last 7 days:")
        # print(places_medical_incidents_df)
        print("Summary of Places where Medical incidents were reported in the last 7 days:")
        print(places_summary_df)
    except FileNotFoundError as e:
        print(e)
