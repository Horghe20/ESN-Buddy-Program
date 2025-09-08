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

from flask import current_app
from database.tables import Buddy, Esner
import math


def compute_match_score(buddy: Buddy, esner: Esner, weights=None):
    """
    Compute an enhanced normalized matching score between a Buddy and an Esner.
    
    Improvements:
    - Guaranteed positive scores (0 to 1 range)
    - Better handling of empty sets
    - Buddy availability bonus to prioritize Esners with fewer buddies
    - All metrics normalized to 0-1 range
    
    :param buddy: An instance of the Buddy model
    :param esner: An instance of the Esner model
    :param weights: Optional dictionary specifying weights for attributes
    :return: A float representing the normalized matching score (0 to 1)
    """
    
    # Enhanced default weights with buddy availability
    if weights is None:
        weights = {
            'gender': 0.15,           # 15% - Important but not dominant
            'languages': 0.25,        # 25% - Critical for communication
            'nationalities': 0.10,    # 10% - Cultural connection
            'faculties': 0.15,        # 15% - Academic alignment
            'interests': 0.20,        # 20% - Personal compatibility
            'availability': 0.15      # 15% - Buddy distribution factor
        }
    
    # Helper function to safely get attributes as sets
    def get_attr_set(obj, getter):
        try:
            items = getter()
            if items is None:
                return set()
            return set(items)
        except Exception:
            return set()
    
    # 1. Gender Score (0 or 1)
    gender_score = 1.0 if esner.gender == buddy.gender else 0.0
    
    # 2. Languages Score (0 to 1)
    esner_languages = get_attr_set(esner, esner.get_languages_spoken)
    buddy_languages = get_attr_set(buddy, buddy.get_languages_spoken)
    
    if len(esner_languages) == 0 or len(buddy_languages) == 0:
        # If either has no languages, give partial credit if they match on "no languages"
        language_score = 0.3 if (len(esner_languages) == len(buddy_languages)) else 0.0
    else:
        # Jaccard similarity for better normalization
        intersection = len(esner_languages & buddy_languages)
        union = len(esner_languages | buddy_languages)
        language_score = intersection / union if union > 0 else 0.0
    
    # 3. Nationalities Score (0 to 1)
    esner_nationalities = get_attr_set(esner, esner.get_nationality)
    buddy_nationalities = get_attr_set(buddy, buddy.get_nationality)
    
    if "Not interested" in esner_nationalities:
        # Neutral score if not interested
        nationality_score = 0.5
    elif len(esner_nationalities) == 0 or len(buddy_nationalities) == 0:
        nationality_score = 0.3
    else:
        # Check if there's any match (binary: 0 or 1)
        nationality_score = 1.0 if len(esner_nationalities & buddy_nationalities) > 0 else 0.0
    
    # 4. Faculties Score (0 to 1)
    esner_faculties = get_attr_set(esner, esner.get_faculty)
    buddy_faculties = get_attr_set(buddy, buddy.get_faculty)
    
    if "Not interested" in esner_faculties:
        # Neutral score if not interested
        faculty_score = 0.5
    elif len(esner_faculties) == 0 or len(buddy_faculties) == 0:
        faculty_score = 0.3
    else:
        # Check if there's any match (binary: 0 or 1)
        faculty_score = 1.0 if len(esner_faculties & buddy_faculties) > 0 else 0.0
    
    # 5. Interests Score (0 to 1)
    esner_interests = get_attr_set(esner, esner.get_interests)
    buddy_interests = get_attr_set(buddy, buddy.get_interests)
    
    if len(esner_interests) == 0 or len(buddy_interests) == 0:
        interest_score = 0.0
    else:
        # Use a combination of overlap ratio and Jaccard similarity
        intersection = len(esner_interests & buddy_interests)
        min_size = min(len(esner_interests), len(buddy_interests))
        
        # Overlap coefficient (how much of the smaller set is covered)
        overlap_coefficient = intersection / min_size if min_size > 0 else 0.0
        
        # Jaccard similarity
        union = len(esner_interests | buddy_interests)
        jaccard = intersection / union if union > 0 else 0.0
        
        # Weighted average favoring overlap for better matches
        interest_score = 0.7 * overlap_coefficient + 0.3 * jaccard
    
    # 6. Availability Score (0 to 1) - NEW COMPONENT
    # This ensures Esners with fewer buddies get priority
    current_buddy_ratio = len(esner.buddies) / esner.max_number_of_buddy if esner.max_number_of_buddy > 0 else 1.0
    
    # Use exponential decay for smoother distribution
    # Score is high when ratio is low (few buddies) and decreases as ratio approaches 1
    availability_score = math.exp(-2 * current_buddy_ratio)  # Range: ~1.0 (no buddies) to ~0.135 (full)
    
    # Alternative: Linear decay (simpler but less smooth)
    # availability_score = max(0, 1 - current_buddy_ratio)
    
    # Calculate weighted sum
    total_score = (
        weights.get('gender', 0) * gender_score +
        weights.get('languages', 0) * language_score +
        weights.get('nationalities', 0) * nationality_score +
        weights.get('faculties', 0) * faculty_score +
        weights.get('interests', 0) * interest_score +
        weights.get('availability', 0) * availability_score
    )
    
    # Normalize by total weight to ensure score is between 0 and 1
    total_weight = sum(weights.values())
    normalized_score = total_score / total_weight if total_weight > 0 else 0.0
    
    # Ensure score is within bounds (defensive programming)
    normalized_score = max(0.0, min(1.0, normalized_score))
    
    return normalized_score


def match_making(buddies, esners):
    """
    Enhanced matchmaking with better distribution and guaranteed positive scores.
    """
    # Create match matrix
    match_matrix = [[0 for _ in range(len(esners))] for _ in range(len(buddies))]
    
    # Fill the match matrix
    for i, buddy in enumerate(buddies):
        for j, esner in enumerate(esners):
            match_matrix[i][j] = compute_match_score(buddy, esner)
    
    matches = []
    data = []
    
    # Track how many times each Esner has been selected in this matching round
    esner_selection_count = {esner.id: 0 for esner in esners}
    
    for i, buddy in enumerate(buddies):
        buddy_id = buddy.id
        
        # Build candidate list with enhanced scoring
        fs_candidates = []
        for j, esner in enumerate(esners):
            score = match_matrix[i][j]
            buddy_count = len(esner.buddies)
            
            # Apply a small penalty if this Esner was already selected multiple times in this round
            # This helps distribute buddies more evenly
            selection_penalty = esner_selection_count[esner.id] * 0.05
            adjusted_score = max(0, score - selection_penalty)
            
            fs_candidates.append((esner.id, adjusted_score, buddy_count, j, score))  # Keep original score too
        
        # Sort by adjusted score (descending)
        # No longer sorting by buddy_count as it's already factored into the score
        fs_candidates.sort(key=lambda x: -x[1])
        
        # Select top matches
        top_matches = fs_candidates[:current_app.config.get("TOP_AUTOMATIC_MATCH", 3)]
        
        # Record matches
        for fs_id, adjusted_score, buddy_count, index, original_score in top_matches:
            matches.append({
                "buddy_id": buddy_id,
                "foreign_student_id": fs_id,
                "score": original_score,  # Use original score for recording
                "adjusted_score": adjusted_score  # Optional: track adjusted score
            })
            
            # Update selection count
            esner_selection_count[fs_id] += 1
            
            # Get Esner instance
            corresponding_esner = next((esner for esner in esners if esner.id == fs_id), None)
            
            # Convert to percentage (guaranteed to be 0-100)
            percentage_score = int(original_score * 100)
            data.append((buddy, corresponding_esner, percentage_score))
    
    return data


# Optional: Configuration helper for weight tuning
def get_recommended_weights(priority='balanced'):
    """
    Get recommended weight configurations based on matching priority.
    
    :param priority: 'balanced', 'language_focused', 'interest_focused', or 'availability_focused'
    :return: Dictionary of weights
    """
    configs = {
        'balanced': {
            'gender': 0.15,
            'languages': 0.25,
            'nationalities': 0.10,
            'faculties': 0.15,
            'interests': 0.20,
            'availability': 0.15
        },
        'language_focused': {
            'gender': 0.10,
            'languages': 0.35,
            'nationalities': 0.10,
            'faculties': 0.10,
            'interests': 0.20,
            'availability': 0.15
        },
        'interest_focused': {
            'gender': 0.10,
            'languages': 0.20,
            'nationalities': 0.10,
            'faculties': 0.10,
            'interests': 0.35,
            'availability': 0.15
        },
        'availability_focused': {
            'gender': 0.10,
            'languages': 0.20,
            'nationalities': 0.10,
            'faculties': 0.15,
            'interests': 0.20,
            'availability': 0.25
        }
    }
    
    return configs.get(priority, configs['balanced'])