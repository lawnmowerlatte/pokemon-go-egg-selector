#!env python3

my_list = """
ABRA
Machop
diglett
cHanSey
"""

rarity_denominator = 257
rarity_tiers = {
    "common": 8,
    "uncommon": 4,
    "rare": 2,
    "ultra-rare": 1
}

pokemon_tiers = {
    "common": [
        "ekans",
        "nidoran-f",
        "nidoran-m",
        "poliwag",
        "geodude",
        "ponyta",
        "krabby",
        "goldeen",
        "staryu",
        "phanpy"
    ],
    "uncommon": [
        "bulbasaur",
        "charmander",
        "squirtle",
        "vulpix",
        "oddish",
        "diglett",
        "growlithe",
        "abra",
        "machop",
        "slowpoke",
        "magnemite",
        "shellder",
        "gastly",
        "drowzee",
        "voltorb",
        "exeggcute",
        "cubone",
        "rhyhorn",
        "eevee",
        "dratini",
        "pichu",
        "cleffa",
        "igglybuff",
        "togepi",
        "aipom",
        "pineco",
        "gligar",
        "slugma",
        "mantine",
        "stantler",
        "tyrogue",
        "smoochum",
        "elekid",
        "magby",
        "larvitar"
    ],
    "rare": [
        "seel",
        "onix",
        "chansey",
        "tangela",
        "scyther",
        "pinsir",
        "mareep",
        "sudowoodo",
        "remoraid"
    ],
    "ultra-rare": [
        "grimer",
        "lickitung",
        "koffing",
        "lapras",
        "porygon",
        "omanyte",
        "kabuto",
        "aerodactyl",
        "snorlax",
        "yanma",
        "misdreavus",
        "wobbuffet",
        "girafarig",
        "dunsparce",
        "qwilfish",
        "shuckle",
        "sneasel",
        "skarmory",
        "miltank"
    ]
}

pokemon_eggs = {
    2: [
    	"bulbasaur",
    	"charmander",
    	"squirtle",
    	"ekans",
    	"nidoran-f",
    	"nidoran-m",
    	"oddish",
    	"diglett",
    	"abra",
    	"machop",
    	"geodude",
    	"slowpoke",
    	"gastly",
    	"krabby",
    	"exeggcute",
    	"goldeen",
    	"pichu",
    	"cleffa",
    	"igglybuff",
    	"togepi",
    	"aipom",
    	"misdreavus",
    	"slugma",
    	"remoraid"
    ],
    5: [
    	"vulpix",
    	"growlithe",
    	"poliwag",
    	"ponyta",
    	"magnemite",
    	"seel",
    	"grimer",
    	"shellder",
    	"onix",
    	"drowzee",
    	"voltorb",
    	"cubone",
    	"lickitung",
    	"koffing",
    	"rhyhorn",
    	"tangela",
    	"staryu",
    	"scyther",
    	"pinsir",
    	"eevee",
    	"porygon",
    	"omanyte",
    	"kabuto",
    	"yanma",
    	"wobbuffet",
    	"girafarig",
    	"dunsparce",
    	"qwilfish",
    	"shuckle",
    	"sneasel",
    	"phanpy",
    	"stantler",
    	"tyrogue",
    	"smoochum",
    	"elekid",
    	"magby"
    ],
    10: [
    	"chansey",
    	"lapras",
    	"aerodactyl",
    	"snorlax",
    	"dratini",
    	"mareep",
    	"sudowoodo",
    	"pineco",
    	"gligar",
    	"mantine",
    	"skarmory",
    	"miltank",
    	"larvitar"
    ]
}

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

desirable_per_km(generate_desirable_list(my_list), pokemon_eggs, rarity_tiers)