"""
legendas:

    - OntoNotes schema:

        TYPE	DESCRIPTION
        PERSON	People, including fictional.
        NORP	Nationalities or religious or political groups.
        FAC	Buildings, airports, highways, bridges, etc.
        ORG	Companies, agencies, institutions, etc.
        GPE	Countries, cities, states.
        LOC	Non-GPE locations, mountain ranges, bodies of water.
        PRODUCT	Objects, vehicles, foods, etc. (Not services.)
        EVENT	Named hurricanes, battles, wars, sports events, etc.
        WORK_OF_ART	Titles of books, songs, etc.
        LAW	Named documents made into laws.
        LANGUAGE	Any named language.
        DATE	Absolute or relative dates or periods.
        TIME	Times smaller than a day.
        PERCENT	Percentage, including ”%“.
        MONEY	Monetary values, including unit.
        QUANTITY	Measurements, as of weight or distance.
        ORDINAL	“first”, “second”, etc.
        CARDINAL	Numerals that do not fall under another type.

    - Wikipedia Schema:

        PER	Named person or family.
        LOC	Name of politically or geographically defined location (cities, provinces, countries, international regions, bodies of water, mountains).
        ORG	Named corporate, governmental, or other organizational entity.
        MISC	Miscellaneous entities, e.g. events, nationalities, products or works of art
"""

# TODO: Escrever mais exemplos
TRAINING_DATA = [
    ('Júlia é uma bela moça', {'entities': [(0, 5, 'PER')]}),
    ('Lisa é uma garota muito inteligente', {'entities': [(0, 4, 'PER')]}),
    ('Kevin é um bom amigo', {'entities': [(0, 5, 'PER')]}),
    ('Bruno é nome do desenvolvedor da API', {'entities': [(0, 6, 'PER')]}),
    ('No meio do ano irei para São Paulo fazer mais um curso', {'entities': [(25, 34, 'LOC')]}),
    ('Em 04/09/1990 nasceu uma linda criança', {'entities': [(3, 13, 'DATE')]}),
    ('', {'entities': [()]}),
    ('', {'entities': [()]})
]
