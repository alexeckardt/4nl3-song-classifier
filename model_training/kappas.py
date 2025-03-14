LOG = False 

def cohen_kappa(iResults, jResults):
    '''
    Finds the binary agreement between two result objects.

    Finds the agreement between the two objects. Gets the proportion of 
    matching values for the same key.
    
    iResults and jResults must have the same keys, be iterable, and have the same length.
    '''
    assert iResults.keys() == jResults.keys(), 'Keys must be the same'

    # Print
    matches = 0
    for key in iResults:
        iAnswer = iResults[key]
        jAnswer = jResults[key]

        match = iAnswer == jAnswer
        if match:
            matches += 1

        if LOG: print(f'{key} {match}')

    # Compute the Kappa
    return matches / len(iResults)

# List Comprehension -- order decades between min and max
minDecade = 1940 #the range for this does not matter -- it's ordinal distance.
maxDecade = 2030
year_ordinal = {x: i for i, x in enumerate([x for x in range(minDecade, maxDecade+1, 10)])}

def ordinal_kappa(iResults, jResults, spacing=1/3, order={}):
    '''
    Finds the ordinal distance agreement between two objects.

    Finds the agreement between the two objects, using an integer distance.
     
    Gets the proportion of matching values for the same key. However, instead of it being a binary match,
    we instead have it be based on the distance between the two values.

        - 1990 vs 1990 = 1 (total agreement)
        - 1990 vs 1980 = 1 - 1*d (partial agreement)
        - 1990 vs 1970 = 1 - 2*d (partial agreement)
        - 1990 vs 1960 = 1 - 3*d (no agreement)
    
        etc, where d is a spacing parameter (default 1/3).
        Match can only be between 1 and 0, however.

    iResults and jResults must have the same keys, be iterable, and have the same length.
    '''
    assert iResults.keys() == jResults.keys(), 'Keys must be the same'

    # Print
    matches = 0
    for key in iResults:
        iAnswer = int(iResults[key])
        jAnswer = int(jResults[key])

        iOrd = year_ordinal[iAnswer]
        jOrd = year_ordinal[jAnswer]

        diff = abs(iOrd - jOrd)
        match = max(0, 1 - (diff*spacing))

        matches += match

        if LOG: print(f'{key} {match}')

    # Compute the Kappa
    return matches / len(iResults)





def cohen_set_kappa(iResultSet, jResultSet):
    '''
    Finds the setwise (proportion of intersection) agreement between two objects.

    Finds the agreement between the two objects on MULTIPLE keys (columns).
    For instance, if we have two datasets

    i:
        topic1: b
        topic2: a

    j:
        topic1: a
        topic2: b

    Running cohen_kappa on topic1 and topic2 would both result in 0, since there is no overlap.
    However, we SHOULD consider this as a whole match, since both annotators agreed on 'a' and 'b' being topics.

    Consider the following case:
    i:
        topic1: b
        topic2: a

    j:
        topic1: a
        topic2: c

    We should conider this half a match, since both annotators agreed on 'a' being a topic.

    iResultSet and jResultSet must be the same length.
    each item in each of the above respectivley (iResults and jResults) must have the same keys, be iterable, and have the same length.
    '''
    
    # Exit
    if len(iResultSet) == 0:
        return 0

    # We are assuming ALL result items (in BOTH sets) have the same keys. (Universal keys)
    universalKeys = set(iResultSet[0].keys())

    # Find how many columns we are checking
    columnCount = len(iResultSet)
    assert columnCount == len(jResultSet), 'Both sets must have the same length'

    # Find Row Count
    rowCount = len(iResultSet[0])
    matches = 0

    for key in universalKeys:
        assert all([key in x for x in iResultSet]), 'Keys must be the same in all items in iResultSet'
        assert all([key in x for x in jResultSet]), 'Keys must be the same in all items in jResultSet'

        # Get the SET of annotations
        iSet = {x[key] for x in iResultSet} #of length between 1 and rowcount
        jSet = {x[key] for x in jResultSet}  #of length between 1 and rowcount

        # Get the intersection of the sets to see how many atucally matched
        intersection = iSet.intersection(jSet)
        matches += len(intersection) / columnCount # keep between 0 and 1

    return matches / rowCount



def single_cohen_set_kappa(iResultSet, jResultSet):
    '''
    Finds the "any overlap" (intersection is not empty) agreement between two objects.

    Finds the agreement between the two objects on MULTIPLE keys (columns), using a binary check for any match.
    For instance, if we have two datasets

    i:
        topic1: b
        topic2: a

    j:
        topic1: a
        topic2: b

    Running cohen_kappa on topic1 and topic2 would both result in 0, since there is no overlap.
    However, we SHOULD consider this as a whole match, since both annotators agreed on 'a' and 'b' being topics.

    Consider the following case:
    i:
        topic1: b
        topic2: a

    j:
        topic1: a
        topic2: c

    We consider this a FULL match, since both annotators agreed on 'a' being a topic.

    iResultSet and jResultSet must be the same length.
    each item in each of the above respectivley (iResults and jResults) must have the same keys, be iterable, and have the same length.
    '''
    
    # Exit
    if len(iResultSet) == 0:
        return 0

    # We are assuming ALL result items (in BOTH sets) have the same keys. (Universal keys)
    universalKeys = set(iResultSet[0].keys())

    # Find how many columns we are checking
    columnCount = len(iResultSet)
    assert columnCount == len(jResultSet), 'Both sets must have the same length'

    # Find Row Count
    rowCount = len(iResultSet[0])
    matches = 0

    for key in universalKeys:
        assert all([key in x for x in iResultSet]), 'Keys must be the same in all items in iResultSet'
        assert all([key in x for x in jResultSet]), 'Keys must be the same in all items in jResultSet'

        # Get the SET of annotations
        iSet = {x[key] for x in iResultSet} #of length between 1 and rowcount
        jSet = {x[key] for x in jResultSet}  #of length between 1 and rowcount

        # Get the intersection of the sets to see how many atucally matched
        intersection = iSet.intersection(jSet)
        if len(intersection) > 0:
            matches += 1 
        else:
            if LOG: print(f'No match on {key} -- {iSet} vs {jSet}')

    return matches / rowCount

