# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class RealtyspidersItem(scrapy.Item):
    BuildType = scrapy.Field(default='N/A')
    BuilderName = scrapy.Field(default='N/A')
    State = scrapy.Field(default='N/A')
    Region = scrapy.Field(default='N/A')
    DesignName = scrapy.Field(default='N/A')
    BuildFinishRange = scrapy.Field(default='N/A')
    BasePrice = scrapy.Field(default='N/A')
    Squares = scrapy.Field(default='N/A')
    HouseWidth = scrapy.Field(default='N/A')
    HouseLength = scrapy.Field(default='N/A')
    Lot_BlockWidth = scrapy.Field(default='N/A')
    LandSize = scrapy.Field(default='N/A')
    SturturalWarranty = scrapy.Field(default='N/A')
    EnergyRating = scrapy.Field(default='N/A')
    Storey = scrapy.Field(default='N/A')
    Bedrooms = scrapy.Field(default='N/A')
    Bathrooms = scrapy.Field(default='N/A')
    Garage = scrapy.Field(default='N/A')
    LivingArea = scrapy.Field(default='N/A')
    TheatreRoom_Yes_No = scrapy.Field(default='N/A')
    SeparateMeals_Yes_No = scrapy.Field(default='N/A')
    Alfresco_Yes_No = scrapy.Field(default='N/A')
    Study_Yes_No = scrapy.Field(default='N/A')
    WalkinPantry_Yes_No = scrapy.Field(default='N/A')
    BultersPantry_Yes_No = scrapy.Field(default='N/A')
    Void_Yes_No = scrapy.Field(default='N/A')
    His_HerWIR_Yes_No = scrapy.Field(default='N/A')
    BedroomGrFloor_Yes_No = scrapy.Field(default='N/A')
    SteelStructure_Yes_No = scrapy.Field(default='N/A')
    Balcony_Yes_No = scrapy.Field(default='N/A')
    LoungeDimension = scrapy.Field(default='N/A')
    FamilyDimension = scrapy.Field(default='N/A')
    Meals_DiningDimension = scrapy.Field(default='N/A')
    TheatreDimension = scrapy.Field(default='N/A')
    KitchenDimension = scrapy.Field(default='N/A')
    StudyDimension = scrapy.Field(default='N/A')
    AlfrescoDimension = scrapy.Field(default='N/A')
    GarageDimension = scrapy.Field(default='N/A')
    MasterBedroomDimension = scrapy.Field(default='N/A')
    Bedroom2Dimension = scrapy.Field(default='N/A')
    Bedroom3Dimension = scrapy.Field(default='N/A')
    Bedroom4Dimension = scrapy.Field(default='N/A')
    KitchenAppliance = scrapy.Field(default='N/A')
    KitchenAppliance1 = scrapy.Field(default='N/A')
    KitchenAppliance2 = scrapy.Field(default='N/A')
    KitchenAppliance3 = scrapy.Field(default='N/A')
    ApplianceBrand = scrapy.Field(default='N/A')
    KitchenBenchtop = scrapy.Field(default='N/A')
    Splashback = scrapy.Field(default='N/A')
    Windows = scrapy.Field(default='N/A')
    FloorCovering = scrapy.Field(default='N/A')
    FloorCovering1 = scrapy.Field(default='N/A')
    FloorCovering2 = scrapy.Field(default='N/A')
    Cooling = scrapy.Field(default='N/A')
    CeilingHeight = scrapy.Field(default='N/A')
    Bath = scrapy.Field(default='N/A')
    EnsuiteWallTiling = scrapy.Field(default='N/A')
    EnsuiteBenchtop = scrapy.Field(default='N/A')
    EnsuiteShowerbase = scrapy.Field(default='N/A')
    WallPaint = scrapy.Field(default='N/A')
    WIRFitouts = scrapy.Field(default='N/A')
    SecuritySystem = scrapy.Field(default='N/A')
    Downlights = scrapy.Field(default='N/A')
    Landscaping = scrapy.Field(default='N/A')
    Driveway = scrapy.Field(default='N/A')
    Promotion = scrapy.Field(default='N/A')
    OtherInclusions = scrapy.Field(default='N/A')
    OtherInclusions1 = scrapy.Field(default='N/A')
    OtherInclusions2 = scrapy.Field(default='N/A')
    OtherInclusions3 = scrapy.Field(default='N/A')
    OtherInclusions4 = scrapy.Field(default='N/A')
    OtherInclusions5 = scrapy.Field(default='N/A')
    BuilderEmailAddress = scrapy.Field(default='N/A')
    DisplayLocation = scrapy.Field(default='N/A')
    Lot_BlockAddress = scrapy.Field(default='N/A')
    HomeDesignMainImage = scrapy.Field(default='N/A')
    FloorPlanImage1 = scrapy.Field(default='N/A')
    FloorPlanImage2 = scrapy.Field(default='N/A')
    BrochureImage_pdf = scrapy.Field(default='N/A')
    InclusionsImage_pdf = scrapy.Field(default='N/A')
    Image1 = scrapy.Field(default='N/A')
    Image2 = scrapy.Field(default='N/A')
    Image3 = scrapy.Field(default='N/A')
    Image4 = scrapy.Field(default='N/A')
    Image5 = scrapy.Field(default='N/A')
    Image6 = scrapy.Field(default='N/A')
    Image7 = scrapy.Field(default='N/A')
    Image8 = scrapy.Field(default='N/A')
    Image9 = scrapy.Field(default='N/A')
    Image10 = scrapy.Field(default='N/A')
    Image11 = scrapy.Field(default='N/A')
    Image12 = scrapy.Field(default='N/A')
    Image13 = scrapy.Field(default='N/A')
    Image14 = scrapy.Field(default='N/A')
    Image15 = scrapy.Field(default='N/A')
    BuilderLogo = scrapy.Field(default='N/A')

    def __getitem__(self, key):
        try:
            return self._values[key]
        except KeyError:
            field = self.fields[key]
            if 'default' in field:
                return field['default']
            raise


