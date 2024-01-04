import pgeocode
import brazilcep
from geopy.geocoders import Nominatim
import re

class address:
    """
    This class can be used to get more information out of ZIP CODES or LOCATIONS from diverse countries.
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

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.key = value

        self.zip_code = kwargs.get("zip_code", None)
        self.country = kwargs.get("country", "br")
        self.street = kwargs.get("street", None)
        self.district = kwargs.get("district", None)
        self.state = kwargs.get("state", None)
        self.position_dict = {}

    def street_formating(self,old_street):
        """
        -------
        --WIP--
        ------
        Some streets have a different name in Nominatim and BrazilCEP, this function /
        will change some words like Rua, Avenida to one another and try to run
        """
        if re.search(r'\bRua\b',old_street,flags=re.IGNORECASE):
            new_street = re.sub(r'\bRua\b','Avenida',old_street,flags=re.IGNORECASE)
        elif re.search(r'\bAvenida\b',old_street,flags=re.IGNORECASE):
            new_street = re.sub(r'\bAvenida\b','Rua',old_street,flags=re.IGNORECASE)

        self.street = new_street
        
        
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
            this case you should try other method)
        """
        if self.zip_code:
            if self.country == "br":
                location = brazilcep.get_address_from_cep(self.zip_code)
                street = location["street"]
                district = location["district"]
                uf = location["uf"]
                
                if self.street is None:
                    self.street = street
                if self.district is None:
                    self.district = district
                if self.state is None:
                    self.state = uf
                
                address_string = "{}, {}, {}".format(street, district, uf)
                geolocator = Nominatim(user_agent="uber_project")
                result = geolocator.geocode(address_string)
                if result is None:
                    if re.search(r'Rua ',street,flags=re.IGNORECASE):
                        new_street = re.sub(r'\bRua\b','Avenida',street,flags=re.IGNORECASE)
                    elif re.search(r'Avenida ',street,flags=re.IGNORECASE):
                        new_street = re.sub(r'\bAvenida\b','Rua',street,flags=re.IGNORECASE)

                    street = new_street
                    address_string = "{}, {}, {}".format(street, district, uf)
                    result = geolocator.geocode(address_string)
                longitude = result.longitude
                latitude = result.latitude

                

                position_dict = {"latitude": latitude, "longitude": longitude}
                self.position_dict = position_dict

            elif self.country == "us":
                if self.street is None:
                    raise Warning(
                        "You should provide a street or the longitude and latitude will have bad precision and will return None sometimes"
                    )

                locator = pgeocode.Nominatim(country=self.country)
                state = locator.query_postal_code(self.zip_code).state_code

                self.state = state

                geolocator = Nominatim(user_agent="uber_project")
                location = geolocator.geocode("{} {}".format(self.street, self.state))

                longitude = location.longitude
                latitude = location.latitude

                position_dict = {"latitude": latitude, "longitude": longitude}
                self.position_dict = position_dict

        else:
            raise ValueError("zip_code value was not provided")

    def get_info_by_address(self):
        """
        ---------
        ---WIP---
        ---------
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

        
        
        