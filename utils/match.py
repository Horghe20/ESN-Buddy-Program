"""
Matchmaking Algorithm for ESN Matchmaking System

This module provides functions to compute matching scores between Buddies and Esner
and to perform the matchmaking process. The matching is based on several attributes,
including gender, languages, nationalities, faculties, and interests. The module uses
a weighted scoring system to determine the best matches.

Modules and Libraries:
- numpy: Used for creating and manipulating the matching matrix.
- sklearn.metrics.pairwise: Provides cosine similarity calculations (imported but not used here).
- database.tables: Contains the Buddy and Esner models.
- utils.config: Provides configuration settings, including the number of top matches to consider.

Functions:
- compute_match_score(buddy, esner, weights=None): Computes a normalized matching score between a Buddy and an Esner.
- match_making(buddies, esner): Performs matchmaking between lists of Buddy and Esner instances.

Usage:
- Use `compute_match_score` to calculate individual match scores between a Buddy and an Esner.
- Use `match_making` to generate a list of top matches for each Buddy based on computed scores.
"""

from database.tables import Buddy, Esner
from utils.config import TOP_AUTOMATIC_MATCH

def compute_match_score(buddy: Buddy, esner: Esner, weights=None):
    """
    Compute a normalized matching score between a Buddy and an Esner.
    
    This function compares a Buddy and an Esner across several key attributes and returns
    a normalized score between 0 and 1 indicating how well they match. The score is computed
    as a weighted average of several individual metrics:
    
    1. **Gender Score**:
       - If the Buddy and the Esner have the same gender, a score of 1.0 is assigned.
       - Otherwise, a score of 0.5 is given.
    
    2. **Languages Score**:
       - Both the Buddy and the Esner provide a set of languages (using their respective getter
         methods, e.g., `get_languages_spoken()`).
       - The score is computed as the ratio:
         
             language_score = |common languages| / min(|esner_languages|, |buddy_languages|)
         
         This ensures that if all languages in the smaller set are found in the larger set,
         the score will be 1.
       - If the Esner does not list any languages, the score defaults to 0.
    
    3. **Nationalities Score**:
       - Both parties have one or more nationalities, obtained via `get_nationality()`.
       - If the Esner's nationality list is provided and does not include "Not interested", then:
         
             nationality_score = |common nationalities|
         
         Otherwise, a default score of 0.5 is used. (This default might be interpreted as a
         neutral or partially matching value.)
    
    4. **Faculties Score**:
       - Similarly, both have faculties obtained via `get_faculty()`.
       - If the Esner's faculty list is provided and does not contain "Not interested", then:
         
             faculty_score = |common faculties|
         
         Else, a default score of 0.5 is used.
    
    5. **Interests Score**:
       - Both have interests (via `get_interests()`), and the score is calculated as:
         
             interest_score = |common interests| / min(|esner_interests|, |buddy_interests|)
         
         Again, if no interests are listed by the Esner, the score is set to 0.
    
    The final matching score is computed using a weighted sum of these individual scores.
    If the caller does not supply a weights dictionary, the function uses the following defaults:
    
        weights = {
            'gender': 0.5,
            'languages': 1,
            'nationalities': 0.8,
            'faculties': 0.5,
            'interests': 1.0
        }
    
    After calculating the weighted sum, the score is normalized by dividing by the total
    weight, resulting in a final score in the range [0, 1].
    
    :param buddy: An instance of the Buddy model representing an Erasmus student seeking a buddy.
    :param esner: An instance of the Esner model representing an ESN associate.
    :param weights: Optional dictionary specifying weights for the attributes. Keys should be
                    'gender', 'languages', 'nationalities', 'faculties', and 'interests'.
    :return: A float representing the normalized matching score (0 to 1).
    
    **Example**:
    
    >>> score = compute_match_score(buddy, esner)
    >>> print(f"Match score: {score:.2f}")
    """
    # Default weights if not provided:
    if weights is None:
        weights = {
            'gender': 0.7,
            'languages': 1,
            'nationalities': 0.5,
            'faculties': 0.7,
            'interests': 0.6
        }
    
    # 1. Gender score
    gender_score = 1.0 if esner.gender == buddy.gender else 0.5

    # Helper function: Retrieve attribute as a set; return an empty set if missing.
    def get_attr_set(obj, getter):
        try:
            items = getter()
            if items is None:
                return set()
            # Convert the list (or similar iterable) to a set.
            return set(items)
        except Exception:
            return set()
    
    # 2. Languages score
    esner_languages = get_attr_set(esner, esner.get_languages_spoken)
    buddy_languages = get_attr_set(buddy, buddy.get_languages_spoken)
    language_score = len(esner_languages & buddy_languages) / (min(len(esner_languages), len(buddy_languages)))

    # 3. Nationalities score
    esner_nationalities = get_attr_set(esner, esner.get_nationality)
    buddy_nationalities = get_attr_set(buddy, buddy.get_nationality)
    if "Not interested" not in esner_nationalities:
        nationality_score = len(esner_nationalities & buddy_nationalities)
    else:
        nationality_score = 0.5

    # 4. Faculties score
    esner_faculties = get_attr_set(esner, esner.get_faculty)
    buddy_faculties = get_attr_set(buddy, buddy.get_faculty)
    if "Not interested" not in esner_faculties:
        faculty_score = len(esner_faculties & buddy_faculties)
    else:
        faculty_score = 0.5

    # 5. Interests score
    esner_interests = get_attr_set(esner, esner.get_interests)
    buddy_interests = get_attr_set(buddy, buddy.get_interests)
    interest_score = len(esner_interests & buddy_interests) / (min(len(esner_interests), len(buddy_interests)))


    # Calculate weighted sum of scores.
    total_weight = (weights['gender'] + weights['languages'] +
                    weights['nationalities'] + weights['faculties'] +
                    weights['interests'])
    
    score = (weights['gender'] * gender_score +
             weights['languages'] * language_score +
             weights['nationalities'] * nationality_score +
             weights['faculties'] * faculty_score +
             weights['interests'] * interest_score)
    
    # Normalize the score to be between 0 and 1.
    normalized_score = (score / total_weight) - (len(esner.buddies) / esner.max_number_of_buddy)
    
    return normalized_score


def match_making(buddies, esners):
    """
    Perform matchmaking between lists of Buddy and Esner instances.
    
    This function calculates a 2D matching matrix where each element represents the matching score
    between a given Buddy and an Esner (computed using compute_match_score). The algorithm then selects
    potential matches for each Buddy based on the following steps:
    
    1. **Matching Matrix Construction**:
       - For each Buddy (row) and each Esner (column), compute the matching score and store it in
         a 2D numpy array.
    
    2. **Candidate Selection**:
       - For each Buddy, a list of candidate Esner is built. Each candidate is a tuple containing:
         (esner.id, match_score, current_buddy_count, index_in_esner_list).
       - The current number of buddies an Esner has is retrieved (via `len(esner.buddies)`).
    
    3. **Sorting of Candidates**:
       - The candidates are sorted using two criteria:
         a) **Primary:** The current number of buddies (ascending order, so that Esner with fewer buddies are prioritized).
         b) **Secondary:** The matching score (descending order, so that higher scores are favored).
    
    4. **Selection of Top Candidates**:
       - Up to 3 top candidates are chosen for each Buddy from the sorted list.
    
    5. **Result Compilation**:
       - For each selected candidate, a match is recorded containing the Buddy's ID, the Esner's ID, and the match score.
       - Additionally, a list of tuples is compiled where each tuple contains (Buddy instance, Esner instance, score as an integer percentage).
    
    :param buddies: List of Buddy instances.
    :param esner: List of Esner instances.
    :return: A list of tuples in the format (Buddy, Esner, score_percentage) representing the matches.
    
    **Example**:
    
    >>> matched_data = match_making(buddies, esner)\n\
    >>> for buddy, esner, score in matched_data:\n\
    ...     print(f\"Buddy {buddy.id} matched with Esner {esner.id} with score {score}%\")\n
    """
    # Create a 2D match matrix with shape (number of buddies, number of esner)
    match_matrix = [[0 for _ in range(len(esners))] for _ in range(len(buddies))]
    # Fill the match matrix using compute_match_score for each Buddy-Esner pair.
    for i, buddy in enumerate(buddies):
        for j, esner in enumerate(esners):
            match_matrix[i][j] = compute_match_score(buddy, esner)
    
    # List to collect final match information.
    matches = []
    data = []
    
    # Process each buddy to find the best matching Esner.
    for i, buddy in enumerate(buddies):
        buddy_id = buddy.id

        # Build candidate list: each candidate is (esner.id, match_score, current_buddy_count, index)
        fs_candidates = []
        for j, esner in enumerate(esners):
            score = match_matrix[i][j]
            buddy_count = len(esner.buddies)  # Number of buddies already matched with this Esner.
            fs_candidates.append((esner.id, score, buddy_count, j))
        
        # Sort candidates: prioritize Esner with fewer buddies and higher match score.
        fs_candidates.sort(key=lambda x: (x[2], -x[1]))
        
        # Select the top 3 candidates.
        top_matches = fs_candidates[:TOP_AUTOMATIC_MATCH]
        
        # Record the selected matches.
        for fs_id, score, buddy_count, index in top_matches:
            matches.append({
                "buddy_id": buddy_id,
                "foreign_student_id": fs_id,
                "score": score
            })
            
            # Retrieve the corresponding Esner instance for additional details.
            corresponding_esner = next((esner for esner in esners if esner.id == fs_id), None)
            data.append((buddy, corresponding_esner, int(score * 100)))
    
    return data

# ==============================================================================
# Example Usage:
# Assuming you have a list of Buddy instances and a list of Esner instances:
#
# buddies = [buddy1, buddy2, ...]  # SQLAlchemy model instances of Buddy.
# esner = [esner1, esner2, ...]     # SQLAlchemy model instances of Esner.
#
# matched_data = match_making(buddies, esner)
# for buddy, esner, score in matched_data:
#     print(f"Buddy {buddy.id} matched with Esner {esner.id} with score {score}%")
# ==============================================================================