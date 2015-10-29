import numpy as np
import fitsio
import mtl
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
    numobs_used = np.zeros(n_targets, dtype='int')
    zwarn_flag = np.zeros(n_targets, dtype='int64')
    object_type = np.chararray(n_targets, itemsize=20)
    object_subtype = np.chararray(n_targets, itemsize=20)
    object_type[:] = "NONE"
    object_subtype[:] = "NONE"

    type_table = [
        ('TARGETID', '>i4'), 
        ('BRICKNAME', '|S8'),
        ('TARGETFLAG', '>i8'), 
        ('Z', '>f4'), 
        ('ZERR', '>f4'),
        ('ZWARN', '>i8'), 
        ('NUMOBSUSED', '>i4'),
        ('TYPE', '|S20'),
        ('SUBTYPE', '|S20')
    ]

    data = np.ndarray(shape=(n_targets), dtype=type_table)
    data['TARGETID'] = targets['TARGETID']
    data['BRICKNAME'] = targets['BRICKNAME']
    data['TARGETFLAG'] = target_flag
    data['Z'] = redshift
    data['ZERR'] = redshift_error
    data['NUMOBSUSED'] = numobs_used
    data['TYPE'] = object_type
    data['SUBTYPE'] = object_subtype
    data['ZWARN'] = zwarn_flag

    #- Create header to include versions, etc.
    hdr = fitsio.FITSHDR()
    hdr['DEPNAM00'] = 'mtl-specresults'
    hdr.add_record(dict(name='DEPVER00', value=mtl.__version__, comment='mtl.__version__'))
    hdr['DEPNAM01'] = 'mtl-git'
    hdr.add_record(dict(name='DEPVAL01', value=mtl.gitversion(), comment='git revision'))
    
    fitsio.write(output_file, data, extname='SPECRES', header=hdr, clobber=True)    

    return 

