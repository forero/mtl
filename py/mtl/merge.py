import fitsio
import numpy as np
from mtl.observation import numobs_needed
from mtl.priority import priority_needed

def create_mtl(target_file, specresults_file, observations_file, output_file):
    """
    Consolidates a Merged Target List file.
    """
    # input basic data
    targets = fitsio.read(target_file, 1, upper=True)
    specresults = fitsio.read(specresults_file, 1, upper=True)
    observations = fitsio.read(observations_file, 1, upper=True)

    # structure for output data
    type_table = [
        ('TARGETID', '>i4'), 
        ('BRICKNAME', '|S8'),
        ('TARGETFLAG', '>i8'), 
        ('Z', '>f4'), 
        ('ZERR', '>f4')
    ]

    # loops over the targets looking for:
    # - number of observations performed on the target
    # - a precise redshift
    # - a definite targetflag
    targetid = targets['TARGETID']
    n_points = len(targetid)

    observations_id = observations['TARGETID']
    observation_tile_id = observations['TILEID']
    observation_fiber_id = observations['FIBERID']

    spec_z = specresults['Z']
    spec_z_err = specresults['ZERR']
    spec_id = specresults['TARGETID']
    spec_flag = specresults['TARGETFLAG']

    target_ra = targets['RA']
    target_dec = targets['DEC']
    target_flag = targets['TARGETFLAG']

    ra = []
    dec = []
    objid = []
    priority = [] 
    numobs = []
    brickname = []

#    Object-id (int)
#    RA (float)
#    DEC (float)
#    FiberPriority (int)
#    FiberObservationsNeeded (int)
#    BrickName (string) needed to track down data flo

    for i in range(n_points):
        item_target_flag = target_flag[i]
        # counts numbers of observations
        item_id = targetid[i]
        n_obs_done = 0
        if item_id in spec_id:
            index = np.where(item_id == observations_id)
            index = index[0]
            if(len(index)):
                tile_id  = observation_tile_id[index]
                fiber_id = observation_tile_id[index]
                n_obs_done = sum((tile_id > 0) & (fiber_id > 0))

                print("{} {} {} RES".format(i, index, n_obs_done))
        
        # finds a value for the redshift and a type
        item_z = -1.0
        item_z_err = 1E12
        item_spec_flag = 0
        if n_obs_done:
            index = np.where(item_id == results_id)
            index = index[0]
            if (len(index)==1):
                print("{} {} OBS".format(i, index))
                item_z = spec_z[index]
                item_z_err = spec_z_err[index]
                item_spec_flag = spec_flag[index]
            else:
                raise NameError('There are more than two redshift determinations for the same object')

        n = numobs_needed(item_target_flag, n_obs_done, item_z, item_z_err, item_spec_flag)
        p = priority_needed(item_target_flag, item_spec_flag)

    return 
