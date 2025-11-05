import random
FACTS = [
    "The shortest war in history lasted 38 minutes.",
    "Octopuses have three hearts.",
    "Bananas are berries, but strawberries aren't.",
    "Honey never spoils.",
    "The Eiffel Tower can be 15 cm taller during summer."
]
def get_random_fact():
    return random.choice(FACTS)
