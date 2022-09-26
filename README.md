# Court Eviction Records API

How does it work? 

The data is continuously scraped from the Hamilton County Clerk of Courts website. 
It's getting cleaned, geocoded, and offered via REST API.

- [x] create admin site
- [x] endpoint to query all records through REST API
- [ ] management command to scrape new records and insert them into db
- [ ] management command to update existing records missing disposition
- [ ] scheduler (cron?)
- [ ] containerize with Docker
