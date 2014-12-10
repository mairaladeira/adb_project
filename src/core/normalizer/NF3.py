from src.core.normalizer.NF import NF
from src.core.normalizer.NF2 import NF2

__author__ = 'Maira'


class NF3(NF):
    def __init__(self):
        super()
        self.nf2 = NF2

def is3NF(fdsLHS,fdsRHS):

#for 1st functional dependancy it will give TRUE as it is in 3NF A->B   A is a PK
#for 2nd functional dependancy it will give FALSE as it is not in 3NF B->C and B is not PK   (these both are for same table)


            #fdsLHS ='a'
            #fdsRHS ='b'
            #fdsLHS ='b'
            #fdsRHS ={'c','d'}
            #fdsRHS ={'c','d'}

            candidateKeys={'a','e','f'}
            thirdNFviolaes = False
            #fdsLHS=functional_dependencies.getLHS_dep();
            #fdsRHS=functional_dependencies.getRHS_dep();

            lhsIsSuperkey=False

            try:
                for e in candidateKeys:
                        if e==fdsLHS:
                            lhsIsSuperkey= True

                if lhsIsSuperkey!=True:
                    for r in fdsRHS:
                        if isKeyAttribute(r)==False:
                            thirdNFviolaes=True


            except Exception as ex:
                print('violates_3NF excepion')
                print(ex)

            return thirdNFviolaes

def isKeyAttribute(atribute):
    isKeyAttr = False
    candidateKeys={'a'}

    for e in candidateKeys:
            if e==atribute:
                isKeyAttr=True

    #print(isKeyAttr)

    return isKeyAttr


print('3rd NF Voilation for B->C,D:  ',is3NF('b',{'c','d'}));   #3NF violated
print('3rd NF Voilation for A->B:    ',is3NF('a',{'b'}));   #3NF not violated


