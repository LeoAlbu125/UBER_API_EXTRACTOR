import pgeocode
import brazilcep
from geopy.geocoders import Nominatim

class address:
    """
    This class to get more information out of ZIP CODES or LOCATIONS from diverse countries.
    You have to provide a COUNTRY (br or us).
    You should provide at least a ZIP_CODE or an address (STREET, DISTRICT, STATE).
    
    ...
    
    args:
        zip_code (string): the zip could can contain especial caracters, default value /
        is None
        country (string): supported countries are Brasil (use "br") and USA (use "us")  /
        standard value is "br".
        street (string): the street of your location, example value is                 /
        "200 Stuart Street MA"
        district (string): the district of your location
        state (string): the state of your location, standard value is "MA"
        
    
    
    methods:
        get_info_by_zip: Get address details and returns a dict with longitude/latitude
    
    """
    def __init__(self,**kwargs):
        for key,value in kwargs:
            self.key = value
        
        self.zip_code = kwargs.get('zip_code', None)
        self.country = kwargs.get('country', 'br')
        self.street = kwargs.get('street', None)
        self.district = kwargs.get('district', None)
        self.state = kwargs.get('state', None)
        
    def get_info_by_zip(self):
        """
        Get info for a provided zip code, if the country is Brazil (br) it will get     / 
        address data with brazilcep, if it is USA (us) it will get address data with    /
        pgeocode (in this case street must be provided)
        
        
        raises:
            ValueError: If zip_code is not provided
        
        returns:
            Dict[Latitude:String,Longitude:String] : latitude and longitude values
            (when looking for Brazilean zip codes, sometimes it will return None, in    /
            this case you shoul try other method)
        """
        if self.zip_code:    
            if self.country == "br":
                location = brazilcep.get_address_from_cep(self.zip_code)
                street = location["street"]
                district = location["district"]
                uf = location["uf"]
                address_string = "{}, {}, {}".format(street,district,uf)
                geolocator = Nominatim(user_agent="uber_project")
                result = geolocator.geocode(address_string)
                longitude = result.longitude
                latitude = result.latitude
                
                self.street = street
                self.district = district
                self.state = uf
                
                position_dict = {"latitude":latitude,"longitude":longitude}
                
                
                
            elif self.country == "us":
                
                locator = pgeocode.Nominatim(country=self.country)
                state = locator.query_postal_code(self.zip_code).state_code
                
                self.state = state
                
                geolocator = Nominatim(user_agent="uber_project")
                location = geolocator.geocode("{} {}".format(self.street, self.state))
                
                longitude = location.longitude 
                latitude = location.latitude
                
                position_dict = {"latitude":latitude,"longitude":longitude}
                
        else:
            raise ValueError("zip_code value was not provided")
        
        return position_dict
    
    
    
    def get_info_by_address(self):
        """
        Get info for a provided address (street, district, state), if the country is Brazil (br) it will get     / 
        address data with brazilcep, if it is USA (us) it will get address data with    /
        pgeocode (in this case street must be provided)
        
        
        raises:
            ValueError: If zip_code is not provided
        
        returns:
            Dict[Latitude:String,Longitude:String] : latitude and longitude values
            (when looking for Brazilean zip codes, sometimes it will return None, in    /
            this case you shoul try other method)
        """