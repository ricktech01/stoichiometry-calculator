import csv
import sigFigs
def getMMass(sVal):
    temp = ''
    for i in sVal:
        if i == '(':
            break
        elif i != '[' and i != ']':
            temp += i
    return temp
def getInfo(sFileName = 'PeriodicTable.csv'):
    elements = [[],[]]
    ptF = open(sFileName)
    csPtF = csv.reader(ptF)
    for row in csPtF:
        elements[0].append(row[1])
        elements[1].append(getMMass(row[3]))
    ptF.close()
    return elements
elements = getInfo()
def symToMass(sSym,coef = 1):
    try:
        for i in range(0,len(elements[0])):
            if  sSym == elements[0][i]:
                return str(coef * float(elements[1][i]))
                break
        raise ValueError(sSym + ' Was not found in the elemental database')
    except ValueError as err:
        print(err) 
        return ('Err')
def interpForm(formula):
    temp =  formula
    syms =  []
    #getting each element in the formula
    t = ''
    for i in temp:
        if i.isupper():
            syms.append(t)
            t = i
        else:
            t += i
    if t != '':
        syms.append(t)
    del syms[0]
    molarWeight = ''
    for i in syms:
        tem = ''
        sstc = ''
        istc = 0
        for j in i:
            if j.isdigit():
                sstc += j 
            else:
                tem += j
        if len(sstc) == 0:
            sstc = '1'
        istc = int(sstc)
        try:
            mw = symToMass(tem, istc)
            if mw == 'Err':
                raise ValueError()
            if molarWeight == '':
                molarWeight = mw
            else:
                molarWeight = sigFigs.add(molarWeight,mw)
        except ValueError:
            return 'Err'
    return molarWeight
def getStCoe(sFormula):
    sStCoe = ''
    #getting the stoechiometric coefficient
    for i in range(0,len(sFormula)):
        if sFormula[i].isdigit():
            sStCoe += sFormula[i]
        else:
            break
    if len(sStCoe) == 0:
        sStCoe = '1'
    return sStCoe
def cMolarWeight():
    CF = input('Enter the chemical formula: ')
    if hasElement(CF) == False:
        print('Invalid Input')
        return 'Err'
    temp =  CF
    sStCoe = getStCoe(CF)
    #getting the stoechiometric coefficient
    if len(sStCoe) > 1:
        temp = CF[len(sStCoe):len(CF)]
    MW = str(interpForm(temp))
    if MW == 'Err':
        return 'Err'
    print('The molar weight of', CF,'is', sigFigs.eMultiply(MW,int(sStCoe)),'amu')
    return sigFigs.eMultiply(MW,int(sStCoe))
def cProductYeild():
    CFR = input('Enter the formula of the reactant (with the stoichiometric coefficient): ')
    if hasElement(CFR) == False:
        print('Invalid Input')
        return 'Err'
    #getting the molar weight and the stoichiometric coefficient of the reactant
    tempRF =  CFR
    sStCoeR = getStCoe(CFR)
    if len(sStCoeR) > 1:
        sStCoeR = CFR[len(sStCoeR):len(CFR)]
    MWR = str(interpForm(tempRF))
    if MWR == 'Err':
        return 'Err'
    MR = input('Enter the mass of the reactant (in grams): ')
    if hasChar(MR) == True:
        print('Invalid Input')
        return 'Err'
    elif '-' in MR:
        print('Cannot compute negative numbers')
        return 'Err'
    molR = sigFigs.divide(MR,MWR)
    CFP = input('Enter the formula of the product (with the stoichiometric coefficient): ')
    if hasElement(CFP) == False:
        print('Invalid Input')
        return 'Err'
    #getting the molar weight and the stoichiometric coefficient of the product
    tempPF =  CFP
    sStCoeP = getStCoe(CFP)
    if len(sStCoeP) > 1:
        sStCoeP = CFP[len(sStCoeP):len(CFP)]
    MWP = str(interpForm(tempPF))
    if MWP == 'Err':
        return 'Err'
    molP = sigFigs.eMultiply(molR,float(sStCoeP)/float(sStCoeR))
    print(molR,'moles', CFR,'*',float(sStCoeP),'/',float(sStCoeR),'=',molP,'moles',CFP)
    MP = sigFigs.multiply(molP,MWP)
    print('Theoretical yeild is', molP,'moles',tempPF, 'or', MP,'g',tempPF)
    CPY = input('Would you like to calculate the percent Yield?').lower()
    if CPY == 'yes':
        EY = input('Enter the mass of the product (in grams): ')
        PY = sigFigs.eMultiply(sigFigs.divide(EY,MP),100)
        print('The percent yield is',PY+'%')
        
    else:
        return molP
#Error trapping functions
def hasElement(sVal):
    for i in sVal:
        if i.isalpha():
            if i.isupper():
                return True
    return False
def hasChar(sVal):
    for i in sVal:
        if i.isalpha():
            return True
    return False
def prompt():
    print('Enter the number of the desired calculation:')
    print('1 - Molar Weight Calculator')
    print('2 - Theoretical Yeild Calculator')
    ans = input('Calculation #: ')
    if ans == '1':
        cMolarWeight()
    elif ans == '2':
        cProductYeild()
    else:
        print('There are no calculations that correspond with your input')
#Run from here
p = 'yes'
while p in ('yes','y','ok','i do'):
    p = ''
    prompt()
    p = input('Would you like to make another calculation? ').lower()
