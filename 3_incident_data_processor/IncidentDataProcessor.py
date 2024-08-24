import pandas as pd

class IncidentDataProcessor:
    def __init__(self, suburb_file_path, incident_file_path, original_geocoded_file_path):
        self.suburb_file_path = suburb_file_path
        self.incident_file_path = incident_file_path
        self.original_geocoded_file_path = original_geocoded_file_path
        self.suburb_data = None
        self.incident_data = None
        self.merged_data = None

    def load_data(self):
        self.suburb_data = pd.read_csv(self.suburb_file_path)
        self.incident_data = pd.read_csv(self.incident_file_path)
        print("Data loaded successfully.")

    def process_suburb_data(self):
        self.suburb_data['Formatted_Location'] = self.suburb_data['Suburb'].str.upper().str.strip()
        print("Suburb data processed successfully.")

    def process_incident_data(self):
        self.incident_data['Formatted_Location'] = self.incident_data['Location'].str.upper().str.strip()
        print("Incident data processed successfully.")

    def create_join(self):
        self.merged_data = pd.merge(self.incident_data, self.suburb_data, on='Formatted_Location', how='left')
        print("One-to-many join created successfully.")

    def compare_records(self):
        merged_record_count = self.merged_data.shape[0]
        original_geocoded_data = pd.read_csv(self.original_geocoded_file_path)
        original_record_count = original_geocoded_data.shape[0]
        
        print(f"Number of records after join: {merged_record_count}")
        print(f"Number of records in original geocoded dataset: {original_record_count}")
        
        if merged_record_count == original_record_count:
            print("The number of records matches the original geocoded dataset.")
        else:
            print(f"There is a difference of {merged_record_count - original_record_count} records.")

    def save_processed_data(self, output_suburb_path, output_merged_path):
        self.suburb_data.to_csv(output_suburb_path, index=False)
        self.merged_data.to_csv(output_merged_path, index=False)
        print("Processed data saved successfully.")

# Example usage
if __name__ == "__main__":
    # Initialize the processor with file paths
    processor = IncidentDataProcessor(
        'path_to_suburb_data.csv', 
        'path_to_incident_data.csv', 
        'path_to_original_geocoded_data.csv'
    )
    
    # Run the processing steps
    processor.load_data()
    processor.process_suburb_data()
    processor.process_incident_data()
    processor.create_join()
    processor.compare_records()
    
    # Save the processed data
    processor.save_processed_data('processed_suburb_data.csv', 'merged_incidents_suburbs.csv')
