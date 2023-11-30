# to get satellites name and id. there is only one: iss
WHERE_IS_ISS_SATELLITES = "https://api.wheretheiss.at/v1/satellites"

# get iss details
WHERE_IS_ISS_SATELLITES_DETAILS = "https://api.wheretheiss.at/v1/satellites/{satellite_id}"

# based on latitude and longitude get where the iss is on top of
REVERSE_GEOCODING_API = 'https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={latitude}&longitude={longitude}&localityLanguage=en'

