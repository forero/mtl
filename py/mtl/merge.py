import fitsio
import numpy as np
from desitarget.internal.maskbits import BitMask
from mtl.observation import numobs_needed
from mtl.priority import priority_needed
import mtl
import yaml


def create_mtl(target_file, specresults_file, output_file):
    """
    Consolidates a Merged Target List file.
    """
    # input basic data
    targets = fitsio.read(target_file, 1, upper=True)
    specresults = fitsio.read(specresults_file, 1, upper=True)

    # structure for output data
    type_table = [
        ('TARGETID', '>i4'), 
        ('BRICKNAME', '|S8'),
        ('RA', '>f4'), 
        ('DEC', '>f4'),
        ('NUMOBS', '>i4'), 
        ('PRIORITY', '>i4')
    ]

    # loops over the targets looking for:
    # - number of observations performed on the target
    # - a precise redshift
    # - a definite targetflag


    n_points = len(targets['TARGETID'])

    ra = []
    dec = []
    objid = []
    priority = [] 
    numobs = []
    brickname = []


    for i in range(n_points):
        item_id = targets['TARGETID'][i]
        item_target_flag = targets['TARGETFLAG'][i]
        n_obs_target = targets['NUMOBS'][i]

        # find properties in specresults
        index = np.where(item_id == specresults['TARGETID'])        
        index = index[0]
        if(len(index)>1):
            print("{} {} NO".format(i, index))
            raise NameError('There are more than two redshift determinations for the same object')
        n_obs_done = specresults['NUMOBSUSED'][index]

        n = numobs_needed(n_obs_target, n_obs_done)
        p = priority_needed(item_target_flag, item_spec_flag)
        
        if n :
            ra.append(targets['RA'][i])
            dec.append(targets['DEC'][i])
            objid.append(targets['TARGETID'][i])
            priority.append(p)
            numobs.append(n)
            brickname.append(targets['BRICKNAME'][i])


    data = np.ndarray(shape=(len(objid)), dtype=type_table)    
    data['TARGETID'] = objid
    data['RA'] = ra
    data['DEC'] = dec
    data['BRICKNAME'] = brickname
    data['NUMOBS'] = numobs
    data['PRIORITY'] = priority

    #- Create header to include versions, etc.
    hdr = fitsio.FITSHDR()
    hdr['DEPNAM00'] = 'mtl'
    hdr.add_record(dict(name='DEPVER00', value=mtl.__version__, comment='mtl.__version__'))
    hdr['DEPNAM01'] = 'mtl-git'
    hdr.add_record(dict(name='DEPVAL01', value=mtl.gitversion(), comment='git revision'))    

    fitsio.write(output_file, data, extname='MTL', header=hdr, clobber=True)    
    print('wrote {} items to MTL file'.format(len(objid)))

    return 
