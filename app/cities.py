# Major Nigerian cities with their state — used for the /cities endpoint
NIGERIAN_CITIES = {
    "lagos": "Lagos",
    "abuja": "FCT",
    "kano": "Kano",
    "ibadan": "Oyo",
    "port-harcourt": "Rivers",
    "benin-city": "Edo",
    "kaduna": "Kaduna",
    "enugu": "Enugu",
    "aba": "Abia",
    "jos": "Plateau",
    "ilorin": "Kwara",
    "maiduguri": "Borno",
    "port harcourt": "Rivers",
}


def is_supported_city(city: str) -> bool:
    return city.lower().strip() in NIGERIAN_CITIES


def normalize_city(city: str) -> str:
    return city.lower().strip()