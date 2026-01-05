import json
from pathlib import Path

import pandas as pd
import pycountry


# Paleta farieb podľa screenshotu (Figma export)
PALETTE = {
    "peach_1": "#F3C09F",
    "peach_2": "#DC9354",
    "yellow_2": "#BF8F1C",
    "peach_3": "#AB7240",
    "peach_4": "#7C512C",
    "pink_2": "#E083AC",
    "pink_3": "#C7508A",
    "pink_4": "#903863",
    "pink_5": "#5D213F",
    "teal_2": "#69AAAF",
    "teal_3": "#508387",
    "teal_4": "#375D60",
    "teal_5": "#213B3D",
    "mint_1": "#52DCCE",
    "mint_2": "#41B1A6",
    "mint_3": "#308980",
    "mint_4": "#20625C",
    "mint_5": "#113E3A",
    "gray_2": "#A9A39F",
    "gray_3": "#837E7B",
    "gray_4": "#5E5A59",
}

GROUP_COLOR = {
    "Primárny sektor": "#DC9354",
    "Spracovateľský priemysel": "#69AAAF",
    "Utility a stavebníctvo": "#AB7240",
    "Obchod a doprava": "#E083AC",
    "Súkromné služby": "#52DCCE",
    "Financie a nehnuteľnosti": "#5E5A59",
    "Verejný sektor": "#C7508A",
}

INDUSTRY_META: dict[str, dict[str, str]] = {
    # Primárny sektor
    "A": {
        "label": "Poľnohospodárstvo a lesníctvo",
        "group": "Primárny sektor",
        "color": PALETTE["peach_1"],
    },
    "B": {
        "label": "Ťažba nerastných surovín",
        "group": "Primárny sektor",
        "color": PALETTE["peach_2"],
    },
    # Spracovateľský priemysel (tlmené modro‑zelené odtiene)
    "C10T12": {
        "label": "Výroba potravín a nápojov",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["teal_2"],
    },
    "C13T15": {
        "label": "Výroba textilu a odevov",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["teal_3"],
    },
    "C16T18": {
        "label": "Výroba dreva, papiera a tlač",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["teal_4"],
    },
    "C19T23": {
        "label": "Výroba chemikálií a plastov",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["mint_1"],
    },
    "C24_25": {
        "label": "Výroba kovov a kovových výrobkov",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["mint_2"],
    },
    "C26_27": {
        "label": "Výroba elektroniky a elektrotechniky",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["mint_3"],
    },
    "C28": {
        "label": "Výroba strojov a zariadení",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["mint_4"],
    },
    "C29_30": {
        "label": "Výroba dopravných prostriedkov",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["mint_5"],
    },
    "C31T33": {
        "label": "Ostatná priemyselná výroba",
        "group": "Spracovateľský priemysel",
        "color": PALETTE["teal_5"],
    },
    # Utility a stavebníctvo
    "D_E": {
        "label": "Energetika a verejné služby",
        "group": "Utility a stavebníctvo",
        "color": PALETTE["peach_3"],
    },
    "F": {
        "label": "Stavebníctvo",
        "group": "Utility a stavebníctvo",
        "color": PALETTE["peach_4"],
    },
    # Obchod, doprava a služby
    "G": {
        "label": "Veľkoobchod a maloobchod",
        "group": "Obchod a doprava",
        "color": PALETTE["pink_2"],
    },
    "H": {
        "label": "Doprava a skladovanie",
        "group": "Obchod a doprava",
        "color": PALETTE["pink_3"],
    },
    "I": {
        "label": "Ubytovanie a stravovanie",
        "group": "Súkromné služby",
        "color": PALETTE["pink_4"],
    },
    "J": {
        "label": "Informačné a komunikačné služby",
        "group": "Súkromné služby",
        "color": PALETTE["pink_5"],
    },
    "K": {
        "label": "Finančné služby",
        "group": "Financie a nehnuteľnosti",
        "color": PALETTE["gray_3"],
    },
    "L": {
        "label": "Služby v oblasti nehnuteľností",
        "group": "Financie a nehnuteľnosti",
        "color": PALETTE["gray_4"],
    },
    "M_N": {
        "label": "Odborné a podnikové služby",
        "group": "Súkromné služby",
        "color": PALETTE["mint_1"],
    },
    "RTT": {
        "label": "Ostatné trhové služby",
        "group": "Súkromné služby",
        "color": PALETTE["mint_2"],
    },
    # Verejný sektor
    "OTQ": {
        "label": "Verejný sektor",
        "group": "Verejný sektor",
        "color": PALETTE["peach_3"],
    },
}


# Geografické regióny krajín a fixné farby
EUROPE = {
    "AUT",
    "BEL",
    "BGR",
    "BLR",
    "CHE",
    "CYP",
    "CZE",
    "DEU",
    "DNK",
    "ESP",
    "EST",
    "FIN",
    "FRA",
    "GBR",
    "GRC",
    "HRV",
    "HUN",
    "IRL",
    "ISL",
    "ITA",
    "LTU",
    "LUX",
    "LVA",
    "MLT",
    "NLD",
    "NOR",
    "POL",
    "PRT",
    "ROU",
    "RUS",
    "SVK",
    "SVN",
    "SWE",
    "TUR",
    "UKR",
}

AMERICAS = {
    "ARG",
    "BRA",
    "CAN",
    "CHL",
    "COL",
    "CRI",
    "MEX",
    "PER",
    "USA",
}

ASIA_PACIFIC = {
    "AUS",
    "BGD",
    "BRN",
    "CHN",
    "HKG",
    "IDN",
    "IND",
    "JPN",
    "KAZ",
    "KHM",
    "KOR",
    "LAO",
    "MMR",
    "MYS",
    "NZL",
    "PAK",
    "PHL",
    "SGP",
    "THA",
    "TWN",
    "VNM",
}

AFRICA_ME = {
    "AGO",
    "ARE",
    "CIV",
    "CMR",
    "COD",
    "EGY",
    "ISR",
    "JOR",
    "MAR",
    "NGA",
    "SAU",
    "SEN",
    "STP",
    "TUN",
}


REGION_LABEL = {
    "Europe": "Európa",
    "Americas": "Amerika",
    "AsiaPacific": "Ázia a Pacifik",
    "AfricaME": "Afrika a Blízky východ",
    "Other": "Ostatné krajiny",
}

REGION_COLOR = {
    # Používame farby priamo z palety v screenshote (spodný riadok)
    "Europe": "#60A5FA",
    "Americas": "#52DCCE",
    "AsiaPacific": "#E083AC",
    "AfricaME": "#BF8F1C",
    "Other": "#837E7B",
}


def country_name_from_iso3(code: str) -> str:
    """
    Prevedie ISO3 kód krajiny na slovenský názov.
    Ak sa nenájde, vráti pôvodný kód.
    """
    if not isinstance(code, str) or not code:
        return code

    country_name_sk = {
        # Afrika a Blízky východ
        "AGO": "Angola",
        "ARE": "Spojené arabské emiráty",
        "CIV": "Pobrežie Slonoviny",
        "CMR": "Kamerun",
        "COD": "Konžská dem. republika",
        "EGY": "Egypt",
        "ISR": "Izrael",
        "JOR": "Jordánsko",
        "MAR": "Maroko",
        "NGA": "Nigéria",
        "SAU": "Saudská Arábia",
        "SEN": "Senegal",
        "STP": "Svätý Tomáš a Princov ostrov",
        "TUN": "Tunisko",
        # Európa
        "AUT": "Rakúsko",
        "BEL": "Belgicko",
        "BGR": "Bulharsko",
        "BLR": "Bielorusko",
        "CHE": "Švajčiarsko",
        "CYP": "Cyprus",
        "CZE": "Česko",
        "DEU": "Nemecko",
        "DNK": "Dánsko",
        "ESP": "Španielsko",
        "EST": "Estónsko",
        "FIN": "Fínsko",
        "FRA": "Francúzsko",
        "GBR": "Spojené kráľovstvo",
        "GRC": "Grécko",
        "HRV": "Chorvátsko",
        "HUN": "Maďarsko",
        "IRL": "Írsko",
        "ISL": "Island",
        "ITA": "Taliansko",
        "LTU": "Litva",
        "LUX": "Luxembursko",
        "LVA": "Lotyšsko",
        "MLT": "Malta",
        "NLD": "Holandsko",
        "NOR": "Nórsko",
        "POL": "Poľsko",
        "PRT": "Portugalsko",
        "ROU": "Rumunsko",
        "RUS": "Rusko",
        "SVK": "Slovensko",
        "SVN": "Slovinsko",
        "SWE": "Švédsko",
        "TUR": "Turecko",
        "UKR": "Ukrajina",
        # Amerika
        "ARG": "Argentína",
        "BRA": "Brazília",
        "CAN": "Kanada",
        "CHL": "Čile",
        "COL": "Kolumbia",
        "CRI": "Kostarika",
        "MEX": "Mexiko",
        "PER": "Peru",
        "USA": "Spojené štáty",
        # Ázia a Pacifik
        "AUS": "Austrália",
        "BGD": "Bangladéš",
        "BRN": "Brunej",
        "CHN": "Čína",
        "HKG": "Hongkong",
        "IDN": "Indonézia",
        "IND": "India",
        "JPN": "Japonsko",
        "KAZ": "Kazachstan",
        "KHM": "Kambodža",
        "KOR": "Kórejská republika",
        "LAO": "Laos",
        "MMR": "Mjanmarsko",
        "MYS": "Malajzia",
        "NZL": "Nový Zéland",
        "PAK": "Pakistan",
        "PHL": "Filipíny",
        "SGP": "Singapur",
        "THA": "Thajsko",
        "TWN": "Taiwan",
        "VNM": "Vietnam",
        # Zvyšok sveta
        "WXD": "Zvyšok sveta",
    }

    if code in country_name_sk:
        return country_name_sk[code]

    try:
        country = pycountry.countries.get(alpha_3=code)
        if country:
            return country.name
    except Exception:
        pass
    return code


def country_region(code: str) -> tuple[str, str]:
    """
    Vráti (region_key, region_label) pre ISO3 kód krajiny.
    """
    if code in EUROPE:
        return "Europe", REGION_LABEL["Europe"]
    if code in AMERICAS:
        return "Americas", REGION_LABEL["Americas"]
    if code in ASIA_PACIFIC:
        return "AsiaPacific", REGION_LABEL["AsiaPacific"]
    if code in AFRICA_ME:
        return "AfricaME", REGION_LABEL["AfricaME"]
    return "Other", REGION_LABEL["Other"]


def prepare_data(
    csv_path: str = "oecd-skva-origin.csv",
    out_path: str = "web/data.json",
) -> None:
    """
    Načíta OECD TiVA CSV, vyfiltruje rok 2022 a
    pripraví agregované dáta pre vizualizáciu v prehliadači.

    Výsledná štruktúra (JSON):
    {
      "industries": [
        {
          "code": "...",
          "label": "Potraviny a nápoje",
          "group": "Spracovateľský priemysel",
          "color": "#f472b6",
          "value": <mil. USD>
        },
        ...
      ],
      "byIndustry": {
        "_all": [
          {
            "countryCode": "DEU",
            "countryName": "Germany",
            "regionKey": "Europe",
            "regionLabel": "Európa",
            "color": "#0ea5e9",
            "value": <mil. USD>
          },
          ...
        ],
        "C10T12": [
          {
            "countryCode": "DEU",
            "countryName": "Germany",
            "regionKey": "Europe",
            "regionLabel": "Európa",
            "color": "#0ea5e9",
            "value": <mil. USD>
          },
          ...
        ],
        ...
      }
    }
    """
    df = pd.read_csv(csv_path)

    # ponecháme len rok 2022, ak je k dispozícii
    if "TIME_PERIOD" in df.columns:
        df = df[df["TIME_PERIOD"] == 2022]

    # názvy krajín podľa ISO3 kódu final demandu
    if "FINAL_DEMAND_AREA" not in df.columns:
        raise ValueError("V súbore chýba stĺpec FINAL_DEMAND_AREA.")

    df["country_name"] = df["FINAL_DEMAND_AREA"].apply(country_name_from_iso3)

    if "VALUE_ADDED_SOURCE_ACTIVITY" not in df.columns:
        raise ValueError("V súbore chýba stĺpec VALUE_ADDED_SOURCE_ACTIVITY.")

    if "OBS_VALUE" not in df.columns:
        raise ValueError("V súbore chýba stĺpec OBS_VALUE.")

    # agregácia podľa odvetví
    industries_df = (
        df.groupby("VALUE_ADDED_SOURCE_ACTIVITY", as_index=False)["OBS_VALUE"]
        .sum()
        .sort_values("OBS_VALUE", ascending=False)
    )

    industries: list[dict[str, object]] = []
    for _, row in industries_df.iterrows():
        code = row["VALUE_ADDED_SOURCE_ACTIVITY"]
        meta = INDUSTRY_META.get(
            code,
            {
                "label": code,
                "group": "Iné",
                "color": "#9ca3af",
            },
        )
        color = GROUP_COLOR.get(meta["group"], meta["color"])
        industries.append(
            {
                "code": code,
                "label": meta["label"],
                "group": meta["group"],
                "color": color,
                "value": float(row["OBS_VALUE"]),
            }
        )

    # agregácia krajín naprieč všetkými odvetviami (potrebujeme pre farby)
    grouped_all = (
        df.groupby(["FINAL_DEMAND_AREA", "country_name"], as_index=False)["OBS_VALUE"]
        .sum()
        .sort_values("OBS_VALUE", ascending=False)
    )
    # agregácia krajín pre každé odvetvie
    by_industry: dict[str, list[dict[str, object]]] = {}

    for code in industries_df["VALUE_ADDED_SOURCE_ACTIVITY"].unique():
        subset = df[df["VALUE_ADDED_SOURCE_ACTIVITY"] == code]
        grouped = (
            subset.groupby(["FINAL_DEMAND_AREA", "country_name"], as_index=False)[
                "OBS_VALUE"
            ]
            .sum()
            .sort_values("OBS_VALUE", ascending=False)
        )

        rows: list[dict[str, object]] = []
        for _, row in grouped.iterrows():
            country_code = row["FINAL_DEMAND_AREA"]
            region_key, region_label = country_region(country_code)
            rows.append(
                {
                    "countryCode": country_code,
                    "countryName": row["country_name"],
                    "regionKey": region_key,
                    "regionLabel": region_label,
                    "color": REGION_COLOR.get(region_key, REGION_COLOR["Other"]),
                    "value": float(row["OBS_VALUE"]),
                }
            )
        by_industry[code] = rows

    all_rows: list[dict[str, object]] = []
    for _, row in grouped_all.iterrows():
        country_code = row["FINAL_DEMAND_AREA"]
        region_key, region_label = country_region(country_code)
        all_rows.append(
            {
                "countryCode": country_code,
                "countryName": row["country_name"],
                "regionKey": region_key,
                "regionLabel": region_label,
                "color": REGION_COLOR.get(region_key, REGION_COLOR["Other"]),
                "value": float(row["OBS_VALUE"]),
            }
        )
    by_industry["_all"] = all_rows

    data = {
        "industries": industries,
        "byIndustry": by_industry,
    }

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    print(f"Dáta pre vizualizáciu uložené do: {out_file}")
    print(
        "Ďalší krok:\n"
        "  1) prejdite do priečinka 'web' (cd web)\n"
        "  2) spustite jednoduchý server: python -m http.server 8000\n"
        "  3) otvorte prehliadač na adrese http://localhost:8000/"
    )


if __name__ == "__main__":
    prepare_data()
