import pgeocode

import brazilcep

from geopy.geocoders import Nominatim
"""
test = pgeocode.Nominatim('US')

print((test.query_postal_code('02116')))

result_br_cep = brazilcep.get_address_from_cep('06325130')

print(result_br_cep)
geolocator = Nominatim(user_agent="tests")
location = geolocator.geocode("200 Stuart Street MA")
print(location)
"""
result_br_cep = brazilcep.get_address_from_cep('06325130')
"""
address_string = "{}, {}, {}".format(street, district, uf)
geolocator = Nominatim(user_agent="uber_project")
result = geolocator.geocode(address_string)
longitude = result.longitude
latitude = result.latitude
"""
print(result_br_cep)

address_string = "{}, {}, {}".format("Avenida Perimetral Sudoeste", "Conjunto Habitacional Presidente Castelo Branco", "SP")
geolocator = Nominatim(user_agent="uber_project")
result = geolocator.geocode(address_string)
print(result.longitude)
