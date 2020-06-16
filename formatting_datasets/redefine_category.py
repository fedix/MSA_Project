def find_category(categories):
    """
    Define the categories in FIFA format,
    based on original KudaGo categories.
    """
    
    new_categories = []
    # KudaGo categories in 'dict' values - list,
    # Proposed new (FIFA) category as 'dict' key.
    correspondence_list = {
        "Sights & Landmarks": ["sights",
                               "recreation",
                               "photo-places",
                               "homesteads",
                               "palace",
                               "church",
                               "temple",
                               "monastery",
                               "fountain",
                               "bridge",
                               "synagogue"],
        
        "Museums & Libraries": ["museums",
                                "library",
                                "observatory"],
        
        "Others": ["attractions",
                   "kids",
                   "amusement",
                   "shops",
                   "suburb",
                   "other",
                   "coworking",
                   "culture",
                   "inn",
                   "business",
                   "handmade",
                   "animal-shelters",
                   "stable",
                   "rynok",
                   "station",
                   "metro",
                   "car-washes",
                   "airports",
                   "hostels",
                   "dogs",
                   "cats"],
        
        "Nature & Parks": ["park",
                           "prirodnyj-zapovednik"],
        
        "Restaurant": ["restaurants",
                       "clubs",
                       "salons",
                       "bar",
                       "anticafe",
                       "brewery"],
        
        "Concerts & Shows": ["education-centers",
                             "art-centers",
                             "theatre",
                             "concert-hall",
                             "cinema",
                             "art-space",
                             "dance-studio",
                             "workshops",
                             "questroom",
                             "strip-club"],
    }
    
    # For each possible original category ('origin_cat')
    # adds corresponding FIFA category ('new_cat')
    for category in categories:
        for new_cat, origin_cat in correspondence_list.items():
            if category in origin_cat:
                if new_cat not in new_categories:
                    new_categories.append(new_cat)
                
    return new_categories

