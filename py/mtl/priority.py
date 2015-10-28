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

def priority_needed(target_flag, results_flag):
    """
    Determines the priority for a target.
    """
    
    if((target_flag != 0) & (results_flag==0)):
        possible_names = targetmask.names(target_flag)
        priorities = []
        for name in possible_names:
            mask_id = targetmask.mask(name)            
            priorities.append(prioritymask.bitnum(name))
    else:
        raise NameError('Have to implement something in the case results_flag!=0')
        
                
    return min(priorities)
