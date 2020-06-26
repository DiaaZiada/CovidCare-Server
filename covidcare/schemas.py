from covidcare import ma

class MeetingSchema(ma.Schema):
  class Meta:
    fields = ('time', 'latitude', 'longitude', 'user_1', 'user_2')