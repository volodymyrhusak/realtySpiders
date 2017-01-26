# -*- coding: utf-8 -*-

# Scrapy settings for realtySpiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'realtySpiders'

SPIDER_MODULES = ['realtySpiders.spiders']
NEWSPIDER_MODULE = 'realtySpiders.spiders'
FEED_EXPORT_FIELDS = ['BuildType', 'BuilderName', 'State', 'Region', 'DesignName',
                      'BuildFinishRange', 'BasePrice', 'Squares', 'HouseWidth',
                      'HouseLength', 'Lot_BlockWidth', 'LandSize', 'SturturalWarranty',
                      'EnergyRating', 'Storey', 'Bedrooms', 'Bathrooms', 'Garage', 'LivingArea', 'TheatreRoom_Yes_No',
                      'SeparateMeals_Yes_No', 'Alfresco_Yes_No', 'Study_Yes_No', 'WalkinPantry_Yes_No',
                      'BultersPantry_Yes_No', 'Void_Yes_No', 'His_HerWIR_Yes_No', 'BedroomGrFloor_Yes_No',
                      'SteelStructure_Yes_No', 'Balcony_Yes_No', 'LoungeDimension', 'FamilyDimension',
                      'Meals_DiningDimension', 'TheatreDimension', 'KitchenDimension', 'StudyDimension',
                      'AlfrescoDimension', 'GarageDimension', 'MasterBedroomDimension', 'Bedroom2Dimension',
                      'Bedroom3Dimension', 'Bedroom4Dimension', 'KitchenAppliance', 'KitchenAppliance1',
                      'KitchenAppliance2', 'KitchenAppliance3', 'ApplianceBrand', 'KitchenBenchtop', 'Splashback',
                      'Windows', 'FloorCovering', 'FloorCovering1', 'FloorCovering2', 'Cooling', 'CeilingHeight',
                      'Bath', 'EnsuiteWallTiling', 'EnsuiteBenchtop', 'EnsuiteShowerbase', 'WallPaint', 'WIRFitouts',
                      'SecuritySystem', 'Downlights', 'Landscaping', 'Driveway', 'Promotion', 'OtherInclusions',
                      'OtherInclusions1', 'OtherInclusions2', 'OtherInclusions3', 'OtherInclusions4',
                      'OtherInclusions5', 'BuilderEmailAddress', 'DisplayLocation', 'Lot_BlockAddress',
                      'HomeDesignMainImage', 'FloorPlanImage1', 'FloorPlanImage2', 'BrochureImage_pdf',
                      'InclusionsImage_pdf', 'Image1', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7',
                      'Image8', 'Image9', 'Image10', 'Image11', 'Image12', 'Image13', 'Image14', 'Image15',
                      'BuilderLogo']
FEED_STORE_EMPTY = True
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'realtySpiders (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'realtySpiders.middlewares.RealtyspidersSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'realtySpiders.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'realtySpiders.pipelines.SomePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
