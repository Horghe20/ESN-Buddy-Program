# Match

[Esn-buddy-program Index](../README.md#esn-buddy-program-index) / [Utils](./index.md#utils) / Match

> Auto-generated documentation for [utils.match](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/match.py) module.

- [Match](#match)
  - [compute_match_score](#compute_match_score)
  - [match_making](#match_making)

## compute_match_score

[Show source in match.py:27](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/match.py#L27)

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

#### Arguments

- `buddy` - An instance of the Buddy model representing an Erasmus student seeking a buddy.
- `esner` - An instance of the Esner model representing an ESN associate.
- `weights` - Optional dictionary specifying weights for the attributes. Keys should be
                'gender', 'languages', 'nationalities', 'faculties', and 'interests'.

#### Returns

A float representing the normalized matching score (0 to 1).

**Example**:

```python
>>> score = compute_match_score(buddy, esner)
>>> print(f"Match score: {score:.2f}")
```

#### Signature

```python
def compute_match_score(buddy: Buddy, esner: Esner, weights=None): ...
```

#### See also

- [Buddy](../database/tables.md#buddy)
- [Esner](../database/tables.md#esner)



## match_making

[Show source in match.py:167](https://github.com/Horghe20/ESN-Buddy-Program/blob/main/utils/match.py#L167)

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

#### Arguments

- `buddies` - List of Buddy instances.
- `esner` - List of Esner instances.

#### Returns

A list of tuples in the format (Buddy, Esner, score_percentage) representing the matches.

**Example**:

```python
>>> matched_data = match_making(buddies, esner)
>>> for buddy, esner, score in matched_data:
...     print(f"Buddy {buddy.id} matched with Esner {esner.id} with score {score}%")
```

#### Signature

```python
def match_making(buddies, esners): ...
```