#!/usr/bin/env python

from WxMAP2 import *
MF=MFutils()

def parseOutput(cards):

    ocards=[]
    cards=cards.split('\n')
    for card in cards:
        if(mf.find(card,'SSSHHH')): ocards.append(card)

    return(ocards)

def getModelOpt(basin,year,veriStat,phrOpt,veriOpt,addNavy=0,override=0):

    """
this is for the super bt project... consistent aids 1979-2021    
"""
    filtOpt='z0012'
    if(phrOpt == 6):
        filtOpt='z0618'

    yearEnd=2024
    yearClip=2017
    yearClp5=2019
    
    # -- renamed clp3/5 -> clip in nhc basins 2017-2021
    
    if(veriStat == 'pe' or veriStat == 'fe' or veriStat == 'pod'):
            
        if(year <= yearEnd):
            modelOptAD='ofcl,tera5,clip,avno' 
            if(phrOpt == ''):
                modelOpt='ofcl,tera5,clip' 
            elif(phrOpt == 0):
                modelOpt='ofcl00,tera500,clip00' 
            elif(phrOpt == 6):
                modelOpt='ofcl,tera506,clip,avno06' 
            
            modelOptHomo='ofcl,tera5'
                
                
        else:
            print 'year <= ',yearEnd,' for BT++ project'
            sys.exit()
        
        
        if(basin == 'w' or basin == 'h'): 
            
            modelOptAD='jtwc,tera5,clip,avno'

            if(year <= yearEnd):
                if(phrOpt == ''):   
                    modelOpt='jtwc,tera5,clip,avno'
                elif(phrOpt == 0):
                    modelOpt='jtwc00,tera500,clip00,avno00'
                elif(phrOpt == 6):
                    modelOpt='jtwc,tera506,clip,avno06'
                    
                modelOptHomo='jtwc,tera5'
                    
            else:
                print 'year <= ',yearEnd,' for BT++ project in WPAC'
                sys.exit()
                
        

    elif(veriStat == 'vbias'):

        if(year <= yearEnd and phrOpt == ''):         modelOpt='ofcl,tera5' 
        else:
            print 'year <= ',yearEnd,' for BT++ project'
            sys.exit()


        if(basin == 'w' or basin == 'h'): 
            
            if(year <= yearEnd  and phrOpt == ''):       modelOpt='jtwc,tera5'
            else:
                print 'year <= ',yearEnd,' for BT++ project in WPAC'
                sys.exit()

                
                
    if(veriOpt == '-H'):
        if(phrOpt == ''):  veriLabel='raw-hetero'
        elif(phrOpt == 0): veriLabel='phr00-raw-hetero'
        elif(phrOpt == 6): veriLabel='phr06-raw-hetero'
        
    if(veriOpt == ''):
        veriLabel='raw-homo'
        if(phrOpt == ''):  veriLabel='raw-homo'
        elif(phrOpt == 0): veriLabel='phr00-raw-homo'
        elif(phrOpt == 6): veriLabel='phr06-raw-homo'

        modelOpt=modelOptHomo
        
    setOpt='ncep'
    if(addNavy): setOpt='navy'

    if(override):
        overrideOpt='-O'
        overrideOptAD='-O1'
    else:
        overrideOpt=''
        overrideOptAD=''
        
    return(modelOpt,filtOpt,overrideOpt,veriLabel,setOpt,overrideOptAD,modelOptAD)


class MyearVd2aCmdLine(CmdLine):

    def __init__(self,argv=sys.argv):

        if(argv == None): argv=sys.argv
        
        self.argv=argv
        self.argopts={
            #1:['source',  '''source1[,source2,...,sourceN]'''],
            }

        self.options={
            'verb':                ['V',0,1,'verb is verbose'],
            'basinOpt':            ['b:','n','a','basins'],
            'phrOpt':              ['h:',None,'a',"""[no BC] | 0 - 0-h BC | 6 - 6-h BC | all - both 0/6 h"""],
            'veriOpt':             ['H:',-1,'i',"""" [-1 heterogeneous] | 1 for homogeneous |  0: both """],
            'veriStatOpt':         ['s:','pe','a',"""['pe'] for position error | 'pod' | gainxyfe """],
            'yearOpt':             ['y:','2017.2017','a',"""byear.eyear for a range of years"""],
            'doad2':               ['A',0,1,"""make ad2 decks"""],
            'addNavy':             ['n',0,1,"""make ad2 decks"""],
            'ropt':                ['N','norun','norun',' norun is norun'],
            'doIt':                ['X',0,1,' doIt'],
            'override':            ['O',0,1,'override'],
            }

        self.defaults={
            }

        self.purpose='''
        purpose -- multi-year ad2/vd2  processing'''

        self.examples='''
%s -y 2015[.2017] '''

CL=MyearVd2aCmdLine(argv=sys.argv)
CL.CmdLine()
exec(CL.estr)
if(verb): print CL.estr

dsbdirOptAD=''
dsbdirOptVD=''
localDSs='./DSs-local'
if(os.path.exists(localDSs)):
    print 'llllllllllll--------lllllllllll',localDSs
    dsbdir=localDSs
    dsbdirOptAD="-D %s"%(dsbdir)
    dsbdirOptVD="-D %s"%(dsbdir)
        
vd2apycmd='w2-tc-dss-vd2-anl.py'
ad2pycmd='w2-tc-dss-ad2.py'

allBasins=['h','w','e','l']

# -- basins
#
basins=basinOpt.split(',')
if(basinOpt == 'n'): basins=allBasins

# -- years
#
if(mf.find(yearOpt,'.')): 
    tt=yearOpt.split('.')
    if(len(tt) == 2):
        byear=int(tt[0])    
        eyear=int(tt[1])    
    else:
        print 'EEE bad yearOpt, must be byear.eyear of byear'
        sys.exit()
else:
    try:
        byear=eyear=int(yearOpt)
    except:
        print 'EEE bad yearOpt -- for single year must be YYYY'
        sys.exit()
years=range(byear,eyear+1)



if(veriOpt == 1):
    veriOptsAll=['']
elif(veriOpt == -1):
    veriOptsAll=['-H']
else:
    veriOptsAll=['','-H']
    
if(phrOpt == None or (phrOpt != None and phrOpt == 'raw')):
    phrOptsAll=['']
elif(phrOpt != None and (phrOpt == '0' or phrOpt == '6')):
    phrOptsAll=[int(phrOpt)]
elif(phrOpt != None and phrOpt == 'all'):
    phrOptsAll=['',0,6]
    
if(veriStatOpt != None):
    veriStatsAll=[veriStatOpt]
else:
    veriStatsAll=['pe','pod','vbias']

if(doIt): ropt=''

ddir="./datTCstats"


dovd2a=1

if(doad2):  
    veriOptsAll=['']
    #phrOptsAll=['']
    veriStats=['pe']
    dovd2a=0
else:
    veriStats=veriStatsAll
    
MF.sTimer('all')

for veriStat in veriStats:
    
    veriOpts=veriOptsAll
    phrOpts=phrOptsAll
    
    if(veriStat == 'pod'):
        veriOpts=['-H']
        phrOpts=['']

    for veriOpt in veriOpts:
        
        cveriOpt='hetero'
        if(veriOpt == ''): cveriOpt='homo'
        
        for phrOpt in phrOpts:

            csetOpt='ncep'
            if(addNavy): csetOpt='navy'
            
            cphrOpt='raw'
            if(phrOpt != ''): cphrOpt="%02d"%(int(phrOpt))
            
            overiStat=veriStat
            if(veriStat == 'pe'): overiStat='fe'
                
            MF.sTimer("VVV-%s-%s-%s-%s"%(overiStat,cveriOpt,cphrOpt,csetOpt))
            
            for basin in basins:
                
                for year in years:
                    
                    rc=getModelOpt(basin,year,veriStat,phrOpt,veriOpt,
                                   addNavy=addNavy,override=override)
                    (modelOpt,filtOpt,overrideOpt,veriLabel,setOpt,overrideOptAD,modelOptAD)=rc

                    if(ropt != 'norun'): MF.sTimer("%s-%s-%s-%s-%s-%s"%(veriStat,veriOpt,phrOpt,setOpt,basin,year))
                    
                    cyear=str(year)[-2:]
                    ofile="%s/stats.%s-%s.%s.%s.%s.txt"%(ddir,basin,cyear,veriStat,veriLabel,setOpt)
                    basinOpt='%s.%s'%(basin,cyear)
                    if(basin == 'e'):
                        basinOpt='c.%s,%s.%s'%(cyear,basin,cyear)
            
                    if(doad2):
                        # -- add clp? for nhc >= 2017
                        #
                        modelOptADFinal=modelOptAD
                        if(year >= 2017 and (basin == 'e' or basin == 'l')):
                            modelOptADFinal=modelOptAD+',clp3,clp5'
                        elif(year <= 1989 and basin == 'h'):
                            modelOptADFinal=modelOptAD+',clim,hpac'
                            
                            
                        phrs=phrOptsAll
                        ad2sourcOpt=''
                        for phr in phrs:
                            ad2sourcOpt='jt,tmtrkN,mftrkN,ncep'
                            if(year <= 2021): ad2sourcOpt='jt,tmtrkN,mftrkN'
                            if(phr == ''): phropt='' 
                            if(phr == 0): phropt='-h 0'
                            if(phr == 6): phropt='-h 6'
                            ad2cmd="%s %s -O1 -S %s -T %s %s %s %s"%\
                                (ad2pycmd,ad2sourcOpt,basinOpt,modelOptADFinal,phropt,overrideOptAD,dsbdirOptAD)
                            MF.runcmd(ad2cmd,ropt)
                        # -- don't do vd2    
                        continue
                            
                    if(dovd2a):
                        vd2acmd="%s -S %s -T %s -f %s %s -p %s %s %s"%\
                            (vd2apycmd,basinOpt,modelOpt,filtOpt,veriOpt,veriStat,overrideOpt,dsbdirOptVD)
                        cards=MF.runcmdLogOutput(vd2acmd,ropt=ropt)
                        if(ropt == ''):
                            ocards=parseOutput(cards)
                            rc=MF.WriteList2File(ocards,ofile,verb=1)
                            
                    if(ropt != 'norun'): MF.dTimer("%s-%s-%s-%s-%s-%s"%(veriStat,veriOpt,phrOpt,setOpt,basin,year))
                    
            MF.dTimer("VVV-%s-%s-%s-%s"%(overiStat,cveriOpt,cphrOpt,csetOpt))
                        

MF.dTimer('all')
