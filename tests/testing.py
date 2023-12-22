import pgeocode

import brazilcep

from geopy.geocoders import Nominatim

test = pgeocode.Nominatim('US')

print((test.query_postal_code('02116')))

result_br_cep = brazilcep.get_address_from_cep('06325-130')


geolocator = Nominatim(user_agent="tests")
location = geolocator.geocode("200 Stuart Street MA")
print(location)
