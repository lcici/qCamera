"""Status codes for the Sensicam. These were taken by conversion using
h2py and then writing to a dictionary from PCO_err.h. Additionally,
this implements the incredibly messy way of looking up error texts
found in PCO_errt.h. Why they chose to make things this complicated, I
really don't know.

"""

# Error code definitions
# ======================

SENSICAM_CODES = {
    0: "PCO_NOERROR",
    4095: "PCO_ERROR_CODE_MASK",
    61440: "PCO_ERROR_LAYER_MASK",
    16711680: "PCO_ERROR_DEVICE_MASK",
    520093696: "PCO_ERROR_RESERVED_MASK",
    536870912: "PCO_ERROR_IS_COMMON",
    1073741824: "PCO_ERROR_IS_WARNING",
    2147483648: "PCO_ERROR_IS_ERROR",
    4096: "PCO_ERROR_FIRMWARE",
    8192: "PCO_ERROR_DRIVER",
    12288: "PCO_ERROR_SDKDLL",
    16384: "PCO_ERROR_APPLICATION",
    65536: "SC2_ERROR_POWER_CPLD",
    131072: "SC2_ERROR_HEAD_UP",
    196608: "SC2_ERROR_MAIN_UP",
    262144: "SC2_ERROR_FWIRE_UP",
    327680: "SC2_ERROR_MAIN_FPGA",
    393216: "SC2_ERROR_HEAD_FPGA",
    458752: "SC2_ERROR_MAIN_BOARD",
    524288: "SC2_ERROR_HEAD_CPLD",
    589824: "SC2_ERROR_SENSOR",
    851968: "SC2_ERROR_POWER",
    917504: "SC2_ERROR_GIGE",
    983040: "SC2_ERROR_USB",
    1048576: "SC2_ERROR_BOOT_FPGA",
    1114112: "SC2_ERROR_BOOT_UP",
    655360: "SC2_ERROR_SDKDLL",
    2097152: "PCI540_ERROR_DRIVER",
    2162688: "PCI525_ERROR_DRIVER",
    3145728: "PCO_ERROR_DRIVER_FIREWIRE",
    3211264: "PCO_ERROR_DRIVER_USB",
    3276800: "PCO_ERROR_DRIVER_GIGE",
    3342336: "PCO_ERROR_DRIVER_CAMERALINK",
    720896: "SC2_ERROR_DRIVER",
    655360: "PCO_ERROR_PCO_SDKDLL",
    1114112: "PCO_ERROR_CONVERTDLL",
    1179648: "PCO_ERROR_FILEDLL",
    1245184: "PCO_ERROR_JAVANATIVEDLL",
    1048576: "PCO_ERROR_CAMWARE",
    2684354561: "PCO_ERROR_WRONGVALUE",
    2684354562: "PCO_ERROR_INVALIDHANDLE",
    2684354563: "PCO_ERROR_NOMEMORY",
    2684354564: "PCO_ERROR_NOFILE",
    2684354565: "PCO_ERROR_TIMEOUT",
    2684354566: "PCO_ERROR_BUFFERSIZE",
    2684354567: "PCO_ERROR_NOTINIT",
    2684354568: "PCO_ERROR_DISKFULL",
    2147491841: "PCO_ERROR_DRIVER_NOTINIT",
    2147491845: "PCO_ERROR_DRIVER_WRONGOS",
    2147491846: "PCO_ERROR_DRIVER_NODRIVER",
    2147491847: "PCO_ERROR_DRIVER_IOFAILURE",
    2147491848: "PCO_ERROR_DRIVER_CHECKSUMERROR",
    2147491849: "PCO_ERROR_DRIVER_INVMODE",
    2147491851: "PCO_ERROR_DRIVER_DEVICEBUSY",
    2147491852: "PCO_ERROR_DRIVER_DATAERROR",
    2147491853: "PCO_ERROR_DRIVER_NOFUNCTION",
    2147491854: "PCO_ERROR_DRIVER_KERNELMEMALLOCFAILED",
    2147491856: "PCO_ERROR_DRIVER_BUFFER_CANCELLED",
    2147491857: "PCO_ERROR_DRIVER_INBUFFER_SIZE",
    2147491858: "PCO_ERROR_DRIVER_OUTBUFFER_SIZE",
    2147491859: "PCO_ERROR_DRIVER_FUNCTION_NOT_SUPPORTED",
    2147491860: "PCO_ERROR_DRIVER_BUFFER_SYSTEMOFF",
    2147491872: "PCO_ERROR_DRIVER_SYSERR",
    2147491874: "PCO_ERROR_DRIVER_REGERR",
    2147491875: "PCO_ERROR_DRIVER_WRONGVERS",
    2147491876: "PCO_ERROR_DRIVER_FILE_READ_ERR",
    2147491877: "PCO_ERROR_DRIVER_FILE_WRITE_ERR",
    2147491878: "PCO_ERROR_DRIVER_LUT_MISMATCH",
    2147491879: "PCO_ERROR_DRIVER_FORMAT_NOT_SUPPORTED",
    2147491880: "PCO_ERROR_DRIVER_BUFFER_DMASIZE",
    2147491881: "PCO_ERROR_DRIVER_WRONG_ATMEL_FOUND",
    2147491882: "PCO_ERROR_DRIVER_WRONG_ATMEL_SIZE",
    2147491883: "PCO_ERROR_DRIVER_WRONG_ATMEL_DEVICE",
    2147491884: "PCO_ERROR_DRIVER_WRONG_BOARD",
    2147491885: "PCO_ERROR_DRIVER_READ_FLASH_FAILED",
    2147491886: "PCO_ERROR_DRIVER_HEAD_VERIFY_FAILED",
    2147491887: "PCO_ERROR_DRIVER_HEAD_BOARD_MISMATCH",
    2147491888: "PCO_ERROR_DRIVER_HEAD_LOST",
    2147491889: "PCO_ERROR_DRIVER_HEAD_POWER_DOWN",
    2147491890: "PCO_ERROR_DRIVER_CAMERA_BUSY",
    2147491891: "PCO_ERROR_DRIVER_BUFFERS_PENDING",
    2147495937: "PCO_ERROR_SDKDLL_NESTEDBUFFERSIZE",
    2147495938: "PCO_ERROR_SDKDLL_BUFFERSIZE",
    2147495939: "PCO_ERROR_SDKDLL_DIALOGNOTAVAILABLE",
    2147495940: "PCO_ERROR_SDKDLL_NOTAVAILABLE",
    2147495941: "PCO_ERROR_SDKDLL_SYSERR",
    2147495942: "PCO_ERROR_SDKDLL_BADMEMORY",
    2147495944: "PCO_ERROR_SDKDLL_BUFCNTEXHAUSTED",
    2147495945: "PCO_ERROR_SDKDLL_ALREADYOPENED",
    2147495946: "PCO_ERROR_SDKDLL_ERRORDESTROYWND",
    2147495947: "PCO_ERROR_SDKDLL_BUFFERNOTVALID",
    2147495948: "PCO_ERROR_SDKDLL_WRONGBUFFERNR",
    2147495949: "PCO_ERROR_SDKDLL_DLLNOTFOUND",
    2147495950: "PCO_ERROR_SDKDLL_BUFALREADYASSIGNED",
    2147495951: "PCO_ERROR_SDKDLL_EVENTALREADYASSIGNED",
    2147495952: "PCO_ERROR_SDKDLL_RECORDINGMUSTBEON",
    2147495953: "PCO_ERROR_SDKDLL_DLLNOTFOUND_DIVZERO",
    2147495954: "PCO_ERROR_SDKDLL_BUFFERALREADYQUEUED",
    2147495955: "PCO_ERROR_SDKDLL_BUFFERNOTQUEUED",
    3221237761: "PCO_WARNING_SDKDLL_BUFFER_STILL_ALLOKATED",
    3221237762: "PCO_WARNING_SDKDLL_NO_IMAGE_BOARD",
    3221237763: "PCO_WARNING_SDKDLL_COC_VALCHANGE",
    3221237764: "PCO_WARNING_SDKDLL_COC_STR_SHORT",
    2147500033: "PCO_ERROR_APPLICATION_PICTURETIMEOUT",
    2147500034: "PCO_ERROR_APPLICATION_SAVEFILE",
    2147500035: "PCO_ERROR_APPLICATION_FUNCTIONNOTFOUND",
    2147500036: "PCO_ERROR_APPLICATION_DLLNOTFOUND",
    2147500037: "PCO_ERROR_APPLICATION_WRONGBOARDNR",
    2147500038: "PCO_ERROR_APPLICATION_FUNCTIONNOTSUPPORTED",
    2147500039: "PCO_ERROR_APPLICATION_WRONGRES",
    2147500040: "PCO_ERROR_APPLICATION_DISKFULL",
    2147500041: "PCO_ERROR_APPLICATION_SET_VALUES",
    3221241857: "PCO_WARNING_APPLICATION_RECORDERFULL",
    2147487745: "PCO_ERROR_FIRMWARE_TELETIMEOUT",
    2147487746: "PCO_ERROR_FIRMWARE_WRONGCHECKSUM",
    2147487747: "PCO_ERROR_FIRMWARE_NOACK",
    2147487748: "PCO_ERROR_FIRMWARE_WRONGSIZEARR",
    2147487749: "PCO_ERROR_FIRMWARE_DATAINKONSISTENT",
    2147487750: "PCO_ERROR_FIRMWARE_UNKNOWN_COMMAND",
    2147487751: "PCO_ERROR_FIRMWARE_0x80001007",
    2147487752: "PCO_ERROR_FIRMWARE_INITFAILED",
    2147487753: "PCO_ERROR_FIRMWARE_CONFIGFAILED",
    2147487754: "PCO_ERROR_FIRMWARE_HIGH_TEMPERATURE",
    2147487755: "PCO_ERROR_FIRMWARE_VOLTAGEOUTOFRANGE",
    2147487756: "PCO_ERROR_FIRMWARE_I2CNORESPONSE",
    2147487757: "PCO_ERROR_FIRMWARE_CHECKSUMCODEFAILED",
    2147487758: "PCO_ERROR_FIRMWARE_ADDRESSOUTOFRANGE",
    2147487759: "PCO_ERROR_FIRMWARE_NODEVICEOPENED",
    2147487760: "PCO_ERROR_FIRMWARE_BUFFERTOSMALL",
    2147487761: "PCO_ERROR_FIRMWARE_TOMUCHDATA",
    2147487762: "PCO_ERROR_FIRMWARE_WRITEERROR",
    2147487763: "PCO_ERROR_FIRMWARE_READERROR",
    2147487764: "PCO_ERROR_FIRMWARE_NOTRENDERED",
    2147487765: "PCO_ERROR_FIRMWARE_NOHANDLEAVAILABLE",
    2147487766: "PCO_ERROR_FIRMWARE_DATAOUTOFRANGE",
    2147487767: "PCO_ERROR_FIRMWARE_NOTPOSSIBLE",
    2147487768: "PCO_ERROR_FIRMWARE_UNSUPPORTED_SDRAM",
    2147487769: "PCO_ERROR_FIRMWARE_DIFFERENT_SDRAMS",
    2147487770: "PCO_ERROR_FIRMWARE_ONLY_ONE_SDRAM",
    2147487771: "PCO_ERROR_FIRMWARE_NO_SDRAM_MOUNTED",
    2147487772: "PCO_ERROR_FIRMWARE_SEGMENTS_TOO_LARGE",
    2147487773: "PCO_ERROR_FIRMWARE_SEGMENT_OUT_OF_RANGE",
    2147487774: "PCO_ERROR_FIRMWARE_VALUE_OUT_OF_RANGE",
    2147487775: "PCO_ERROR_FIRMWARE_IMAGE_READ_NOT_POSSIBLE",
    2147487776: "PCO_ERROR_FIRMWARE_NOT_SUPPORTED",
    2147487777: "PCO_ERROR_FIRMWARE_ARM_NOT_SUCCESSFUL",
    2147487778: "PCO_ERROR_FIRMWARE_RECORD_MUST_BE_OFF",
    2147487781: "PCO_ERROR_FIRMWARE_SEGMENT_TOO_SMALL",
    2147487782: "PCO_ERROR_FIRMWARE_COC_BUFFER_TO_SMALL",
    2147487783: "PCO_ERROR_FIRMWARE_COC_DATAINKONSISTENT",
    2147487784: "PCO_ERROR_FIRMWARE_CORRECTION_DATA_INVALID",
    2147487785: "PCO_ERROR_FIRMWARE_CCDCAL_NOT_FINISHED",
    2147487792: "PCO_ERROR_FIRMWARE_COC_TRIGGER_INVALID",
    2147487793: "PCO_ERROR_FIRMWARE_COC_PIXELRATE_INVALID",
    2147487794: "PCO_ERROR_FIRMWARE_COC_POWERDOWN_INVALID",
    2147487795: "PCO_ERROR_FIRMWARE_COC_SENSORFORMAT_INVALID",
    2147487796: "PCO_ERROR_FIRMWARE_COC_ROI_BINNING_INVALID",
    2147487797: "PCO_ERROR_FIRMWARE_COC_ROI_DOUBLE_INVALID",
    2147487798: "PCO_ERROR_FIRMWARE_COC_MODE_INVALID",
    2147487799: "PCO_ERROR_FIRMWARE_COC_DELAY_INVALID",
    2147487800: "PCO_ERROR_FIRMWARE_COC_EXPOS_INVALID",
    2147487801: "PCO_ERROR_FIRMWARE_COC_TIMEBASE_INVALID",
    2147487808: "PCO_ERROR_FIRMWARE_COC_PERIOD_INVALID",
    2147487809: "PCO_ERROR_FIRMWARE_COC_MONITOR_INVALID",
    2147487824: "PCO_ERROR_FIRMWARE_UNKNOWN_DEVICE",
    2147487825: "PCO_ERROR_FIRMWARE_DEVICE_NOT_AVAIL",
    2147487826: "PCO_ERROR_FIRMWARE_DEVICE_IS_OPEN",
    2147487827: "PCO_ERROR_FIRMWARE_DEVICE_NOT_OPEN",
    2147487828: "PCO_ERROR_FIRMWARE_NO_DEVICE_RESPONSE",
    2147487829: "PCO_ERROR_FIRMWARE_WRONG_DEVICE_TYPE",
    2147487830: "PCO_ERROR_FIRMWARE_ERASE_FLASH_FAILED",
    2147487831: "PCO_ERROR_FIRMWARE_DEVICE_NOT_BLANK",
    2147487832: "PCO_ERROR_FIRMWARE_ADDRESS_OUT_OF_RANGE",
    2147487833: "PCO_ERROR_FIRMWARE_PROG_FLASH_FAILED",
    2147487834: "PCO_ERROR_FIRMWARE_PROG_EEPROM_FAILED",
    2147487835: "PCO_ERROR_FIRMWARE_READ_FLASH_FAILED",
    2147487836: "PCO_ERROR_FIRMWARE_READ_EEPROM_FAILED",
    2147487872: "PCO_ERROR_FIRMWARE_GIGE_COMMAND_IS_INVALID",
    2147487873: "PCO_ERROR_FIRMWARE_GIGE_UART_NOT_OPERATIONAL",
    2147487874: "PCO_ERROR_FIRMWARE_GIGE_ACCESS_DENIED",
    2147487875: "PCO_ERROR_FIRMWARE_GIGE_COMMAND_UNKNOWN",
    2147487876: "PCO_ERROR_FIRMWARE_GIGE_COMMAND_GROUP_UNKNOWN",
    2147487877: "PCO_ERROR_FIRMWARE_GIGE_INVALID_COMMAND_PARAMETERS",
    2147487878: "PCO_ERROR_FIRMWARE_GIGE_INTERNAL_ERROR",
    2147487879: "PCO_ERROR_FIRMWARE_GIGE_INTERFACE_BLOCKED",
    2147487880: "PCO_ERROR_FIRMWARE_GIGE_INVALID_SESSION",
    2147487881: "PCO_ERROR_FIRMWARE_GIGE_BAD_OFFSET",
    2147487882: "PCO_ERROR_FIRMWARE_GIGE_NV_WRITE_IN_PROGRESS",
    2147487883: "PCO_ERROR_FIRMWARE_GIGE_DOWNLOAD_BLOCK_LOST",
    2147487884: "PCO_ERROR_FIRMWARE_GIGE_DOWNLOAD_INVALID_LDR",
    2147487888: "PCO_ERROR_FIRMWARE_GIGE_DRIVER_IMG_PKT_LOST",
    2147487889: "PCO_ERROR_FIRMWARE_GIGE_BANDWIDTH_CONFLICT",
    2147488000: "PCO_ERROR_FIRMWARE_FLICAM_EXT_MOD_OUT_OF_RANGE",
    2147488001: "PCO_ERROR_FIRMWARE_FLICAM_SYNC_PLL_NOT_LOCKED",
    3221229569: "PCO_WARNING_FIRMWARE_FUNC_ALREADY_ON",
    3221229570: "PCO_WARNING_FIRMWARE_FUNC_ALREADY_OFF",
    3221229571: "PCO_WARNING_FIRMWARE_HIGH_TEMPERATURE",
    3221229572: "PCO_WARNING_FIRMWARE_OFFSET_NOT_LOCKED"
}

# Allow for using the text instead of the numeric codes as the
# dictionary keys.
_inverse = {v:k for k, v in SENSICAM_CODES.items()}
SENSICAM_CODES.update(_inverse)

# Error texts
# ===========

PCO_ERROR_COMMON_TXT = (
  "No error.",                                     # 0x00000000  PCO_NOERROR
  "Function call with wrong parameter.",           # 0xA0000001  PCO_ERROR_WRONGVALUE 
  "Handle is invalid.",                            # 0xA0000002  PCO_ERROR_INVALIDHANDLE 
  "No memory available.",                          # 0xA0000003  PCO_ERROR_NOMEMORY 

  "A file handle could not be opened.",            # 0xA0000004  PCO_ERROR_NOFILE 
  "Timeout in function.",                          # 0xA0000005  PCO_ERROR_TIMEOUT 
  "A buffer is to small.",                         # 0xA0000006  PCO_ERROR_BUFFERSIZE
  "The called module is not initialized.",         # 0xA0000007  PCO_ERROR_NOTINIT
  "Disk full.",                                    # 0xA0000008  PCO_ERROR_DISKFULL
  "",                                              # 0xA0000009
)

PCO_ERROR_DRIVER_TXT = (
  "No error.",                                     # 0x00002000  PCO_NOERROR
  "Initialization failed; no camera connected.",   # 0x80002001  PCO_ERROR_DRIVER_NOTINIT
  "",                                              # 0x80002002  
  "",                                              # 0x80002003  
  "",                                              # 0x80002004  
  "Wrong driver for this OS.",                     # 0x80002005  PCO_ERROR_DRIVER_WRONGOS
  "Open driver or driver class failed.",           # 0x80002006  PCO_ERROR_DRIVER_NODRIVER    
  "I/O operation failed.",                         # 0x80002007  PCO_ERROR_DRIVER_IOFAILURE    

  "Error in telegram checksum.",                   # 0x80002008  PCO_ERROR_DRIVER_CHECKSUMERROR
  "Invalid Camera mode.",                          # 0x80002009  PCO_ERROR_DRIVER_INVMODE
  "",                                              # 0x8000200A  
  "Device is hold by an other process.",           # 0x8000200B  PCO_ERROR_DRIVER_DEVICEBUSY

  "Error in reading or writing data to board.",    # 0x8000200C  PCO_ERROR_DRIVER_DATAERROR
  "No function specified.",                        # 0x8000200D  PCO_ERROR_DRIVER_NOFUNCTION
  "Kernel Memory allocation in driver failed.",    # 0x8000200E  PCO_ERROR_DRIVER_KERNELMEMALLOCFAILED
  "",                                              # 0x8000200F

  "Buffer was cancelled.",                         # 0x80002010  PCO_ERROR_DRIVER_BUFFER_CANCELLED
  "Input buffer too small for this IO-call.",      # 0x80002011  PCO_ERROR_DRIVER_INBUFFER_TO_SMALL
  "Output buffer too small for this IO-call.",     # 0x80002012  PCO_ERROR_DRIVER_OUTBUFFER_TO_SMALL
  "Driver IO-Function not supported.",             # 0x80002013  PCO_ERROR_DRIVER_FUNCTION_NOT_SUPPORTED
  "Buffer failed because device power off.",       # 0x80002014  PCO_ERROR_DRIVER_BUFFER_SYSTEMOFF

  "", "", "",                                      # 0x80002015 - 0x80002017
  "", "", "", "", "", "", "", "",                  # 0x80002018 - 0x8000201F

  "A call to a windows-function fails.",           # 0x80002020  PCO_ERROR_DRIVER_SYSERR
  "",                                              # 0x80002021  
  "Error in reading/writing to registry.",         # 0x80002022  PCO_ERROR_DRIVER_REGERR
  "Need newer called vxd or dll.",                 # 0x80002023  PCO_ERROR_DRIVER_WRONGVERS

  "Error while reading from file.",                # 0x80002024  PCO_ERROR_DRIVER_FILE_READ_ERR
  "Error while writing to file.",                  # 0x80002025  PCO_ERROR_DRIVER_FILE_WRITE_ERR
  "Camera and dll lut do not match.",              # 0x80002026  PCO_ERROR_DRIVER_LUT_MISMATCH
  "Grabber does not support transfer format.",     # 0x80002027  PCO_ERROR_DRIVER_FORMAT_NOT_SUPPORTED
  "DMA Error not enough data transferred.",        # 0x80002028  PCO_ERROR_DRIVER_BUFFER_DMASIZE

  "version verify failed wrong typ id.",           # 0x80002029  PCO_ERROR_DRIVER_WRONG_ATMEL_FOUND
  "version verify failed wrong size.",             # 0x8000202A  PCO_ERROR_DRIVER_WRONG_ATMEL_SIZE
  "version verify failed wrong device id.",        # 0x8000202B  PCO_ERROR_DRIVER_WRONG_ATMEL_DEVICE
  "firmware is not supported from this driver.",   # 0x8000202C  PCO_ERROR_DRIVER_WRONG_BOARD
  "board firmware verify failed.",                 # 0x8000202D  PCO_ERROR_DRIVER_READ_FLASH_FAILED
  "camera head is not recognized correctly.",      # 0x8000202E  PCO_ERROR_DRIVER_HEAD_VERIFY_FAILED
  "firmware does not support camera head.",        # 0x8000202F  PCO_ERROR_DRIVER_HEAD_BOARD_MISMATCH
  "camera head is not connected.",                 # 0x80002030  PCO_ERROR_DRIVER_HEAD_LOST
  "camera head power down.",                       # 0x80002031  PCO_ERROR_DRIVER_HEAD_POWER_DOWN
  "camera started."                                # 0x80002032  PCO_ERROR_DRIVER_CAMERA_BUSY
  "camera busy."                                   # 0x80002033  PCO_ERROR_DRIVER_BUFFERS_PENDING
)

PCO_ERROR_SDKDLL_TXT = (
  "No error.",                                     # 0x00000000  PCO_NOERROR
  "wSize of an embedded buffer is to small.",      # 0x80003001  PCO_ERROR_SDKDLL_NESTEDBUFFERSIZE   
  "wSize of a buffer is to small.",                # 0x80003002  PCO_ERROR_SDKDLL_BUFFERSIZE   
  "A dialog is not available.",                    # 0x80003003  PCO_ERROR_SDKDLL_DIALOGNOTAVAILABLE   
  "Option is not available.",                      # 0x80003004  PCO_ERROR_SDKDLL_NOTAVAILABLE   
  "A call to a windows-function fails.",           # 0x80003005  PCO_ERROR_SDKDLL_SYSERR
  "Memory area is invalid.",                       # 0x80003006  PCO_ERROR_SDKDLL_BADMEMORY   
  "",                                              # 0x80003007    
  "Number of available buffers is exhausted.",     # 0x80003008  PCO_ERROR_SDKDLL_BUFCNTEXHAUSTED   
  "Dialog is already open.",                       # 0x80003009  PCO_ERROR_SDKDLL_ALREADYOPENED   
  "Error while destroying dialog.",                # 0x8000300A  PCO_ERROR_SDKDLL_ERRORDESTROYWND   
  "A requested buffer is not available.",          # 0x8000300B  PCO_ERROR_SDKDLL_BUFFERNOTVALID  
  "The buffer nr is out of range.",                # 0x8000300C  PCO_ERROR_SDKDLL_WRONGBUFFERNR
  "A DLL could not be found.",                     # 0x8000300D  PCO_ERROR_SDKDLL_DLLNOTFOUND  
  "Buffer already assigned to another buffernr.",  # 0x8000300E  PCO_ERROR_SDKDLL_BUFALREADYASSIGNED
  "Event already assigned to another buffernr.",   # 0x8000300F  PCO_ERROR_SDKDLL_EVENTALREADYASSIGNED
  "Recording must be active.",                     # 0x80003010  PCO_ERROR_SDKDLL_RECORDINGMUSTBEON
  "A DLL could not be found, due to div by zero.", # 0x80003011  PCO_ERROR_SDKDLL_DLLNOTFOUND_DIVZERO
  "Buffer is already queued.",                     # 0x80003012  PCO_ERROR_SDKDLL_BUFFERALREADYQUEUED
  "Buffer is not queued.",                         # 0x80003013  PCO_ERROR_SDKDLL_BUFFERNOTQUEUED
)

PCO_ERROR_APPLICATION_TXT = (
  "No error.",                                     # 0x00000000  PCO_NOERROR
  "Error while waiting for a picture.",            # 0x80004001  PCO_ERROR_APPLICATION_PICTURETIMEOUT   
  "Error while saving file.",                      # 0x80004002  PCO_ERROR_APPLICATION_SAVEFILE 
  "A function inside a DLL could not be found.",   # 0x80004003  PCO_ERROR_APPLICATION_FUNCTIONNOTFOUND 

  "A DLL could not be found.",                     # 0x80004004  PCO_ERROR_APPLICATION_DLLNOTFOUND 
  "The board number is out of range.",             # 0x80004005  PCO_ERROR_APPLICATION_WRONGBOARDNR 
  "The decive does not support this function.",    # 0x80004006  PCO_ERROR_APPLICATION_FUNCTIONNOTSUPPORTED
  "Started Math with different resolution than reference.",# 0x80004007 PCO_ERROR_APPLICATION_WRONGRES
  "Disk full.",                                    # 0x80004008  PCO_ERROR_APPLICATION_DISKFULL
  "Error setting values to camera.",               # 0x80004009  PCO_ERROR_APPLICATION_SET_VALUES
)

PCO_ERROR_FIRMWARE_TXT = (
  "No error.",                                     # 0x00000000  PCO_NOERROR
  "Timeout in telegram.",                          # 0x80001001  PCO_ERROR_FIRMWARE_TELETIMEOUT   
  "Wrong checksum in telegram.",                   # 0x80001002  PCO_ERROR_FIRMWARE_WRONGCHECKSUM   
  "No acknowledge.",                               # 0x80001003  PCO_ERROR_FIRMWARE_NOACK   

  "Wrong size in array.",                          # 0x80001004  PCO_ERROR_FIRMWARE_WRONGSIZEARR   
  "Data is inkonsistent.",                         # 0x80001005  PCO_ERROR_FIRMWARE_DATAINKONSISTENT   
  "Unknown command telegram.",                     # 0x80001006  PCO_ERROR_FIRMWARE_UNKNOWN_COMMAND
  "",                                              # 0x80001007  

  "FPGA init failed.",                             # 0x80001008  PCO_ERROR_FIRMWARE_INITFAILED   
  "FPGA configuration failed.",                    # 0x80001009  PCO_ERROR_FIRMWARE_CONFIGFAILED   
  "High temperature.",                             # 0x8000100A  PCO_ERROR_FIRMWARE_HIGH_TEMPERATURE
  "Supply voltage out of range.",                  # 0x8000100B  PCO_ERROR_FIRMWARE_VOLTAGEOUTOFRANGE

  "No response from I2C Device.",                  # 0x8000100C  PCO_ERROR_FIRMWARE_I2CNORESPONSE  
  "Checksum in code area is wrong.",               # 0x8000100D  PCO_ERROR_FIRMWARE_CHECKSUMCODEFAILED  
  "An address is out of range.",                   # 0x8000100E  PCO_ERROR_FIRMWARE_ADDRESSOUTOFRANGE  
  "No device is open for update.",                 # 0x8000100F  PCO_ERROR_FIRMWARE_NODEVICEOPENED  

  "The delivered buffer is to small.",             # 0x80001010  PCO_ERROR_FIRMWARE_BUFFERTOSMALL   
  "To much data delivered to function.",           # 0x80001011  PCO_ERROR_FIRMWARE_TOMUCHDATA   
  "Error while writing to camera.",                # 0x80001012  PCO_ERROR_FIRMWARE_WRITEERROR   
  "Error while reading from camera.",              # 0x80001013  PCO_ERROR_FIRMWARE_READERROR   

  "Was not able to render graph.",                 # 0x80001014  PCO_ERROR_FIRMWARE_NOTRENDERED   
  "The handle is not known.",                      # 0x80001015  PCO_ERROR_FIRMWARE_NOHANDLEAVAILABLE   
  "Value is out of allowed range.",                # 0x80001016  PCO_ERROR_FIRMWARE_DATAOUTOFRANGE   
  "Desired function not possible.",                # 0x80001017  PCO_ERROR_FIRMWARE_NOTPOSSIBLE   

  "SDRAM type read from SPD unknown.",             # 0x80001018  PCO_ERROR_FIRMWARE_UNSUPPORTED_SDRAM   
  "Different SDRAM modules mounted.",              # 0x80001019  PCO_ERROR_FIRMWARE_DIFFERENT_SDRAMS   
  "For CMOS sensor two modules needed.",           # 0x8000101A  PCO_ERROR_FIRMWARE_ONLY_ONE_SDRAM   
  "No SDRAM mounted.",                             # 0x8000101B  PCO_ERROR_FIRMWARE_NO_SDRAM_MOUNTED   

  "Segment size is too large.",                    # 0x8000101C  PCO_ERROR_FIRMWARE_SEGMENTS_TOO_LARGE   
  "Segment is out of range.",                      # 0x8000101D  PCO_ERROR_FIRMWARE_SEGMENT_OUT_OF_RANGE   
  "Value is out of range.",                        # 0x8000101E  PCO_ERROR_FIRMWARE_VALUE_OUT_OF_RANGE    
  "Image read not possible.",                      # 0x8000101F  PCO_ERROR_FIRMWARE_IMAGE_READ_NOT_POSSIBLE   

  "Command/data not supported by this hardware.",  # 0x80001020  PCO_ERROR_FIRMWARE_NOT_SUPPORTED            
  "Starting record failed due not armed.",         # 0x80001021  PCO_ERROR_FIRMWARE_ARM_NOT_SUCCESSFUL       
  "Arm is not possible while record active.",      # 0x80001022  PCO_ERROR_FIRMWARE_RECORD_MUST_BE_OFF       
  "",                                              # 0x80001023             

  "",                                              # 0x80001024  
  "Segment too small for image.",                  # 0x80001025  PCO_ERROR_FIRMWARE_SEGMENT_TOO_SMALL        
  "COC built is too large for internal memory.",   # 0x80001026  PCO_ERROR_FIRMWARE_COC_BUFFER_TO_SMALL      
  "COC has invalid data at fix position.",         # 0x80001027  PCO_ERROR_FIRMWARE_COC_DATAINKONSISTENT     

  "Correction data not valid.",                    # 0x80001028  PCO_ERROR_FIRMWARE_CORRECTION_DATA_INVALID
  "CCD calibration not finished.",                 # 0x80001029  PCO_ERROR_FIRMWARE_CCDCAL_NOT_FINISHED       
  "",                                              # 0x8000102A  
  "",                                              # 0x8000102B  

  "",                                              # 0x8000102C        
  "",                                              # 0x8000102D  
  "",                                              # 0x8000102E  
  "",                                              # 0x8000102F  

  "COC Trigger setting invalid.",                  # 0x80001030  PCO_ERROR_FIRMWARE_COC_TRIGGER_INVALID 
  "COC PixelRate setting invalid.",                # 0x80001031  PCO_ERROR_FIRMWARE_COC_PIXELRATE_INVALID
  "COC Powerdown setting invalid.",                # 0x80001032  PCO_ERROR_FIRMWARE_COC_POWERDOWN_INVALID
  "COC Sensorformat setting invalid.",             # 0x80001033  PCO_ERROR_FIRMWARE_COC_SENSORFORMAT_INVALID
  "COC ROI to Binning setting invalid.",           # 0x80001034  PCO_ERROR_FIRMWARE_COC_ROI_BINNING_INVALID
  "COC ROI to Double setting invalid.",            # 0x80001035  PCO_ERROR_FIRMWARE_COC_ROI_DOUBLE_INVALID
  "COC Mode setting invalid.",                     # 0x80001036  PCO_ERROR_FIRMWARE_COC_MODE_INVALID
  "COC Delay setting invalid.",                    # 0x80001037  PCO_ERROR_FIRMWARE_COC_DELAY_INVALID
  "COC Exposure setting invalid.",                 # 0x80001038  PCO_ERROR_FIRMWARE_COC_EXPOS_INVALID
  "COC Timebase setting invalid.",                 # 0x80001039  PCO_ERROR_FIRMWARE_COC_TIMEBASE_INVALID
  "", "", "", "", "", "",                          # 0x8000103A - 0x8000103F

  "COC modulate period time invalid.",             # 0x80001040 PCO_ERROR_FIRMWARE_COC_PERIOD_INVALID
  "COC modulate monitor time invalid",             # 0x80001041 PCO_ERROR_FIRMWARE_COC_MONITOR_INVALID
  "", "", "", "", "", "",                          # 0x80001042 - 0x80001047
  "", "", "", "", "", "", "", "",                  # 0x80001048 - 0x8000104F

  "Attempt to open unknown device for update.",    # 0x80001050  PCO_ERROR_FIRMWARE_UNKNOWN_DEVICE     
  "Attempt to open device not available.",         # 0x80001051  PCO_ERROR_FIRMWARE_DEVICE_NOT_AVAIL   
  "This or other device is already open.",         # 0x80001052  PCO_ERROR_FIRMWARE_DEVICE_IS_OPEN
  "No device opened for update command.",          # 0x80001053  PCO_ERROR_FIRMWARE_DEVICE_NOT_OPEN

  "Device to open does not respond.",              # 0x80001054  PCO_ERROR_FIRMWARE_NO_DEVICE_RESPONSE 
  "Device to open is wrong device type.",          # 0x80001055  PCO_ERROR_FIRMWARE_WRONG_DEVICE_TYPE  
  "Erasing device flash/firmware failed.",         # 0x80001056  PCO_ERROR_FIRMWARE_ERASE_FLASH_FAILED 
  "Device to program is not blank.",               # 0x80001057  PCO_ERROR_FIRMWARE_DEVICE_NOT_BLANK   

  "Device address is out of range.",               # 0x80001058  PCO_ERROR_FIRMWARE_ADDRESS_OUT_OF_RANGE
  "Programming device flash/firmware failed.",     # 0x80001059  PCO_ERROR_FIRMWARE_PROG_FLASH_FAILED  
  "Programming device EEPROM failed.",             # 0x8000105A  PCO_ERROR_FIRMWARE_PROG_EEPROM_FAILED 
  "Reading device flash/firmware failed.",         # 0x8000105B  PCO_ERROR_FIRMWARE_READ_FLASH_FAILED  

  "Reading device EEPROM failed.",                 # 0x8000105C  PCO_ERROR_FIRMWARE_READ_EEPROM_FAILED 

  "", "", "",                                      # 0x8000105D - 0x8000105F
  "", "", "", "", "", "", "", "",                  # 0x80001060 - 0x80001067
  "", "", "", "", "", "", "", "",                  # 0x80001068 - 0x8000106F

  "", "", "", "", "", "", "", "",                  # 0x80001070 - 0x80001077
  "", "", "", "", "", "", "", "",                  # 0x80001078 - 0x8000107F

  "Command is invalid.",                           # 0x80001080  PCO_ERROR_FIRMWARE_GIGE_COMMAND_IS_INVALID
  "Camera UART not operational.",                  # 0x80001081  PCO_ERROR_FIRMWARE_GIGE_UART_NOT_OPERATIONAL         
  "Access denied. Debugging? See pco_err.h!",      # 0x80001082  PCO_ERROR_FIRMWARE_GIGE_ACCESS_DENIED                
  "Command unknown.",                              # 0x80001083  PCO_ERROR_FIRMWARE_GIGE_COMMAND_UNKNOWN              
  "Command group unknown.",                        # 0x80001084  PCO_ERROR_FIRMWARE_GIGE_COMMAND_GROUP_UNKNOWN        
  "Invalid command parameters.",                   # 0x80001085  PCO_ERROR_FIRMWARE_GIGE_INVALID_COMMAND_PARAMETERS   
  "Internal error.",                               # 0x80001086  PCO_ERROR_FIRMWARE_GIGE_INTERNAL_ERROR               
  "Interface blocked.",                            # 0x80001087  PCO_ERROR_FIRMWARE_GIGE_INTERFACE_BLOCKED            
  "Invalid session.",                              # 0x80001088  PCO_ERROR_FIRMWARE_GIGE_INVALID_SESSION              
  "Bad offset.",                                   # 0x80001089  PCO_ERROR_FIRMWARE_GIGE_BAD_OFFSET                   
  "NV write in progress.",                         # 0x8000108a  PCO_ERROR_FIRMWARE_GIGE_NV_WRITE_IN_PROGRESS         
  "Download block lost.",                          # 0x8000108b  PCO_ERROR_FIRMWARE_GIGE_DOWNLOAD_BLOCK_LOST          
  "Flash loader block invalid.",                   # 0x8000108c  PCO_ERROR_FIRMWARE_GIGE_DOWNLOAD_INVALID_LDR         
  "", "", "",                                      # 0x8000108d - 0x8000108F
  "Image packet lost.",                            # 0x80001090 PCO_ERROR_FIRMWARE_GIGE_DRIVER_IMG_PKT_LOST
  "GiGE Data bandwidth conflict.",		   # 0x80001091 PCO_ERROR_FIRMWARE_GIGE_BANDWIDTH_CONFLICT
  "", "", "", "", "",                              # 0x80001092 - 0x80001096
  "", "", "", "", "",                              # 0x80001097 - 0x8000109B
  "", "", "", "",                                  # 0x8000109C - 0x8000109F
  "External modulation frequency out of range.",   # 0x80001100 PCO_ERROR_FIRMWARE_FLICAM_EXT_MOD_OUT_OF_RANGE
  "Sync PLL not locked."                           # 0x80001101 PCO_ERROR_FIRMWARE_FLICAM_SYNC_PLL_NOT_LOCKED
)

