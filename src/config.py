{
 # Bandwidth usage limit in bytes/second.
 'BW_LIMIT': 100000,

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

 # Skip images whose width or height is less than IMG_MIN_DIM pixels or
 # greater than IMG_MAX_DIM pixels.
 'IMG_MIN_DIM': 5,
 'IMG_MAX_DIM': 4100,

 # Convert all images to this format.
 'IMG_EXT': 'png',

 # Resize all images to this size.
 'IMG_WIDTH': 320,
 'IMG_HEIGHT': 240,

 # When resizing images of different aspect ratio than IMG_WIDTH/IMG_HEIGHT,
 # fill empty space with this color.
 'IMG_BGCOL': '#000000',
}
