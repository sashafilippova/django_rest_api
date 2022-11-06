# Court Eviction Records API

How does it work? 

Case records is continuously scraped from the Hamilton County Clerk of Courts website. 
It's getting cleaned, geocoded, and offered via REST API.

- [x] create admin site
- [x] endpoint to query all records through REST API
- [x] management command to scrape new records and insert them into db
- [x] management command to delete all records in db
- [x] management command to write records into db from a csv file
- [x] management command to update existing records missing disposition
- [x] front end page to download records
- [ ] scheduler (cron?)
- [ ] containerize with Docker
- [ ] figure out hosting
