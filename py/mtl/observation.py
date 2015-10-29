def numobs_needed(numobs_target, numobs_done):
    """
    Determines the number of observations still needed for an object.
    """
    numobs = numobs_target - numobs_done

    return max(0,numobs)


