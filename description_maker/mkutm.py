#
# UTM
#
# 51から
utm_areas = {
  "en": [
    "Western Okinawa",
    "Okinawa (excluding the western part), Kyushu region",
    "Chugoku region, Shikoku region, Kinki region, western Chubu region",
    "Eastern Chubu region, Kanto region, Tohoku region, Hokkaido (excluding the eastern part)",
    "Eastern Hokkaido",
    "Minamitorishima"
  ],
  "ja": [
    "沖縄県西部",
    "沖縄県(西部以外)、九州地方",
    "中国地方、四国地方、近畿地方、中部地方西部",
    "中部地方東部、関東地方、東北地方、北海道(東部以外)",
    "北海道東部",
    "南鳥島"
  ]
}

utm_codes = {
  "WGS84": 32651,
  "Tokyo Datum": 3092,
  "JGD2000": 3097,
  "JGD2011": 6688
}

utm_counts = {
  "WGS84": 6,
  "Tokyo Datum": 5,
  "JGD2000": 5,
  "JGD2011": 5
}


for datum in ("WGS84", "Tokyo Datum", "JGD2000", "JGD2011"):
  image = "\"epsg_%d.png\"" % (utm_codes[datum])
  
  for n in range(0,utm_counts[datum]):
    zone = n + 51
    epsgcode = "EPSG:%d" % (utm_codes[datum] + n)
    en_name = "%s UTM Zone %d" % (datum, zone)
    ja_name = "%s UTM ゾーン %d" % (datum, zone)
    en_desc = "Universal Transverse Mercator based on %s (Zone %d).\\n\\nCovered Areas:\\n\\n  %s" % (datum, zone, (utm_areas["en"])[n])
    ja_desc = "%s を基にした UTM (Universal Transverse Mercator) ゾーン %d です。\\n\\n該当地域（概要）:\\n  %s" % (datum, zone, (utm_areas["ja"])[n])
    #
    dat = """    \"%s\": {
        \"image\": %s,
        \"name\": {
            \"en\": \"%s\",
            \"ja\": \"%s\"
        },
        \"description\": {
            \"en\": \"%s\",
            \"ja\": \"%s\"
        }
    },
""" % ( epsgcode, image, en_name, ja_name, en_desc, ja_desc)
    print(dat)

