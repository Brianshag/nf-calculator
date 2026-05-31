# This is a noise figure calculator script based off the Rohde/Schwarz noise figure document
#

import math
import sys

def NF(noiseSourceOff, noiseSourceOn, noiseSourceOff_DUT, noiseSourceOn_DUT, noiseSourceENR):


    # noiseSourceOff = float(sys.argv[1])    # need to typecast to float because arguments are in decimals and sys.argv takes arguments as strings by default
    # noiseSourceOn = float(sys.argv[2])
    # noiseSourceOff_DUT = float(sys.argv[3])
    # noiseSourceOn_DUT = float(sys.argv[4])
    # noiseSourceENR = float(sys.argv[5])

    # noiseSourceOff = -92 
    # noiseSourceOn = -87
    # noiseSourceOff_DUT = -103
    # noiseSourceOn_DUT = -92
    # noiseSourceENR = 15


    # Calibration Step. Only noise source connected to SA
    #noiseSourceENR = 15.13
    TsourceOff = 290
    TsourceOn = TsourceOff*(1+10**(noiseSourceENR/10))

    noiseSourceOff_dB = noiseSourceOff
    noiseSourceOff_Watts = (0.001)*10**((noiseSourceOff_dB)/10)

    noiseSourceOn_dB = noiseSourceOn
    noiseSourceOn_Watts = (0.001)*10**((noiseSourceOn_dB)/10)

    Y = noiseSourceOn_Watts / noiseSourceOff_Watts

    Tcalib = (TsourceOn-(Y*290))/(Y-1)


    NF = 10*math.log((Tcalib/290)+1, 10)

    # With DUT. Noise Source and DUT connected to SA
    noiseSourceOffDUT_dB = noiseSourceOff_DUT
    noiseSourceOffDUT_Watts = (0.001) * 10 ** ((noiseSourceOffDUT_dB) / 10)

    noiseSourceOnDUT_dB = noiseSourceOn_DUT
    noiseSourceOnDUT_Watts = (0.001) * 10 ** ((noiseSourceOnDUT_dB) / 10)

    Y_DUT = noiseSourceOnDUT_Watts / noiseSourceOffDUT_Watts

    T_DUT = (TsourceOn - (Y_DUT*290)) / (Y_DUT-1)

    NF_DUT = 10*math.log((T_DUT/290)+1, 10)

    # Final Calculations
    gain = (noiseSourceOnDUT_Watts - noiseSourceOffDUT_Watts) / (noiseSourceOn_Watts - noiseSourceOff_Watts)
    gain_dB = 10*math.log(gain, 10)
    T_DUT_final = (T_DUT - (Tcalib/gain))     # understand why i had to multiply by -1 here. like why am i getting a negative value in the first place. ****Because I was using lower values for NoiseSourceOff/ON_DUT than NoiseSource only, which isnt even physically possible
    print(T_DUT_final)
    NF_final = 10*math.log((T_DUT_final/290)+1, 10)

    #print(NF)
    #print(NF_DUT)
    #print(NF_final)
    return NF_final


