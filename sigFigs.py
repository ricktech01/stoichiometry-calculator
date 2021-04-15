import math
def hasWhole(sVal):
    if getWholeLen(sVal) > 0:
        return True
    else: return False
def getWholeLen(sVal):
    if int(getWhole(sVal)) == 0:
        return 0
    else:
        return len(getWhole(sVal))
def getDeci(sVal):
    temp = ''
    reached = False
    for i in sVal:
        if reached:
            temp += i
        if i == '.':
            reached = True
    return temp
def getDeciSig(sVal):
    if len(getWholeSig(sVal)) > 0:
        return getDeci(sVal)
    else:
        temp = getRaw(getDeci(sVal))
        out = ''
        reached = False
        for i in temp:
            if i != '0':
                reached = True
            if reached:
                out += i
        return out
def getWhole(sVal):
    temp = ''
    for i in sVal:
        if i == '.':
            break
        else:
            temp+= i
    return temp
def getWholeSig(sVal):
    if hasDeci(sVal):
        if getWhole(sVal) == '0':
            return ''
        else: return getWhole(sVal)
    else:
        temp = sVal[::-1]
        reached = False
        out = ''
        for i in temp:
            if i != '0':
                reached = True
            if reached:
                out += i
        return out[::-1]
def getDeciLen(sVal):
    if len(getDeci(sVal)) == 0:
        return 0
    elif int(getDeci(sVal)) == 0:
        return 0
    else: return len(getDeci(sVal))
def hasDeci(sVal):
    if  getDeciLen(sVal) > 0:
        return True
    else: return False
def getRaw(sVal):
    return sVal.replace(".", "")  
def getSigFigs(sVal):
    tMsrdNum = msrdNum
    temp = ''
    #A zero at the beginning of the decimal number is not significant.
    if hasWhole(sVal):
        if hasDeci(sVal):
            return len(getRaw(sVal))
def isDeci(sVal):
    if len(getWholeSig(sVal)) == 0 and len(getDeciSig(sVal)) > 0:
        return True
    else: return False
def isWhole(sVal):
    if len(getDeciSig(sVal)) == 0 and len(getWholeSig(sVal)) > 0:
        return True
    else: return False
def getDeciZ(sVal):
    temp = getDeci(sVal)
    out = ''
    reached = False
    for i in temp:
        if i != '0':
            reached = True
        if not reached:
            out += i
    return out
def getDeciNZ(sVal):
    temp = getDeci(sVal)
    out = ''
    reached = False
    for i in temp:
        if i != '0':
            reached = True
        if reached:
            out += i
    return out
def getWholeZ(sVal):
    temp = getWhole(sVal)[::-1]
    out = ''
    reached = False
    for i in temp:
        if i != '0':
            reached = True
        if not reached:
            out += i
    return out
def getSigs(sVal):
    out = 0
    #case 0, sVal is in scientific notation
    if 'e' in sVal:
        for i in sVal:
            if i == 'e':
                break
            elif i != '.':
                out += 1
        return out
    #case 1, sVal is a decimal number
    elif isDeci(sVal):
        out = len(getDeciSig(sVal))
        return out
    #case 2, sVal is a whole number
    elif isWhole(sVal):
        out = len(getWholeSig(sVal))
        return out
    #case 3, sVal is a whole number with a decemial fraction
    else:
        out = len(getRaw(sVal))
        return out
def signify(sVal, iSigs):
    out = ''
    #case 0, sVal is in scientific notation
    if 'e' in sVal:
        temp = str(format(float(sVal),'f'))
        out = signify(temp,iSigs)
    #case 1, sVal is a decimal number
    elif isDeci(sVal):
        temp = getDeciNZ(sVal)
        TDP = len(getDeciZ(sVal))+iSigs
        form = ("{0:."+ (str(TDP)) +"f}")
        out = form.format(float(sVal))
    #case 2, sVal is a whole number with no decimal numbers
    elif isWhole(sVal):
        NRP = iSigs - len(getWhole(sVal))
        #case 2.A, the zeroes greater than or equal to the negative rounding place
        if len(getWholeZ(sVal)) >= iSigs:
            form = ("{0:."+ (str(iSigs)) +"}")
            out = form.format(float(sVal))
        #case 2.B, the whole number is less than the significant figure
        elif len(getWhole(sVal)) < iSigs:
            TDP = iSigs - 1
            out =  ("%."+str(TDP)+"e") % (float(getWhole(sVal)))
        #case 2.C+ all other cases
        else:
            out = getWhole(str(round(float(sVal), NRP)))
    #case 3, sVal is a whole number with a decimal fraction
    else:
        #case 3.A the whole number is greater than or equal to the significant figures
        if len(getWhole(sVal))>= iSigs:
            NRP = iSigs - len(getWhole(sVal))
            #case 3.A.I, the zeroes greater than or equal to the negative rounding place
            if len(getWholeZ(sVal)) >= iSigs:
                form = ("{0:."+ (str(iSigs)) +"}")
                out = form.format(float(getWhole(sVal)))
            #case 3.A.II, the whole number is less than the significant figure
            elif len(getWhole(sVal)) < iSigs:
                TDP = iSigs - len(getWhole(sVal))
                form =  "%."+str(NRP -1)+"e" % (float(getWhole(sVal)))
            #case 3.A.III+ all other cases
            else:
                out = getWhole(str(round(float(sVal), NRP)))
        #case 3.B the whole number is less than the signficant figure
        else:
            TDP = iSigs - len(getWhole(sVal))
            form = ("{0:."+ (str(TDP)) +"f}")
            out = form.format(float(sVal))
    return str(out)
def add(sA, sB):
    sumAB = float(sA) + float(sB)
    if getDeciLen(sA) < getDeciLen(sB):
        form = '{0:.'+ str(len(getDeciSig(sA)))+'f}'
        return str(form.format(sumAB))
    else:
        form = '{0:.'+ str(len(getDeciSig(sB)))+'f}'
        return str(form.format(sumAB))
def subtract(sA, sB):
    difAB = float(sA) - float(sB)
    if getDeciLen(sA) < getDeciLen(sB):
        form = '{0:.'+ str(len(getDeciSig(sA)))+'f}'
        return str(form.format(difAB))
    else:
        form = '{0:.'+ str(len(getDeciSig(sB)))+'f}'
        return str(form.format(difAB))
def multiply(sA, sB):
    proAB = str(float(sA) * float(sB))
    if getSigs(sA) < getSigs(sB):
        return signify(proAB,getSigs(sA))
    else:
        return signify(proAB,getSigs(sB))
def divide(sA, sB):
    divAB = str(float(sA) / float(sB))
    if getSigs(sA) < getSigs(sB):
        return signify(divAB,getSigs(sA))
    else:
        return signify(divAB,getSigs(sB))
def eMultiply(sMsrd, fExa):
    prod = str(float(sMsrd) * fExa)
    return signify(prod,getSigs(sMsrd))
def eDivide(sMsrd, fExa):
    divi = str(float(sMsrd) * fExa)
    return signify(divi,getSigs(sMsrd))
