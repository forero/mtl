from desitarget.targetmask import targetmask
from desitarget.internal.maskbits import BitMask
import yaml

_bitdefs = yaml.load("""
#- Target type Mask
prioritymask:
    - [LRG,       400, "LRG"]
    - [ELG,       300, "ELG"]
    - [BGS,       200, "BGS"]
    - [QSO,       100, "QSO"]
""")
prioritymask = BitMask('prioritymask', _bitdefs)

def priority_needed(target_flag, results_subtype=None):
    """
    Determines the priority for a target.
    """
    if (results_subtype is None):
        if (target_flag != 0):
            possible_names = targetmask.names(target_flag)
            priorities = []
            for name in possible_names:
                mask_id = targetmask.mask(name)            
                priorities.append(prioritymask.bitnum(name))
        else:
            raise NameError("You don't know anything about your target!")                        
        priority = priorities.index(min(priorities))
    else:
        priority =  prioritymask.bitnum(results_subtype.rstrip())


    return priority


def return_type(target_mask):
    """
    Returns the type from a mask.
    In the case of multiple possibilities picks the highest priority
    """

    if(target_mask):
        possible_names = targetmask.names(target_mask)
        priorities = []
        for name in possible_names:
            mask_id = targetmask.mask(name)            
            priorities.append(prioritymask.bitnum(name))
    else:
        raise NameError('target_mask is zero!')
    
    min_index = priorities.index(min(priorities))
    
                
    return possible_names[min_index]
