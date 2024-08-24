import arcpy
import pandas as pd
import os

class CsvToMapCheckPoints:
    def __init__(self, csv_file_path, output_gdb, output_feature_class, locator_path):
        self.csv_file_path = csv_file_path
        self.output_gdb = output_gdb
        self.output_feature_class = output_feature_class
        self.locator_path = locator_path

    def prepare_environment(self):
        # Ensure the directory for the output geodatabase exists
        output_folder = os.path.dirname(self.output_gdb)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Ensure the output geodatabase exists
        if not arcpy.Exists(self.output_gdb):
            arcpy.management.CreateFileGDB(output_folder, os.path.basename(self.output_gdb))

    def read_csv(self):
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(self.csv_file_path)
        return df

    def geocode_addresses(self, df):
        try:
            # Create a temporary CSV file for the geocoding process
            temp_csv = os.path.join(os.path.dirname(self.csv_file_path), "temp_geocode.csv")
            df.to_csv(temp_csv, index=False)
            
            # Output feature class for geocoded results
            geocoded_fc = os.path.join(self.output_gdb, "GeocodedPoints")
            
            # Check if the output feature class already exists and delete it
            if arcpy.Exists(geocoded_fc):
                arcpy.management.Delete(geocoded_fc)
            
            # Define address locator fields mapping (adjust as per your locator requirements)
            address_fields = "Address Address VISIBLE NONE"
            
            # Perform geocoding using the locator
            arcpy.geocoding.GeocodeAddresses(
                in_table=temp_csv,
                address_locator=self.locator_path,
                in_address_fields=address_fields,
                out_feature_class=geocoded_fc
            )
            
            return geocoded_fc

        except arcpy.ExecuteError:
            print(f"Geocoding failed: {arcpy.GetMessages(2)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def create_point_feature_class(self, df):
        try:
            # Save the DataFrame to a new CSV file for ArcPy to process
            filtered_csv = self.csv_file_path.replace(".csv", "_filtered.csv")
            df.to_csv(filtered_csv, index=False)

            # Define the spatial reference
            spatial_ref = arcpy.SpatialReference(4326)  # WGS 1984

            # Create the point feature class from the CSV
            arcpy.management.XYTableToPoint(
                filtered_csv,
                os.path.join(self.output_gdb, self.output_feature_class),
                "Longitude",  # Adjust column names as necessary
                "Latitude",
                coordinate_system=spatial_ref
            )

        except arcpy.ExecuteError:
            print(f"Creating point feature class failed: {arcpy.GetMessages(2)}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def calculate_agol_credits(self, num_records):
        # Calculate the total credits needed for geocoding
        total_credits = num_records * 0.04
        return total_credits

    def execute(self):
        self.prepare_environment()
        df = self.read_csv()
        
        if 'Longitude' in df.columns and 'Latitude' in df.columns:
            self.create_point_feature_class(df)
        else:
            geocoded_fc = self.geocode_addresses(df)
            if geocoded_fc:
                num_records = int(arcpy.management.GetCount(geocoded_fc).getOutput(0))
                total_credits = self.calculate_agol_credits(num_records)
                print(f"Total AGOL credits required for geocoding: {total_credits}")

# Example usage
if __name__ == "__main__":
    locator_path = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer"  # ArcGIS Online service URL
    
    csv_to_map = CsvToMapCheckPoints(
        csv_file_path=r"C:\Users\Ifeanyi\PythonProgramFiles\python_exercises\2_plot_into_points_exercise\data\summary_incident_reports_by_places.csv",
        output_gdb=r"K:\CS\COMPUTER_TECHNOLOGY\GIS\Ifeanyi\MyProject\MyProject.gdb",
        output_feature_class="PointsFeatureClass",
        locator_path=locator_path
    )

    csv_to_map.execute()
DFdFFFF