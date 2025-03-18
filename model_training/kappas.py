import numpy as np


LOG = False 


def binary_proportion(iResults, jResults):
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

def cohen_kappa(iResults, jResults):
    '''
    Finds the agreement between two result objects.

    Finds the agreement between the two objects. Gets the proportion of 
    matching values for the same key.
    
    iResults and jResults must have the same keys, be iterable, and have the same length.
    '''
    assert iResults.keys() == jResults.keys(), 'Keys must be the same'

    # Count agreement categories
    values = set(str(x) for x in set(iResults.values()).union(set(jResults.values())))
    total = 0
    observedAgrees = 0
    answerCounts = {x: 0 for x in values}
    annotatiorCounts = [{x: 0 for x in values}, {x: 0 for x in values}]

    for key in iResults:
        iAnswer = str(iResults[key])
        jAnswer = str(jResults[key])
        total += 1

        answerCounts[iAnswer] += 1
        answerCounts[jAnswer] += 1
        annotatiorCounts[0][iAnswer] += 1
        annotatiorCounts[1][jAnswer] += 1


        if iAnswer == jAnswer:
            observedAgrees += 1  # Exact match


    # Observed agreement (P_o)
    P_o = observedAgrees / total

    # Expected agreement (P_e)
    P_e = ([(annotatiorCounts[0][label] / total) * (annotatiorCounts[1][label] / total) for label in values])
    P_e = sum(P_e)

    # Cohen's Kappa
    if P_e == 1:  # Avoid division by zero in case of perfect agreement
        return 1.0
    kappa = (P_o - P_e) / (1 - P_e)
    return kappa

# List Comprehension -- order decades between min and max
minDecade = 1940 #the range for this does not matter -- it's ordinal distance.
maxDecade = 2030
year_ordinal = {x: i for i, x in enumerate([x for x in range(minDecade, maxDecade+1, 10)])}

def ordinal_kappa(iResults, jResults, order={}):
    '''
    Finds the agreement between two objects, taking into account the ordinal distance between the two objects.
     
    Gets the proportion of matching values for the same key. However, instead of it being a binary match,
    we instead have it be based on the distance between the two values.

        - 1990 vs 1990 = 1 (total agreement)
        - 1990 vs 1980 = 1 - 1*d (partial agreement)
        - 1990 vs 1970 = 1 - 2*d (partial agreement)
        - 1990 vs 1960 = 1 - 3*d (no agreement)
    
        etc, where d is a spacing parameter between 0 and 1.
        Match can only be between 1 and 0, however.

    iResults and jResults must have the same keys, be iterable, and have the same length.
    '''
    assert iResults.keys() == jResults.keys(), 'Keys must be the same'

    # Build confusion matrix
    decades = len(year_ordinal.keys())
    confusionMatrix = np.zeros((decades, decades))

    # Store amount of times a pair was found
    for key in iResults:
        i_idx = year_ordinal[iResults[key]]
        j_idx = year_ordinal[jResults[key]]
        confusionMatrix[i_idx, j_idx] += 1
    total = np.sum(confusionMatrix)

    # Compute weight matrix
    weights = np.zeros((decades, decades))
    for i in range(decades):
        for j in range(decades):
            diff = abs(i - j)
            weights[i, j] = diff / (decades - 1) ## larger differences penalized more

    # Compute observed agreement (weighted)
    observed_weighted = np.sum(weights * confusionMatrix) / total

    # Compute expected agreement (weighted)
    row_sums = confusionMatrix.sum(axis=1) / total  # P(i)
    col_sums = confusionMatrix.sum(axis=0) / total  # P(j)
    expected_matrix = np.outer(row_sums, col_sums) * total
    expected_weighted = np.sum(weights * expected_matrix) / total

    # Compute weighted kappa
    if expected_weighted == 1:  # Perfect agreement case
        return 1.0
    
    weighted_kappa = 1 - (observed_weighted / expected_weighted)

    return weighted_kappa


def cohen_set_kappa(iResultSet, jResultSet):
    '''
    Finds the setwise (proportion of intersection) agreement between two objects, using Jaccard Similarity.

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
    universalKeys = set(iResultSet.keys())

    # Find how many columns we are checking
    columnCount = len(iResultSet)
    assert columnCount == len(jResultSet), 'Both sets must have the same length'
    assert all([len(x) == 2 for x in iResultSet.values()]), 'All songs should have 2 topics'

    # Find Row Count
    rowCount = len(iResultSet)

    # Find the produced jaccard similarity for the sets (i, j)
    jaccards = []
    for key in universalKeys:
        assert all([key in iResultSet]), 'Keys must be the same in all items in iResultSet'
        assert all([key in jResultSet]), 'Keys must be the same in all items in jResultSet'

        # Get the SET of annotations
        iSet = iResultSet[key] #of length between 1 and rowcount
        jSet = jResultSet[key]  #of length between 1 and rowcount

        # Get the intersection of the sets to see how many atucally matched
        # Jaccard Similarity
        intersection = iSet.intersection(jSet)
        union = iSet.union(jSet)
        jaccards.append(len(intersection) / len(union))

    # Get list of every label
    allLabels = set()
    for _, labelSet in iResultSet.items():
        allLabels = allLabels.union(labelSet)
    for _, labelSet in jResultSet.items():
        allLabels = allLabels.union(labelSet)

    # find the liklihood that label exists in setI
    def construct_appearance_liklihood(annotationSet):

        liklihoods = {}
        for label in allLabels:
            
            # How often does it appear as a label?
            appearences = sum([ 1 if label in subset else 0 for subset in annotationSet.values() ])

            # Calculate the liklihood
            liklihoods[label] =  appearences / rowCount
        
        return liklihoods
            
    # Get
    liklihoodI = construct_appearance_liklihood(iResultSet)
    liklihoodJ = construct_appearance_liklihood(jResultSet)
    
    # Calculate the expected values
    expected_jaccards = []
    for key in universalKeys:
        
        iList = list(iResultSet[key])
        jList = list(jResultSet[key])

        labeli1 = iList[0]
        labeli2 = iList[1]
        labelj1 = jList[0]
        labelj2 = jList[1]

        # Calculate the expected jaccard
        expected_jaccard = (
            liklihoodI[labeli1] * liklihoodJ[labelj1] +
            liklihoodI[labeli1] * liklihoodJ[labelj2] +
            liklihoodI[labeli2] * liklihoodJ[labelj1] +
            liklihoodI[labeli2] * liklihoodJ[labelj2]
        ) / 4
        expected_jaccards.append(expected_jaccard) 

    # Compute P_o (Observed agreement) and P_e (Expected agreement)
    P_o = np.mean(jaccards)
    P_e = np.mean(expected_jaccards)

    # Compute Cohen's Kappa
    if P_e == 1:  # Avoid division by zero if perfect agreement
        return 1.0
    return (P_o - P_e) / (1 - P_e)


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

