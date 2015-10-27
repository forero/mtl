import numpy as np
import fitsio
import mtl
def new_observations_file(target_file, output_file):
    """
    Initializes the file summarizing observational bookkeeping.
    This file lists the fiber and tile for which a target
    had a spectrum taken.
    """

    targets = fitsio.read(target_file, 1, upper=True)

    target_id = targets['TARGETID']
    n_targets = len(target_id)
    tile_id = -1 * np.ones(n_targets, dtype='int')
    fiber_id = -1 * np.ones(n_targets, dtype='int')

    type_table = [
        ('TARGETID', '>i4'), 
        ('BRICKNAME', '|S8'),
        ('TILEID', '>i4'), 
        ('FIBERID', '>i4')
    ]
    data = np.ndarray(shape=(n_targets), dtype=type_table)
    data['TARGETID'] = targets['TARGETID']
    data['BRICKNAME'] = targets['BRICKNAME']
    data['TILEID'] = tile_id
    data['FIBERID'] = fiber_id

    #- Create header to include versions, etc.
    hdr = fitsio.FITSHDR()
    hdr['DEPNAM00'] = 'mtl-observations'
    hdr.add_record(dict(name='DEPVER00', value=mtl.__version__, comment='mtl.__version__'))
    hdr['DEPNAM01'] = 'mtl-git'
    hdr.add_record(dict(name='DEPVAL01', value=mtl.gitversion(), comment='git revision'))
    

    fitsio.write(output_file, data, extname='OBSERVATIONS', header=hdr, clobber=True)    

    return 

def new_specresults_file(target_file, output_file):
    """
    Initializes the file summarizing spectral pipeline results.
    """

    targets = fitsio.read(target_file, 1, upper=True)
    target_id = targets['TARGETID']
    n_targets = len(target_id)
    tile_id = np.zeros(n_targets)
    fiber_id = np.zeros(n_targets)
    redshift = -1.0*np.ones(n_targets)
    redshift_error = 1E4*np.ones(n_targets)
    target_flag = np.zeros(n_targets, dtype='int64')

    type_table = [
        ('TARGETID', '>i4'), 
        ('BRICKNAME', '|S8'),
        ('TARGETFLAG', '>i8'), 
        ('Z', '>f4'), 
        ('ZERR', '>f4')
    ]

    data = np.ndarray(shape=(n_targets), dtype=type_table)
    data['TARGETID'] = targets['TARGETID']
    data['BRICKNAME'] = targets['BRICKNAME']
    data['TARGETFLAG'] = target_flag
    data['Z'] = redshift
    data['ZERR'] = redshift_error

    #- Create header to include versions, etc.
    hdr = fitsio.FITSHDR()
    hdr['DEPNAM00'] = 'mtl-specresults'
    hdr.add_record(dict(name='DEPVER00', value=mtl.__version__, comment='mtl.__version__'))
    hdr['DEPNAM01'] = 'mtl-git'
    hdr.add_record(dict(name='DEPVAL01', value=mtl.gitversion(), comment='git revision'))
    

    fitsio.write(output_file, data, extname='SPECRES', header=hdr, clobber=True)    

    return 

