# About
Scraping Finn housing/work ads with Python and requests. **Work in progress**.

Scraping different subdomains within finn *(see parameters.yml)*. E.g. housing ads, project ads,
work ads. Each different subdomain requires a different set of xpaths, though there are many common denominators *(see src/xpaths.py)*.



CSV example
![alt text](media/scrape_example.png)

Log example
![alt text](media/log_example.png)


# Setup
`mkdir scrapes`\
`mkdir logs`\
`pip install -r requirements.txt`

### Parameters
Adjust parameters in `parameters.yml`.\
**daily_scrape:** If true scraper only scrapes the daily adds.\
**finn_sub_urls:** Which part of finn to scrape. A different CSV is created for
all the different sub urls.

### To run
`python src/finn_scraper.py`


## Checklist
- [ ] Add detail to headers.
- [ ] Add sleep timer and folder etc to parameters.yml.
- [ ] Custom queries instead of binary daily/not daily scrape.
- [ ] Reduce line length across project.
- [ ] Checking if all requests yields code 200.