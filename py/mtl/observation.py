def numobs_needed(target_flag, numobs_target, numobs_done, obs_z, obs_z_err, spec_flag):
    """
    Determines the number of observations still needed for an object.
    """
    numobs = numobs_target - numobs_done

    return numobs


