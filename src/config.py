{
 # How many seconds to sleep before scraping the same query again.
 'SCRAPE_SLEEP': 6*3600,

 # For how long the producer should wait after it finished work before
 # checking if more work is available.
 # If there's no work available, time delay will double until it hits
 # maximum limit - PRODUCE_SLEEP_MAX seconds.
 # The delay resets to PRODUCE_SLEEP_MIN seconds each time there's work
 # to be done, or each time the query changes.
 'PRODUCE_SLEEP_MIN': 10,
 'PRODUCE_SLEEP_MAX': 600,

 # Bandwidth usage limit in bytes/second.
 'BW_LIMIT': 100000,
}
