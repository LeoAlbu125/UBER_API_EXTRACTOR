from utils import address



test = address(zip_code="06325-130",country="br")



test.get_info_by_zip()

print(test.position_dict)

