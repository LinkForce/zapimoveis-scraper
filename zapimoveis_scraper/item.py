class ZapItem:

    description = None
    price = None
    bedrooms = None
    bathrooms = None
    total_area_m2 = None
    vacancies = None
    address = None
    link = None

    def __str__(self):
        return """{
    description : "%s",
    price : %s,
    bedrooms : %s,
    bathrooms : %s,
    total_area_m2 : %s,
    vacancies : %s,
    address : "%s",
    link : "%s"
},""" % (self.description, self.price, self.bedrooms, self.bathrooms, self.total_area_m2, self.vacancies, self.address, self.link)
