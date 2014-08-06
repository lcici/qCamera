from qcamera import AndorCamera, Sensicam, ThorlabsDCx, OpenCVCamera

# Valid camera types
CAM_TYPES = {
    'andor': AndorCamera,
    'sensicam': Sensicam,
    'thorlabs_dcx': ThorlabsDCx,
    'opencv' : OpenCVCamera
}

# Configuration file name
CONFIG_FILE = 'viewer.json'
