import fitsio
import numpy as np
from desitarget.targets import calc_priority
from mtl.observation import numobs_needed
from astropy.table import Table
import mtl
import yaml


def create_mtl(target_file, specresults_file, output_file):
    """
    Consolidates a Merged Target List file.
    """
    # input basic data
    # targets = fitsio.read(target_file, 1, upper=True)
    # specresults = fitsio.read(specresults_file, 1, upper=True)

    targets = Table.read(target_file, format='fits')
    specresults = Table.read(specresults_file, format='fits')

    n_points = len(targets['TARGETID'])
    n_spec = len(specresults['TARGETID'])
    print("{} objects in the input MTL file".format(n_points))
    print("{} objects in the zcat file".format(n_spec))

    # structure for output data
    type_table = [
        ('TARGETID', '>i8'), 
        ('BRICKNAME', '|S8'),
        ('RA', '>f4'), 
        ('DEC', '>f4'),
        ('NUMOBS', '>i4'), 
        ('PRIORITY', '>i4'),
        ('DESI_TARGET', '>i8'), 
        ('BGS_TARGET', '>i8'), 
        ('MWS_TARGET', '>i8')
    ]

    # loops over the targets looking for:
    # - number of observations performed on the target
    # - a definite targetflag


    num_obs = np.zeros(n_points, dtype='int')
    priority = np.zeros(n_points, dtype='int')
    required_numobs = targets['NUMOBS']
    iiobs = np.in1d(targets['TARGETID'], specresults['TARGETID'])

#    import IPython
#    IPython.embed()

    # update the priority, 
    # TEMPORARY: We don't take into account the targetstate. This has to be changed).
    priority = calc_priority(targets)
    
    id_results = 0
    for i in range(n_points):
        if iiobs[i]:
            n_obs_done = specresults['NUMOBS'][id_results]
            id_results = id_results + 1
        else:
            n_obs_done = 0
        num_obs[i] = numobs_needed(required_numobs[i], n_obs_done)

    data = np.ndarray(shape=(n_points), dtype=type_table)    
    data['TARGETID'] = targets['TARGETID']
    data['RA'] = targets['RA']
    data['DEC'] = targets['DEC']
    data['BRICKNAME'] = targets['BRICKNAME']
    data['DESI_TARGET'] = targets['DESI_TARGET']
    data['BGS_TARGET'] = targets['BGS_TARGET']
    data['MWS_TARGET'] = targets['MWS_TARGET']
    data['NUMOBS'] = num_obs
    data['PRIORITY'] = priority

    #- Create header to include versions, etc.
    hdr = fitsio.FITSHDR()
    hdr['DEPNAM00'] = 'mtl'
    hdr.add_record(dict(name='DEPVER00', value=mtl.__version__, comment='mtl.__version__'))
    hdr['DEPNAM01'] = 'mtl-git'
    hdr.add_record(dict(name='DEPVAL01', value=mtl.gitversion(), comment='git revision'))    

    fitsio.write(output_file, data, extname='MTL', header=hdr, clobber=True)    
    print('wrote {} items to MTL file'.format(n_points))

    #- TEMPORARY: fiberassign needs ASCII not FITS
    #- read it back in an write out an ascii table
    # t = Table.read(output_file, format='fits')
    #text_output = output_file.replace('.fits', '.txt')
    #assert text_output != output_file
    #t.write(text_output, format='ascii.commented_header')

    return 
