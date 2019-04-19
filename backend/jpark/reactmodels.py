model = Profile
    fields = ('user', 'first_name', 'last_name', 'licence_plate', 'email', 'phone', 'balance')

model = Category
    fields = ('zone_in_category_choices', 'zone_price')

model = Parking
    fields = ('owner', 'category', 'drivers', 'street_type', 'street_name', 'street_number', 'zip_code', 'province', 'city', 'image', 'phone', 'description', 'opening_time', 'closing_time', 'hourly_rate')

model = Reservation
    