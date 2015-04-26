{
 # Bandwidth usage limit in bytes/second.
 'LIMIT_RATE': 100000,

 # New search results for particular query can appear over time, so it makes
 # sense to do the scraping again every once in a while.
 # When scraping is done, sleep for this number of seconds before
 # repeat scraping. If the query has changed, do scraping right away though.
 'SCRAPE_SLEEP': 6*3600,

 # It's quite time consuming to check if there are newly scraped image URLs,
 # which have not been processed yet. So it's better to wait between checks.
 # If there's no work available, the delay will double until it hits
 # maximum limit - PRODUCE_SLEEP_MAX seconds.
 # The delay resets to PRODUCE_SLEEP_MIN seconds each time there's some work
 # to be done, or each time the query changes.
 'PRODUCE_SLEEP_MIN': 10,
 'PRODUCE_SLEEP_MAX': 600,

 # Set new background picture after this time in seconds.
 # We want a slide show, don't we?
 'SHOW_SLEEP': 600,

 # If there are no images to show, check again after this time in seconds.
 # Checking for new images can be time consuming, so it's wise to do it rarely.
 'SHOW_SLEEP_NO_IMG': 60,

 # X Window DISPLAY variable to set background picture for.
 'DISPLAY': ':0',

 # There are very large and very small images on the internet.
 # We'll skip images whose width or height is less than IMG_DIM_MIN pixels or
 # greater than IMG_DIM_MAX pixels.
 'IMG_DIM_MIN': 5,
 'IMG_DIM_MAX': 4100,

 # Convert all images to this format.
 'IMG_EXT': 'png',

 # Resize all images to this size.
 'IMG_WIDTH': 320,
 'IMG_HEIGHT': 240,

 # When resizing images of different aspect ratio than IMG_WIDTH/IMG_HEIGHT,
 # fill empty space with this color.
 'IMG_BGCOL': '#000000',
}
