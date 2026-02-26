class Flat:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

                
# class Flat:
#     id: int
#     uuid: str
#     url: str
#     room: int
#     square: int
#     city: str
#     lat: float
#     lon: float
#     description: str
#     photo: str
#     price: int
#     star: int | None = None
#     focus: int | None = None

#     floor: int | None = None
#     ceiling_height: int | None = None
#     building_type: str | None = None
#     furniture: bool | None = None
#     phone: str | None = None
#     internet: str | None = None
#     bathroom: str | None = None
#     balcony: str | None = None
#     parking: str | None = None
#     flooring: str | None = None
#     security: str | None = None
#     former_hostel: bool | None = None