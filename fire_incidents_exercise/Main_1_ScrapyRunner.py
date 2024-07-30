import subprocess
import os
from datetime import datetime
import pytz

class ScrapyRunner:
    def __init__(self, spider_name):
        # Set the time zone to New Zealand
        nz_tz = pytz.timezone('Pacific/Auckland')
        current_date = datetime.now(nz_tz).strftime('%d-%m-%Y')
        self.output_file = os.path.join('data', f'day_of_week_incident_reports_{current_date}.csv')
        self.spider_name = spider_name
        self.ensure_data_directory()

    def ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def run_spider(self):
        try:
            # Delete the output file if it exists to ensure it is overwritten
            if os.path.exists(self.output_file):
                os.remove(self.output_file)

            # Change to the correct directory and adjust the output path
            subprocess.run(['scrapy', 'crawl', self.spider_name, '-o', os.path.join('..', '..', '..', self.output_file)], 
                           check=True, cwd=os.path.join('fire_incidents', 'fire_incidents', 'spiders'))
            print("Spider executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running the spider: {e}")

# Example usage
if __name__ == "__main__":
    runner = ScrapyRunner(spider_name='incident_reports')
    runner.run_spider()
