import scrapy

class IncidentReportsSpider(scrapy.Spider):
    name = "incident_reports"
    allowed_domains = ["fireandemergency.nz"]
    start_urls = ["https://fireandemergency.nz/incidents-and-news/incident-reports"]

    def parse(self, response):
        # Extract the entire div for the Central region
        region_central_div = response.xpath("//div[@class='incidentreport__region'][h3[text()='Central']]")
        
        if region_central_div:
            # Extract the <li> elements within the specific <ul>
            li_elements = region_central_div.xpath(".//ul[@class='incidentreport__region__list']/li/a")
            
            for li in li_elements:
                # Extract the link and the text
                day_of_week_link = li.xpath("@href").get()
                day_of_week_text = li.xpath("text()").get().strip()
                
                # Create the full URL and yield a request to follow the link
                full_url = response.urljoin(day_of_week_link)
                yield scrapy.Request(full_url, callback=self.parse_day_page, meta={'day_text': day_of_week_text})

    def parse_day_page(self, response):
        # Extract additional data from the day page
        day_of_week_text = response.meta['day_text']
        
        # Define the expected order of keys
        key_labels = ['Incident number', 'Date and time', 'Location', 'Duration', 'Attending Stations/Brigades', 'Call Type']
        
        # Extract the report data
        values = response.xpath("//div[@class='report__table__cell report__table__cell--value']/p/text()").getall()
        
        # Ensure that the number of values is a multiple of the number of keys
        assert len(values) % len(key_labels) == 0, "Mismatch between number of values and expected key labels"

        # Chunk the values into groups of length equal to the number of keys
        chunked_values = [values[i:i + len(key_labels)] for i in range(0, len(values), len(key_labels))]
        
        # Create dictionaries using zip for each chunk of values
        reports = [dict(zip(key_labels, chunk)) for chunk in chunked_values]
        
        # Yield the scraped data
        for report in reports:
            yield report
