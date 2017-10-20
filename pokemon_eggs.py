#!env python3

my_list = """
diglett
snorlax
dratini
totodile
pichu
togepi
mareep
scyther
larvitar
"""

rarity_denominator = 508
rarity_tiers = {
    "common": 16,
    "uncommon": 8,
    "rare": 4,
    "super-rare": 2,
    "hyper-rare": 1
}

pokemon_tiers = {
    "common": [
        "geodude",
        "krabby",
        "nidoran-f",
        "nidoran-m",
        "phanpy",
        "pichu",
        "poliwag",
        "ponyta",
    ],
    "uncommon": [
        "abra",
        "aipom",
        "chinchou",
        "cleffa",
        "cubone",
        "diglett",
        "dratini",
        "drowzee",
        "eevee",
        "elekid",
        "exeggcute",
        "gastly",
        "growlithe",
        "hoppip",
        "igglybuff",
        "larvitar",
        "machop",
        "magby",
        "mantine",
        "mareep",
        "marill",
        "natu",
        "oddish",
        "porygon",
        "rhyhorn",
        "shellder",
        "slowpoke",
        "slugma",
        "smoochum",
        "spinarak",
        "stantler",
        "swinub",
        "togepi",
        "tyrogue",
        "voltorb",
        "wooper",
    ],
    "rare": [
        "chansey",
        "chikorita",
        "cyndaquil",
        "houndour",
        "onix",
        "pinsir",
        "remoraid",
        "scyther",
        "seel",
        "skarmory",
        "snubbull",
        "sudowoodo",
        "tangela",
        "teddiursa",
        "totodile",
    ],
    "super-rare": [
        "aerodactyl",
        "gligar",
        "grimer",
        "kabuto",
        "koffing",
        "lapras",
        "lickitung",
        "miltank",
        "misdreavus",
        "omanyte",
        "pineco",
        "qwilfish",
        "sneasel",
        "snorlax",
    ],
    "hyper-rare": [
        "dunsparce",
        "girafarig",
        "shuckle",
        "wobbuffet",
    ]
}

pokemon_eggs = {
    2: [
        "abra",
        "aipom",
        "cleffa",
        "diglett",
        "exeggcute",
        "gastly",
        "geodude",
        "igglybuff",
        "krabby",
        "machop",
        "misdreavus",
        "nidoran-f",
        "nidoran-m",
        "oddish",
        "pichu",
        "remoraid",
        "slowpoke",
        "slugma",
        "spinarak",
        "togepi",
    ],
    5: [
        "chikorita",
        "chinchou",
        "cubone",
        "cyndaquil",
        "drowzee",
        "dunsparce",
        "eevee",
        "elekid",
        "girafarig",
        "gligar",
        "grimer",
        "growlithe",
        "hoppip",
        "houndour",
        "kabuto",
        "koffing",
        "lickitung",
        "magby",
        "mantine",
        "marill",
        "natu",
        "omanyte",
        "onix",
        "phanpy",
        "pineco",
        "pinsir",
        "poliwag",
        "ponyta",
        "qwilfish",
        "rhyhorn",
        "scyther",
        "seel",
        "shellder",
        "shuckle",
        "smoochum",
        "sneasel",
        "snubbull",
        "stantler",
        "swinub",
        "tangela",
        "teddiursa",
        "totodile",
        "tyrogue",
        "voltorb",
        "wobbuffet",
        "wooper",
    ],
    10: [
        "aerodactyl",
        "chansey",
        "dratini",
        "lapras",
        "larvitar",
        "mareep",
        "miltank",
        "porygon",
        "skarmory",
        "snorlax",
        "sudowoodo",
    ]
}

def test_dataset(eggs, tiers):
    all_in_eggs = [species for egg_list in eggs.values() for species in egg_list]
    all_in_tiers = [species for tier_list in tiers.values() for species in tier_list]
    
    print("Found {} species by distance".format(len(all_in_eggs)))
    print("Found {} species by rarity".format(len(all_in_tiers)))
    
    print("Checking egg list against tier list:")
    for egg_class, egg_list in eggs.items():
        for species in egg_list:
            print("    {}:    ".format(species), end="")
            assert species in all_in_tiers
            print("OK")

    print("\nChecking tier list against egg list:")
    for tier_class, tier_list in tiers.items():
        for species in tier_list:
            print("    {}:    ".format(species), end="")
            assert species in all_in_eggs
            print("OK")


def find_pokemon_rarity(pokemon):
    for rarity, pokemon_list in pokemon_tiers.items():
        if pokemon in pokemon_list:
            return rarity
    
    raise Exception("Could not find {} in any of the Pokemon egg tiers, are you sure it's hatchable?".format(pokemon))

def rarity_by_egg_group(pokemon_eggs, rarity_tiers):
    egg_rarity = {}
    for egg_distance, pokemon_list in pokemon_eggs.items():
        egg_rarity[egg_distance] = sum(rarity_tiers[find_pokemon_rarity(pokemon)] for pokemon in pokemon_list)
    
        print("{}km: Found total rarity {}".format(egg_distance, egg_rarity[egg_distance]))

    return egg_rarity
    
def desirable_liklihood_by_egg_group(desirable_pokemon, pokemon_eggs, egg_rarity):
    desirable_likelihood = {}
    for egg_distance, pokemon_list in pokemon_eggs.items():
        desirable_likelihood[egg_distance] = 0
        for desirable in desirable_pokemon:
            if desirable in pokemon_list:
                print("Found desirable Pokemon {} in {}km egg group with {}/{} chance ({}%)".format(
                    desirable.capitalize(),
                    egg_distance,
                    rarity_tiers[find_pokemon_rarity(desirable)],
                    egg_rarity[egg_distance],
                    int(rarity_tiers[find_pokemon_rarity(desirable)] / egg_rarity[egg_distance] * 1000) / 10))
                desirable_likelihood[egg_distance] += rarity_tiers[find_pokemon_rarity(desirable)]
    
        print("{}km egg group has an overall desirable probability of {}/{} ({}%)".format(
            egg_distance,
            desirable_likelihood[egg_distance],
            egg_rarity[egg_distance],
            int(desirable_likelihood[egg_distance] / egg_rarity[egg_distance] * 1000) / 10))
            
    return desirable_likelihood
    
def desirable_liklihood_per_km(desirable_likelihood, pokemon_eggs, egg_rarity):
    desirables_per_km = {}    
    for egg_distance, pokemon_list in pokemon_eggs.items():
        desirables_per_km[egg_distance] = desirable_likelihood[egg_distance] / egg_distance
    
        print("{}km egg group has a {}% chance of desirable pokemon per km".format(
            egg_distance,
            int(desirables_per_km[egg_distance] / egg_rarity[egg_distance] * 1000) / 10))
    
    return desirables_per_km
    
def desirable_per_km(desirable_pokemon, pokemon_eggs, rarity_tiers):
    egg_rarity = rarity_by_egg_group(pokemon_eggs, rarity_tiers)
    print()
    desirable_likelihood = desirable_liklihood_by_egg_group(desirable_pokemon, pokemon_eggs, egg_rarity)
    print()
    desirables_per_km = desirable_liklihood_per_km(desirable_likelihood, pokemon_eggs, egg_rarity)

def generate_desirable_list(desirable_text):
    desirable_list = [pokemon.lower().strip() for pokemon in desirable_text.splitlines() if pokemon != ""]
    return desirable_list


# test_dataset(pokemon_eggs, pokemon_tiers)

desirable_per_km(generate_desirable_list(my_list), pokemon_eggs, rarity_tiers)