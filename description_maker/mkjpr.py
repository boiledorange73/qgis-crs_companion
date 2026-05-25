#
# JPR
#
jpr_areas = {
  "en": [
    "Nagasaki, Kagoshima (western remote islands)",
    "Fukuoka, Saga, Kumamoto, Oita, Miyazaki, Kagoshima (excluding Series 1)",
    "Yamaguchi, Shimane, Hiroshima",
    "Kagawa, Ehime, Tokushima, Kochi",
    "Hyogo, Tottori, Okayama",
    "Kyoto, Osaka, Fukui, Shiga, Mie, Nara, Wakayama",
    "Ishikawa, Toyama, Gifu, Aichi",
    "Niigata, Nagano, Yamanashi, Shizuoka",
    "Tokyo (excluding Series 14, 18, and 19), Fukushima, Tochigi, Ibaraki, Saitama, Chiba, Gunma, Kanagawa",
    "Aomori, Akita, Yamagata, Iwate, Miyagi",
    "Hokkaido (western part)",
    "Hokkaido (excluding Series 11 and 13)",
    "Hokkaido (eastern part)",
    "Tokyo (Ogasawara Islands)",
    "Okinawa (excluding Series 16 and 17)",
    "Okinawa (western part)",
    "Okinawa (Daito Islands)",
    "Tokyo (Okinotorishima Island)",
    "Tokyo (Minamitorishima Island)",
  ],
  "ja": [
    "長崎県 鹿児島県（奄美群島、甑島列島等の西方離島部）",
    "福岡県 佐賀県 熊本県 大分県 宮崎県 鹿児島県 (1系以外)",
    "山口県 島根県 広島県",
    "香川県 愛媛県 徳島県 高知県",
    "兵庫県 鳥取県 岡山県",
    "京都府 大阪府 福井県 滋賀県 三重県 奈良県 和歌山県",
    "石川県 富山県 岐阜県 愛知県",
    "新潟県 長野県 山梨県 静岡県",
    "東京都（14系, 18系, 19系以外）福島県 栃木県 茨城県 埼玉県 千葉県 群馬県 神奈川県",
    "青森県 秋田県 山形県 岩手県 宮城県",
    "北海道（西部）",
    "北海道（11系, 13系以外）",
    "北海道（東部）",
    "東京都（小笠原諸島）",
    "沖縄県（16系, 17系以外）",
    "沖縄県（西部）",
    "沖縄県（大東諸島）",
    "東京都（沖ノ鳥島）",
    "東京都（南鳥島）",
  ]
}

jpr_codes = {
  "Tokyo Datum": 30161,
  "JGD2000": 2443,
  "JGD2011": 6669
}

for datum in ("Tokyo Datum", "JGD2000", "JGD2011"):
  for n in range(0,19):
    syscode = n + 1
    epsgcode = "EPSG:%d" % (jpr_codes[datum] - 1 + syscode)
    en_name = "%s Japan Plane Rectangular %d" % (datum, syscode)
    ja_name = "%s 平面直角座標系 %d系" % (datum, syscode)
    en_desc = "Japan Plane Rectangular System based on %s (System %d).\\n\\nCovered Areas:\\n\\n  %s" % (datum, syscode, (jpr_areas["en"])[n])
    ja_desc = "%s を基にした平面直角座標系(%d系)です。\\n\\n該当地域（概要）:\\n  %s" % (datum, syscode, (jpr_areas["ja"])[n])
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
""" % ( epsgcode, "null", en_name, ja_name, en_desc, ja_desc)
    print(dat)

