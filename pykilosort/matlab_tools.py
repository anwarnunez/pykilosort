import os
from scipy.io import loadmat

from pykilosort import Bunch


def export_chanmap_mat2npy(chanmap_matfile):
    '''Convert a MATLAB channel map file to a series of NPY files.

    Parameters
    ----------
    chanmap_matfile (str): MATLAB file containing probe information

    Returns
    -------
    chanmap_npyfiles (list): NPY files saved
    '''
    # read MAT file and extract relevant info
    parent_dir = os.path.split(chanmap_matfile)[0]
    probe = import_matlab_chanmap(chanmap_matfile)
    probe_info = probe.keys()

    # iterate through contents and save as NPY
    chanmap_npyfiles = []
    for content in probe_info:
        npyout = os.path.join(parent_dir, '%s.npy'%content)
        np.save(npyout, probe[content])
        chanmap_npyfiles.append(npyout)

    return chanmap_npyfiles


def import_matlab_chanmap(chanmap_matfile):
    '''Load a MATLAB channel map file.

    Parameters
    ----------
    chanmap_matfile (str): MATLAB file containing probe information

    Returns
    -------
    probe (pykilosort.Bunch):
        Object containing probe information
    '''
    # read MAT file and extract relevant info
    mat = loadmat(chanmap_matfile)
    chanmap_zeroidx = mat['chanMap'].squeeze().astype(np.int64) - 1 # 0-indexed
    xcoords = mat['xcoords'].squeeze().astype(np.float32)
    ycoords = mat['ycoords'].squeeze().astype(np.float32)

    # Create `probe` object
    probe = Bunch()
    probe.chanMap = chanmap_zeroidx
    probe.xc = xcoords
    probe.yc = ycoords
    probe.NchanTOT = len(chanmap_zeroidx)
    return probe


def test_matlab_import():
    '''
    '''
    import urllib.request
    from io import BytesIO
    url = 'https://github.com/MouseLand/Kilosort2/raw/master/configFiles/neuropixPhase3B2_kilosortChanMap.mat'
    response = urllib.request.urlopen(url)
    fl = BytesIO(response.read())
    mat = loadmat(fl)

    probe = import_matlab_chanmap(fl)
    assert 'chanMap' in probe
    assert 'xc' in probe
    assert 'yc' in probe
    assert 'NchanTOT' in probe
    assert np.allclose(mat['chanMap'].squeeze() - 1, probe['chanMap'])
