# -- import in sBTvars sbtLocal import *
#

from sBTvars import *

# -- MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

def ndayyr(yyyy):
    nd=365
    if (int(yyyy)%4 == 0): nd=366
    return(nd)

def ndaymo(yyyymm):
    yyyy=string.atoi(yyyymm[0:4])
    mm=string.atoi(yyyymm[4:6])

    leap=0
    if (yyyy%4 == 0): leap=1

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): leap=0

    if(leap):
        return(mdayleap[mm])
    else:
        return(mday[mm])

def TimeZoneName():

    import time
    tz=time.tzname
    tz=tz[time.daylight]
    return(tz)


def Dtg2JulianDay(dtg):

    import time
    year=int(str(dtg)[0:4])
    month=int(str(dtg)[4:6])
    day=int(str(dtg)[6:8])

    t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    jday=time.gmtime(t)[7]
    jday="%03d"%(int(jday))
    return (jday)

def YearJulianDay2YMD(year,jday):

    from datetime import date,timedelta
    ymd=date(int(str(year)),1,1) + timedelta(int(str(jday))-1)
    ymd=ymd.strftime("%Y%m%d")
    return(ymd)



def dtg6(opt="default"):

    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/6)*6)
    mn="%02d" % t[4]
    sc="%02d" % t[5]

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)

def dtg(opt="default"):

    import time
    
    from datetime import datetime
    from dateutil import tz
    
    tzname=" %s "%(TimeZoneName())
    
    from_zone = tz.gettz('UTC')
    to_zone   = tz.gettz('America/Denver')

    if (opt == "curtime" or opt == "curtimeonly" or opt == 'cur_hms'):
        t=time.localtime(time.time())
    else:
        t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/6)*6)
    phr=int(t[3])%6
    mn="%02d" % t[4]
    sc="%02d" % t[5]
    fphr=float(phr)*1.0 + float(mn)/60.0;

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "phr":
        dtg="%4.2f"%(fphr)
    elif opt == "fphr":
        dtg=fphr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif opt == "cur.hm":
        dtg=yr + mo + dy + " " + hr + ":" + mn
    elif opt == "dtg.phm":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn
    elif opt == "dtg.phms":
        cphr="%02d"%(phr)
        dtg=yr + mo + dy + fhr + " " + cphr + ":" + mn + ":" + sc
    elif opt == "dtgmn":
        dtg=yr + mo + dy +  hr + mn
    elif opt == "dtg_mn":
        dtg=yr + mo + dy +  hr + '_%s'%(mn)
    elif opt == "dtg_ms":
        dtg=yr + mo + dy +  hr + "_%s_%s"%(mn,sc)
    elif opt == "dtg_hms":
        dtg=yr + mo + dy + "_%s_%s_%s"%(hr,mn,sc)
    elif opt == "cur_hms":
        dtg="  ---> CurDT: " + yr + mo + dy + " %s:%s:%s <---"%(hr,mn,sc)
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif opt == "dtg.hms":
        dtg=yr + mo + dy +  " " + hr + ":" + mn + ":" + sc
    elif opt == "dtgcurhr":
        dtg=yr + mo + dy + hr
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtimeonly"):
        dtg=hr+":"+mn+":"+sc+ tzname
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)

def dtg12(opt="default"):
    import time
    tzname=" %s "%(TimeZoneName())

    if (opt == "curtime" or opt == "curtimeonly" ):t=time.localtime(time.time())
    else:t=time.gmtime(time.time())

    yr="%04d" % t[0]
    mo="%02d" % t[1]
    dy="%02d" % t[2]
    hr="%02d" % t[3]
    fhr="%02d" % (int(t[3]/12)*12)
    phr=int(t[3])%12
    mn="%02d" % t[4]
    sc="%02d" % t[5]
    fphr=float(phr)*1.0 + float(mn)/60.0;

    if opt == "default":
        dtg=yr + mo + dy + fhr
    elif opt == "phr":
        dtg="%4.2f"%(fphr)
    elif opt == "fphr":
        dtg=fphr
    elif opt == "dtg.hm":
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn
    elif (opt == "timeonly"):
        dtg=hr+":"+mn+":"+sc+ " UTC "
    elif (opt == "time"):
        dtg=hr+":"+mn+":"+sc+ " UTC " + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtime"):
        dtg=hr+":"+mn+":"+sc+ tzname + str(t[2]) + " " + mname[mo] + ", " + yr
    elif (opt == "curtimeonly"):
        dtg=hr+":"+mn+":"+sc+ tzname
    else:
        dtg=yr + mo + dy + fhr + " " + hr + ":" + mn

    return(dtg)


def isRealTime(tdtgs,age=72.0):
    curdtg=dtg()
    alldtgs=tdtgs
    if(type(tdtgs) != ListType): alldtgs=[tdtgs]
    
    rc=1
    for tdtg in alldtgs:
        dtgd=dtgdiff(tdtg,curdtg)
        if(dtgd > age): 
            rc=0
            break
        
    return(rc)
    

def rhh2hhmm(hh):

    if(hh < 0):
        rhh=abs(hh)
        lt0=1
    else:
        rhh=hh
        lt0=0

    imm=int(rhh*60.0+0.5)
    ihh=imm/60
    imm=imm%60
    if(lt0):
        ohhmm="-%02d:%02d"%(ihh,imm)
    else:
        ohhmm="+%02d:%02d"%(ihh,imm)

    return(ohhmm)



def yyyymmrange(byyyymm,eyyyymm,inc=1):

    yyyymms=[]

    byyyymm=str(byyyymm)
    eyyyymm=str(eyyyymm)

    yyyymm=byyyymm

    while(yyyymm<=eyyyymm):
        yyyymms.append(yyyymm)
        yyyymm=yyyymminc(yyyymm,inc)


    return(yyyymms)

def yyyyrange(byyyy,eyyyy,inc=1):

    yyyys=[]

    byyyy=str(byyyy)
    eyyyy=str(eyyyy)

    yyyy=byyyy

    while(yyyy<=eyyyy):
        yyyys.append(yyyy)
        yyyy=yyyyinc(yyyy,inc)

    return(yyyys)



def yyyymmdiff(yyyymm1,yyyymm2):

    yyyy1=int(yyyymm1[0:4])
    yyyy2=int(yyyymm2[0:4])
    mm1=int(yyyymm1[4:6])
    mm2=int(yyyymm2[4:6])
    dyyyy=yyyy2-yyyy1
    dmm=mm2-mm1+1

    dyyyymm=(dyyyy*12)+dmm

    return(dyyyymm)


def yyyymminc(yyyymm,inc=1):
    yyyy=int(yyyymm[0:4])
    mm=int(yyyymm[4:6])
    mm=mm+inc
    if mm > 12:
        mm=mm-12
        yyyy=yyyy+1
    if mm < 1:
        mm=mm+12
        yyyy=yyyy-1

    nyyyymm="%04d%02d"%(yyyy,mm)
    return(nyyyymm)

def yyyyinc(yyyy,inc):

    yyyy=int(yyyy)

    nyyyy=yyyy+inc

    nyyyy="%04d"%(nyyyy)
    return(nyyyy)

def IsLeapYear(yyyy):
    rc=0
    if(yyyy%4 == 0 and (yyyy%100 != 0) or (yyyy%400 == 0)):
        rc=1
    return(rc)


def dtginc(idtg,off):

    dtg=str(idtg)
    
    if(len(dtg) == 10):
        yr=int(dtg[0:4])    
        mo=int(dtg[4:6])
        dy=int(dtg[6:8])
        hr=int(dtg[8:10])
    elif(len(dtg) == 11):
        yr=int(dtg[0:5])    
        mo=int(dtg[5:7])
        dy=int(dtg[7:9])
        hr=int(dtg[9:11])
        
    hr=hr+int(off)

    #
    # do leap if going forward in time
    #

    leap=0

    #200201120
    # problem, limit backward offset
    #
    if (IsLeapYear(yr) and off > -120): leap=1

    #
    # turn off leap of 365 day calendar
    #
    if(calendar == '365day'): leap=0

    ndyyr=365+leap

    jdy=dy-1

    ada=aday[mo-1]
    if leap == 1:ada=adayleap[mo-1];
    jdy=jdy+ada

    while hr >= 24:
        hr=hr-24
        jdy=jdy+1

    while hr < 0:
        hr=hr+24
        jdy=jdy-1

    if jdy <= 0:
        yr=yr-1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

        jdy=jdy+ndyyr

    if jdy > ndyyr:
        jdy=jdy-ndyyr
        yr=yr+1
        leap=0
        if(IsLeapYear(yr)):
            leap=1
            ndyyr=366
            if(calendar == '365day'):
                leap=0
                ndyyr=365
        else:
            ndyyr=365

    if(calendar == '365day'): leap=0

    i=11
    if leap == 1:
        while(jdy<adayleap[i]):i=i-1
        ndy=jdy-adayleap[i]+1
    else:
        while(jdy<aday[i]):i=i-1
        ndy=jdy-aday[i]+1

    yr="%04d"%yr
    mo="%02d"%(i+1)
    dy="%02d"%ndy
    hr="%02d"%hr

    ndtg=yr+mo+dy+hr

    return(ndtg)

def dtg2time(dtg):


    cdtg=str(dtg)

    try:
        yy=int(cdtg[0:4])
        mm=int(cdtg[4:6])
        dd=int(cdtg[6:8])
        hh=int(cdtg[8:10])

        ct=(yy,mm,dd,hh,0,0,0,0,0)
        time=mktime(ct)
    except:
        print 'dtg2time: invalid dtg: ',dtg,' sayoonara'
        sys.exit()

    return(time)

def dtgmn2time(dtg):

    from time import mktime 

    cdtg=str(dtg)

    yy=int(cdtg[0:4])
    mm=int(cdtg[4:6])
    dd=int(cdtg[6:8])
    hh=int(cdtg[8:10])
    mn=int(cdtg[10:12])

    ct=(yy,mm,dd,hh,mn,0,0,0,0)
    time=mktime(ct)
    return(time)


def dtgdiff(dtg1,dtg2):

    #from time import *

    dtg1=str(dtg1)
    dtg2=str(dtg2)

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)
    nhr=(t2-t1)*sec2hr

    return(nhr)

def dtgmndiff(dtgmn1,dtgmn2):

    #from time import *

    dtgmn1=str(dtgmn1)
    dtgmn2=str(dtgmn2)

    yyyy1=int(dtgmn1[0:4])
    yyyy2=int(dtgmn2[0:4])

    offyear=1981
    if(yyyy1%4==0):
        offyear=1980
    if(yyyy2%4==0):
        offyear=1979

    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtgmn1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtgmn2[4:10]

    t1=dtgmn2time(dtgmn1)
    t2=dtgmn2time(dtgmn2)
    nhr=(t2-t1)*sec2hr

    return(nhr)


def dtgShift0012(dtg,round=1):

    bstart=8
    if(len(dtg) == 11): bstart=9
    
    if(round):
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,6)
        else:
            odtg=dtg
    else:
        if(dtg[bstart:] == '06' or dtg[bstart:] == '18'):
            odtg=dtginc(dtg,-6)
        else:
            odtg=dtg

    return(odtg)


def dtgrange(dtg1,dtg2,inc=6):

    verb=0

    inc=int(inc)
    dtg1=str(dtg1)
    dtg2=str(dtg2)

    if(verb): print 'ddd dtgrange',dtg1,dtg2,inc

    if(inc > 0 and dtg2 < dtg1 and inc > 0):
        print "EEE invalid edtg (before bdtg) in dtgrange: dtg1: %s  dtg2: %s"%(dtg1,dtg2)
        sys.exit()

#
# return dtg1 if dtg1=dtg2
#
    if(dtg1 == dtg2):
        dtgs=[dtg1]
        return(dtgs)

#
# pre 1970? problem
#
    dtg1off=0

    yyyy1=int(dtg1[0:4])
    yyyy2=int(dtg2[0:4])

    offyear=1981
    #
    # 20031114 fix problem when begin/end year are the same
    #
    if(yyyy1%4 == 0 and yyyy2%4 == 0):
        offyear=1980
    if(yyyy2%4 == 0 and yyyy1%4 != 0):
        offyear=1979

    if(verb): print 'aaa ',yyyy1,yyyy2,yyyy1%4,yyyy2%4,offyear
    #
    # override leaping if 365 day calendar
    #
    if(calendar == '365day'): offyear=1981

    #
    # 20030828 -- fix crossing year if offsetting
    #

    dyyyy=yyyy2-yyyy1

    if(verb): print 'bbb ',dtg1,dtg2,yyyy1,yyyy2,offyear
    if(yyyy1 < offyear or yyyy2 < offyear):
        dtg1off=offyear-int(dtg1[0:4])
        dtg1="%04d"%(offyear)+dtg1[4:10]
        dtg2="%04d"%(offyear+dyyyy)+dtg2[4:10]

    t1=dtg2time(dtg1)
    t2=dtg2time(dtg2)


    nhr=(t2-t1)*sec2hr
    dtgs=[]
    dtgo=str(dtg1)

    if(inc > 0):
        ntime=nhr/inc
        if(verb): print 'ddd dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    elif(inc <  0):
        dtgo=str(dtg1)
        ntime=abs(nhr/inc)
        if(verb): print 'ddd ------------ dtgrange',ntime,nhr,inc
        dtga=dtgo
        dtgs.append(dtga)
        i=1
        while(i<=ntime):
            dtgn=dtginc(dtgo,inc)
            dtga=dtgn
            dtgs.append(dtga)
            dtgo=dtgn
            i=i+1

        if(dtg1off != 0):
            i=0
            for dtg in dtgs:
                yyyy=int(dtg[0:4])-dtg1off
                dtga="%04d%s"%(yyyy,dtg[4:10])
                dtgs[i]=dtga
                i=i+1

    else:
        dtgs=[-999]

    return(dtgs)

def dtg2ymdh(dtg):

    cdtg=str(dtg)
    if(len(cdtg) == 10):
        yy=cdtg[0:4]
        mm=cdtg[4:6]
        dd=cdtg[6:8]
        hh=cdtg[8:10]
        
    elif(len(cdtg) == 11):
        yy=cdtg[0:5]
        mm=cdtg[5:7]
        dd=cdtg[7:9]
        hh=cdtg[9:11]
        
    else:
        yy=cdtg[0:2]
        mm=cdtg[2:4]
        dd=cdtg[4:6]
        hh=cdtg[6:8]
        yy='19'+yy

    return(yy,mm,dd,hh)

def dtg2vtime(dtg):

    tt=dtg2time(dtg)
    gmt=gmtime(tt)
    #vtime=strftime("%a %HZ %d %b %y",gmt)
    vtime=strftime("%a %d %b %HZ",gmt)
    return(vtime)

def dtg2gtime(dtg):
    try:
        (y,m,d,h)=dtg2ymdh(dtg)
    except:
        return(none)
    mo=mname3[m]
    gtime="%sZ%s%s%s"%(h,d,mo,y)
    return(gtime)

def yyyymm2gtime(yyyymm):
    y=yyyymm[0:4]
    m=yyyymm[4:]
    mo=mname3[m]
    gtime="%s%s"%(mo,y)
    return(gtime)

def gtime2dtg(gtime):
    h=gtime[0:2]
    d=gtime[3:5]
    m=gtime[5:8]
    y=gtime[8:]
    cm=cname3[m]
    dtg=y+cm+d+h
    return(dtg)

def chomp(string):
    ss=string[:-1]
    return ss

def uniq(ulist):
    weirdtest='asdasdfasdfasdfasdf'
    #
    # sort before length check for case of two
    #
    ulist.sort()
    rlist=[]

    if(len(ulist) > 2):
        test=ulist[1]
        test=weirdtest
    elif(len(ulist) == 0):
        return(rlist)
    else:
        test=ulist[0]

    if(test != weirdtest):
        rlist.append(test)

    for l in ulist:
        #if(repr(l) != repr(test)):
        if(l != test):
            rlist.append(l)
            test=l
    return(rlist)


def fopen(file,state='r'):
    from sys import exit
    try:
        fh=open(file,state)
        return(fh)
    except:
        print "unable to open: ",file,"\nsayoonara"
        exit()


def argopt(i):
    import sys
    try:
        if(sys.argv[i]):
            return(1)
    except:
        return(0)


def dtg_dtgopt_prc(dtgopt,ddtg=6):

    ddc=dtgopt.split(',')
    
    if(len(ddc) > 1):
        dtgs=[]
        for dc in ddc:
            if(find(dc,'.') or len(dc) != 10):
                dtgs=dtgs+dtg_dtgopt_prc(dc)
            else:
                dtgs.append(dc)
        return(dtgs)


    dd=dtgopt.split('.')
    if(len(dd) == 1):
        if(len(dtgopt) == 6 and dtgopt.isdigit()):
            bdtg="%s0100"%(dtgopt)
            edtg=dtginc("%s0100"%(yyyymminc(dtgopt,1)),-6)

        else:
            bdtg=dtg_command_prc(dtgopt)
            edtg=bdtg

    if(len(dd) >= 2):

        if(len(dd[0]) == 6 and dd[1].isdigit()):
            bdtg="%s0100"%(dd[0])
        else:
            bdtg=dtg_command_prc(dd[0])
 
        if(len(dd[0]) == 6):
            if(dd[1].isdigit()):
                if(len(dd[1]) == 6):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[1],1)),-6)
                elif(len(dd[1]) == 2 or dd[1] == '6'):
                    edtg=dtginc("%s0100"%(yyyymminc(dd[0],1)),-int(dd[1]))
                    ddtg=int(dd[1])
            else:
                edtg=dtg_command_prc(dd[1])    
        else:
            edtg=dtg_command_prc(dd[1])

    if(len(dd) == 3):
        ddtg=dd[2]

    if(find(dtgopt,'cur12')): ddtg=12

    dtgs=dtgrange(bdtg,edtg,ddtg)

    if(dtgs[0] == '-1'):
        print 'EEE dtg_dtgopt_prc bad dtgopt: ',dtgopt
        sys.exit()

    return(dtgs)


def dtg_command_prc(dtg,quiet=0,curdtg12=0,opsfhr=5.0):

    odtg=dtg
    if(curdtg12):
        curdtg=dtg12()
    else:
        curdtg=dtg6()

    if(dtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(dtg == 'cur+6'):
        odtg=dtginc(curdtg,+6)
    elif(dtg == 'cur'):
        odtg=curdtg
    elif(dtg == 'cur12'):
        odtg=dtg12()
    elif(dtg == 'cur-6'):
        odtg=dtginc(curdtg,-6)
    elif(dtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(dtg == 'cur-18'):
        odtg=dtginc(curdtg,-18)
    elif(dtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)
    elif(dtg == 'cur-30'):
        odtg=dtginc(curdtg,-30)
    elif(dtg == 'cur-36'):
        odtg=dtginc(curdtg,-36)
    elif(dtg == 'cur-42'):
        odtg=dtginc(curdtg,-42)
    elif(dtg == 'cur-48'):
        odtg=dtginc(curdtg,-48)
    elif(dtg == 'cur-d1'):
        odtg=dtginc(curdtg,-24)

    elif(find(dtg,'cur-')  and not(find(dtg,'cur-d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,-1*nhr)

    elif(find(dtg,'cur12-')  and not(find(dtg,'cur12-d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(dtg12(),-1*nhr)

    elif(find(dtg,'cur+') and not(find(dtg,'cur+d')) ):
        ld=len(dtg)
        nhr=int(dtg[4:ld])
        odtg=dtginc(curdtg,nhr)

    elif(find(dtg,'cur12+') and not(find(dtg,'cur12+d')) ):
        ld=len(dtg)
        nhr=int(dtg[6:ld])
        odtg=dtginc(curdtg,nhr)

#
# -dXXX
#
    elif(find(dtg,'cur-d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,-1*nday*24)

    elif(find(dtg,'cur12-d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(dtg12(),-1*nday*24)

    elif(find(dtg,'cur+d')):
        ld=len(dtg)
        nday=int(dtg[5:ld])
        odtg=dtginc(curdtg,nday*24)

    elif(find(dtg,'cur12+d')):
        ld=len(dtg)
        nday=int(dtg[7:ld])
        odtg=dtginc(curdtg,nday*24)

    elif(dtg == 'ops12'):
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhr):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops12long'):
        opsfhrl=11.0
        odtg=dtg12()
        fphr=float(dtg12('fphr'))
        if(fphr <= opsfhrl):
            odtg=dtginc(odtg,-12)
    elif(dtg == 'ops6'):
        (odtg,phr)=dtg_phr_command_prc('cur')
        fphr=float(phr)
        if(fphr <= opsfhr*0.5):
            odtg=dtginc(odtg,-6)

    if(len(odtg) != 10):
        if(quiet != 0):
            print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1

    if(len(dtg.split('.')) > 1):
        odtg=len(dtg.split('.'))

    return(odtg)

def dtg_phr_command_prc(idtg):

    curdtg=dtg()
    curphr=dtg('phr')

    ddtg=-9999

    odtg=dtg_command_prc(idtg)

    if(ddtg != -9999):
        odtg=dtginc(curdtg,ddtg)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)
        odtg=-1
        ocurphr=-1
        return(odtg,ocurphr)

    deltadtg=dtgdiff(odtg,curdtg)
    curphr=float(curphr)+float(deltadtg)

    if(curphr >= 0.0 and curphr < 10.0):
        ocurphr="+%3.2f"%(curphr)
    elif(curphr >= 10.0 and curphr < 100.0):
        ocurphr="+%4.2f"%(curphr)
    elif(curphr >= 100.0 and curphr < 1000.0):
        ocurphr="+%5.2f"%(curphr)

    else:
        ocurphr="%7.2f"%(curphr)


    return(odtg,ocurphr)


def dtg_12_command_prc(idtg):

    odtg=idtg
    curdtg=dtg()
    if(idtg == 'cur+12'):
        odtg=dtginc(curdtg,+12)
    elif(idtg == 'cur'):
        odtg=curdtg
    elif(idtg == 'cur-12'):
        odtg=dtginc(curdtg,-12)
    elif(idtg == 'cur-24'):
        odtg=dtginc(curdtg,-24)

    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)

def cur2dtg(idtg):

    odtg=idtg

    curdtg=dtg6()

    if(idtg == 'cur+12'): odtg=dtginc(curdtg,+12)
    if(idtg == 'cur+6'): odtg=dtginc(curdtg,+6)
    if(idtg == 'cur'): odtg=curdtg
    if(idtg == 'cur-6'): odtg=dtginc(curdtg,-6)
    if(idtg == 'cur-12'): odtg=dtginc(curdtg,-12)
    if(idtg == 'cur-18'): odtg=dtginc(curdtg,-18)
    if(idtg == 'cur-24'): odtg=dtginc(curdtg,-24)
    if(idtg == 'cur-36'): odtg=dtginc(curdtg,-36)
    if(idtg == 'cur-48'): odtg=dtginc(curdtg,-48)


    if(len(odtg) != 10):
        print "EEE odtg ",odtg," fouled len: ",len(odtg)

    return(odtg)


def getCommandOutput2(command):
    child = os.popen(command)
    data = child.read()
    err= child.close()
    if err:
        raise RuntimeError, '%s failed with the exit code %d\n' % (command,err)
    return data



def runcmd(command,logpath='straightrun',lsopt='',prefix='',postfix=''):

    if(logpath == ''):
        logpath='straightrun'

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(logpath == 'straightrun' or logpath == 'norun'):

        curtime=dtg('cur_hms')
        occc="CCC"
        if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
        if(lsopt != 'q'): print "%s: %s %s %s"%(occc,command,curtime,opostfix)
        if(logpath != 'norun'): os.system(command)
        return

    if(logpath == 'quiet'):
        os.system(command)
        return

    global LF

    #
    # output to log file (append and add title line)
    #

    if(logpath != 'nologpath'):

        log=getCommandOutput2(command)

        lout="\nTTT: %s  :: CCC: %s\n\n"%(dtg6('curtime'),command)
        lout=lout+log

        if(not(os.path.exists(logpath))):
            try:
                LF=open(logpath,'a')
                LF.writelines(lout)
                LF.flush()
            except:
                print 'EEE(runcmd): unable to open logpath: %s'%(logpath)
                return
        else:
            try:
                LF.writelines(lout)
                LF.flush()
            except:
                try:
                    LF=open(logpath,'a')
                    LF.writelines(lout)
                    LF.flush()
                except:
                    LF.writelines(lout)
                    LF.flush()
                    print 'EEE(runcmd): unable to write to logpath: %s'%(logpath)
                    return

    #
    # output to terminal
    #

    else:

        log=getCommandOutput2(command)

        print "CCC(log): %s\n"%command
        print log

    return

def runcmd2(command, ropt='', verb=1, lsopt='', prefix='', postfix='', ostdout=1,
            wait=False):

    oprefix=''
    if(prefix != ''): oprefix="(%s)"%(prefix)
    
    opostfix=''
    if(postfix != ''): opostfix="[%s]"%(postfix)

    if(ropt == 'norun'):  
        if(oprefix != ''):  oprefix="%s-NNNrun"%(oprefix)
        else:               oprefix='NNNrun'
        if(opostfix != ''): opostfix="%s-NNN"%(opostfix)
        else:               opostfix='NNN'
    curtime=dtg('cur_hms')
    occc="CCC-222"
    if(oprefix != ''): occc="%s(%s)"%(occc,oprefix)
    ocard="%s: %s %s %s"%(occc,command,curtime,opostfix)
    if(lsopt != 'q'): print ocard
    
    if(ropt == 'norun'): return(0)
    
    import subprocess
    try:
        if (wait):

            p = subprocess.Popen(
                [command], 
                stdout = subprocess.PIPE,
                shell = True)
            p.wait()
        else:
            if(ostdout == 1):
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = PIPE, stderr = PIPE, close_fds = True)
            else:
                p = subprocess.Popen(
                    [command], 
                    shell = True, 
                    stdin = None, stdout = None, stderr = PIPE, close_fds = True)
                
        (result, error) = p.communicate()

        
    except subprocess.CalledProcessError as e:
        sys.stderr.write(
            "common::run_command() : [ERROR]: output = %s, error code = %s\n" 
            % (e.output, e.returncode))
        
        return(-999)


    rc=1
    if(ostdout == 1):
        slines=result.split('\n')

        if(verb): 
            print 'STDOut...'
            for line in slines:
                if(len(line) > 0):  print line

    elines=error.split('\n')
    if(verb and len(elines) > 1): print'STDErr...'
    for line in elines:
        if(verb): 
            if(len(line) > 0):  print line
        if(find(line,'error')): 
            rc=-999

    if(ostdout == 1): rc=(rc,slines)
    
    return (rc)



def PathCreateTime(path):
    import time
    timei=os.path.getctime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

def PathModifyTime(path):
    import time
    timei=os.path.getmtime(path)
    ltimei=time.localtime(timei)
    gtimei=time.gmtime(timei)
    dtimei=time.strftime("%Y%m%d%H:%M%S",ltimei)
    gdtimei=time.strftime("%Y%m%d%H:%M%S",gtimei)
    ldtg=dtimei[0:10]
    gdtg=gdtimei[0:10]
    return(dtimei,ldtg,gdtg)

def ChkDirOld(dir,diropt='verb'):

    if(dir == None):
        if(diropt != 'quiet'): print "dir      = None : "
        return(-2)

    if not(os.path.isdir(dir)) :
        if(diropt != 'quiet'): print "dir  (not there): ",dir
        if(diropt == 'mk' or diropt == 'mkdir'):
            try:
                os.system('mkdir -p %s'%(dir))
            except:
                print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                return(-1)
            print 'dir     (MADE): ',dir
            return(2)
        else:
            return(0)
    else:
        if(diropt == 'verb'):
            print "dir      (there): ",dir
        return(1)

def ChkDir(ddir,diropt='verb'):

    if(ddir == None):
        if(diropt != 'quiet'): print "dir      = None : "
        return(-2)

    if not os.path.exists(ddir):
        
        if(diropt != 'quiet'): print "dir  (not there): ",ddir
        if(diropt == 'mk' or diropt == 'mkdir'):
    
            try:
                os.makedirs(ddir)
                print 'dir     (MADE): ',ddir
                return(2)
                
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
                    #print 'EEE unable to mkdir: ',dir,' in ChkDir, return -1 ...'
                    #return(-1)
                else:
                    print "\nBE CAREFUL! Directory %s already exists." % path
    
        else:
            return(0)
        
    else:
        if(diropt == 'verb'):
            print "dir      (there): ",ddir
        return(1)

def ChangeDir(dir,diropt='verb'):

    try:
        os.chdir(dir)
        print 'cd---> ',dir
    except:
        print 'WWW unable to cd to: ',dir

def ChkPath(path,pathopt='noexit',verb=1):

    if not(os.path.exists(path)) :
        if(verb): print "EEE(ChkPath): path: %s NOT there... "%(path)
        if(pathopt == 'exit'):
            print "EEE(ChkPath): Sayoonara..."
            sys.exit()
        else:
            return(0)
    else:
        return(1)

def GetPathSiz(path,pathopt='exit',verb=1):

    if(ChkPath(path,pathopt='noexit') != 1):
        siz=None
    else:
        siz=os.path.getsize(path)

    return(siz)





def LsPids():

    #
    # get executing processes
    #

    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)

def findPyPids(job):

    #
    # get executing processes
    #

    processes=os.popen('ps kstart_time -ef | grep -i %s'%(job)).readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[1]),int(tt[2]),pname,piddate) )
        
    opids=[]
    for pid in pids:
        if(find(pid[2],'python')):
            opids.append(pid)
        

    return(opids)


def LsPids3():

    # get executing processes and three ids (on bsd/mac only?)
    #
    processes=os.popen('ps -ef ').readlines()
    pids=[]
    for i in range(1,len(processes)):
        process=processes[i]
        tt=process.split()
        pname=''
        for n in range(7,len(tt)):
            pname="%s %s"%(pname,tt[n])
        piddate=tt[4]
        pname=pname.lstrip()
        pids.append( (int(tt[0]),int(tt[1]),int(tt[2]),pname,piddate) )

    return(pids)


def PsTime2Hours(time):
    tt=time.split('-')

    if(len(tt) == 2):
        days=float(tt[0])
        ttime=tt[1].split(':')
    else:
        days=0.0
        ttime=time.split(':')

    hours=float(ttime[0])
    minutes=float(ttime[1])
    seconds=float(ttime[2])

    totaltime=days*24.0 + hours + (minutes+ (seconds/60.0) )/60.0

    return(totaltime)


def LsPidsuSer():

    #
    # get user executing processes
    #
    user=os.getenv('USER')
    processes=os.popen("ps -u %s -o \"pid,ppid,time,comm\""%(user)).readlines()
    pids=[]

    for n in range(1,len(processes)):
        p=processes[n]
        tt=p.split()
        pid=int(tt[0])
        ppid=int(tt[1])
        time=tt[2]
        command=tt[3]
        totaltime=PsTime2Hours(time)
        pids.append( (pid, ppid, totaltime, command) )

    return(pids)

def KillLongRunningProcess(timelimitkill,command2kill):

    upids=LsPidsuSer()
    for upid in upids:
        pid=upid[0]
        totaltime=upid[2]
        command=upid[3]
        if(totaltime >= timelimitkill and command == command2kill):
            print 'KKKKKKKKKKKilling: ',pid,totaltime,command
            os.kill(pid,signal.SIGKILL)






def KillPids(parentpid):

    verb=1

    #
    #  look for children (cpid) of the current parent process (ppid)
    #  put in list of spawned pids (spids)
    #
    #  initialize with input pid from calling parent

    curpid=parentpid

    spids=[]

    pids=LsPids()

    for pid in pids:
        cpid=pid[0]
        ppid=pid[1]
        pname=pid[2]

        if(ppid == curpid):
            spids.append(cpid)
            curpid=cpid
            if(verb): print cpid,ppid,curpid,pname

    #
    #  send kill signal to spids
    #

    nspids=len(spids)
    if(verb): print 'KKKKKKKKKKKK',nspids,spids,parentpid
    for spid in spids:
        try:
            print 'Killing pid: ',spid
            os.kill(spid,signal.SIGKILL)
        except:
            if(verb):
                print "unable to kill spawnd process: ",spid
            else:
                pass

    #
    #  now kill the main process if the one of the spawned 
    #

    try:
        os.kill(curpid,signal.SIGKILL)
    except:
        pass



def CleanReturns(istring):

    olist=[]

    o=istring.split('\n')

    for oo in o:
        if(len(oo) != 0):
            olist.append(oo+'\n')

    return(olist)

#
# calculate age of file using current and motime (h)
#
def PathDmtime(ipath):

    import time
    import os
    ctime=time.time()
    mtime=os.path.getmtime(ipath)
    dmtime=(ctime-float(mtime))/3600.0
    return(dmtime)


def doFTPsimple(server,localdir,remotedir,mask,
                opt='ftp.put',passive='off',doitout=0,quittime=None,
                verb=0):


    ftpopt=''
    if(quittime != None):
        ftpopt="-q %s"%(quittime)

    if(passive == 'off'):
        passopt=''
    elif(passive == 'on'):
        passopt='passive'
    else:
        passopt='passive'

    if(opt == 'ftp.ls' or opt == 'ftp.noload'):
        cmd="""
%s
cd %s
pwd
dir %s
quit
"""%(passopt,remotedir,mask)

    elif(opt == 'local.ls' or opt == 'ftp.noload'):
        cmd="""
%s
lcd %s
pwd
!ls -l %s
quit
"""%(passopt,localdir,mask)

    elif(opt == 'ftp.mkdir'):
        cmd="""
%s
mkdir %s
"""%(passopt,remotedir)

    elif(opt == 'ftp.rm'):
        cmd="""
%s
###verbose
prompt
cd %s
pwd
mdel %s
"""%(passopt,remotedir,mask)

    elif(opt == 'ftp.put' or opt == 'ftp'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,localdir,mask)

    elif(opt == 'ftp.put.mk' or opt == 'ftp'):

        cmd="""
#passive
verbose
mkdir %s
cd %s
lcd %s
bin
prompt
mput %s
"""%(remotedir,remotedir,localdir,mask)

    elif(opt == 'ftp.get'):

        cmd="""
#passive
verbose
cd %s
lcd %s
bin
prompt
mget %s
"""%(remotedir,localdir,mask)

    else:
        print 'EEEEEEEEEEE in doFTPsimple invalid opt: ',opt
        sys.exit()


    doit=1
    if(opt == 'ftp.noload'): doit=0

    if(doit and doitout==0):
        ftppopen="ftp %s %s"%(ftpopt,server)
        if(verb): print 'ftppopen: ',ftppopen,' ftp cmd: ',cmd
        o=os.popen(ftppopen,"w")
        o.write(cmd)
        o.close()

    if(doitout):
        if(verb): print "ftp cmd:",cmd
        cmd="""ftp %s %s << EOF
%s
EOF
"""%(ftpopt,server,cmd)
        rc=os.popen(cmd).readlines()
        return(rc)

    #if(opt == 'ftp.ls'): sys.exit()

#
# 20031120 - process __doc__ string (str)
# to add pyfile
#

def usage(str,arg,curdtg=None,curtime=None,curphr=None):
    n=str.count('%s')
    pp=[]
    for n in range(0,n): pp.append(arg)
    pp=tuple(pp)
    print str%(pp)
    if(curdtg!=None and curtime!=None and curphr!=None):
        print "The Current DTG: %s  Phr: %s  Time: %s"%(curdtg,curphr,curtime)
    elif(curdtg!=None and curtime!=None):
        print "The Current DTG: %s  Time: %s"%(curdtg,curtime)


def find(mystr,pattern):
    rc=0
    if(mystr.find(pattern) != -1): rc=1
    return(rc)





def WriteCtl(ctl,ctlpath,verb=0):

    try:
        c=open(ctlpath,'w')
    except:
        print "EEE unable to open: %s"%(ctlpath)
        sys.exit()

    if(verb): print "CCCC creating .ctl: %s"%(ctlpath)
    c.writelines(ctl)
    c.close()
    return

def WriteList(llist,opath,verb=0,wmode='w'):

    try:
        c=open(opath,wmode)
    except:
        print "EEE unable to open: %s"%(opath)
        sys.exit()

    if(verb): print "CCCC creating list output file: %s"%(opath)
    for card in llist:
        card=card+'\n'
        c.writelines(card)
    c.close()
    return


def PrintCtl(ctl,ctlfile=None):

    if(ctlfile):
        otitle=ctlfile
    else:
        otitle="ctl file"
    print "PPPPPPPPP printing: %s ..................."%(otitle)

    for cc in ctl:
        print cc[:-1]

def PrintCurrency(title,ns=54,amount=-999):
    ntot=str(amount)
    nl=len(ntot)
    if(nl>9):
        n9=nl-9
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %4s,%3s,%3s,%3s"%(ns-4,ntot[0:n9],ntot[n9:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>6):
        n6=nl-6
        n3=nl-3
        format="%%-%ds :: %8s,%3s,%3s"%(ns-4,ntot[0:n6],ntot[n6:n3],ntot[n3:])
    elif(nl>3):
        n3=nl-3
        format="%%-%ds :: %12s,%3s"%(ns-4,ntot[0:n3],ntot[n3:])
    else:
        format="%%-%ds :: %16s"%(ns-4,ntot)
    print format%(title)

    return

def PyVer():
    (pyverMajor,pyverMinor,pyverRel)=sys.version.split()[0].split('.')[0:3]
    fpyver=float("%s.%s%s"%(pyverMajor,pyverMinor,pyverRel))
    return(fpyver)

def Timer(str,stime):
    import time
    dtime=time.time()-stime
    print "ffffffff %-60s time: %5.2f s"%(str,dtime)


#
# function to glob than cp files 
#

def cpfiles(sdir,tdir,mask,ropt=''):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="cp %s %s/."%(file,tdir)
        runcmd(cmd,ropt)


def rmfiles(sdir,mask,ropt='norun'):

    files=glob.glob("%s/%s"%(sdir,mask))

    for file in files:
        cmd="rm %s"%(file)
        runcmd(cmd,ropt)

def h2hm(age):

    fh=int(age)*1.0
    im=int( (age-fh)*60.0+0.5 )
    if(im == 60):
        fh=fh+1.0
        im=0

    cage="%4.0f:%02d"%(fh,im)
    return(cage)


def min2minsec(min):

    fm=int(min)*1.0
    im=int( (min-fm)*60.0+0.5 )
    if(im == 60):
        fm=fm+1.0
        im=0

    cmin="%4.0f:%02d"%(fm,im)
    return(cmin)



# -- MMMMMMMMMM -- w2methods
#
def Model2DataTaus(model,dtg):

    dtghh=int(dtg[8:10])
    
    #from M2 import setModel2
    m=setModel2(model)

    etau=None
    dtau=None

    # -- more agressive use of M2
    #
    if(m != None):
        
        # -- ukm2 and navg have a getDataTaus methods
        #
        if(hasattr(m,'getDataTaus')): 
            taus=m.getDataTaus(dtg)
            
        elif(hasattr(m,'dattaus')): 
            taus=m.dattaus
        else:
            etau=m.getEtau(dtg=dtg)
            dtau=m.getDtau(dtg=dtg)
            taus=range(0,etau+1,dtau)
        return(taus)

    taus=[]

    if(model == 'gfs2' or model == 'fim8' or model == 'fimx' or 
       model == 'gfsr' or model == 'gfr1' or model == 'gfsk' or
       model == 'ecm2' or model == 'ecm4' or 
       model == 'cmc2' or model == 'cgd6' or model == 'cgd2' or
       model == 'ocn' or model == 'ohc' or model == 'ww3' or
       model == 'ecmg' or
       model == 'ngpc' or model == 'ngpj' or
       model == 'navg' or
       model == 'jgsm' or
       model == 'gfsc' or model == 'goes' 
       ):
        if(etau == None):
            etau=self.Model2EtauData(model,dtghh)
            dtau=self.Model2DtauData(model,dtghh)

        if(etau != None):
            taus=range(0,etau+1,dtau)
        else:
            taus=[]

    # -- special cases
    #
    elif(model == 'ukm2' or model == 'ngp2' ):
        if(dtghh == 0 or dtghh == 12):
            taus=range(0,72+1,6)+range(84,144+1,12)
        elif(dtghh == 6 or dtghh == 18):
            taus=range(0,60+1,6)

    elif(model == 'ukmc'):
        if(dtghh == 12):
            taus=range(0,72+1,6)+range(84,120+1,12)
        elif(dtghh == 0):
            taus=range(0,72+1,6)+range(84,120+1,12)
        else:
            taus=[]


    # -- nws ecmwf
    #
    elif(model == 'ecmn'):
        taus=range(0,48+1,6)+range(48,240+1,12)

    elif(model == 'jmac'):
        if(dtghh == 12):
            taus=range(0,72+1,6)+range(84,168+1,12)
        elif(dtghh == 0):
            taus=range(0,72+1,6)+range(84,84+1,12)
        else:
            taus=[]

    elif(model == 'gfsn'):
        etau=Model2EtauData(model,dtghh)
        dtau=Model2DtauData(model,dtghh)
        if(etau != None):
            taus=range(0,etau+1,dtau)
        else:
            taus=[]



    else:
        print 'EEE invalid model Model2DataTaus: ',model
        sys.exit()


    return(taus)

def SetLandFrac(lfres='1deg',ni=720,nj=361):

    lf=array.array('f')
    gdir=sbtGeogDatDir
    lfres='1deg'
    lfpath="%s/lf.%s.dat"%(gdir,lfres)
    LF=open(lfpath,'rb')
    nij=ni*nj
    lf.fromfile(LF,nij)
    return(lf)

#  return land frac given lat/lon; note defaults; same as used by .gs
#

def GetLandFrac(lf,tlat,tlon,ni=720,nj=361,blat=-90.0,blon=0.0,dlat=0.5,dlon=0.5):


    def w2ij(wi,wj,ni,nj,wi0,wj0,dwi,dwj):

        i=(wi-wi0)/dwi + 0.5
        j=(wj-wj0)/dwj + 0.5

        #
        # cyclic continuity in x
        #
        if(i <  0.0): i=float(ni)+i
        if(i >   ni): i=i-float(ni)

        i=int(i+1.0)
        j=int(j+1.0)

        return(i,j)


    (i,j)=w2ij(tlon,tlat,ni,nj,blon,blat,dlon,dlat)
    ij=(j-1)*ni+i-1
    return(lf[ij])



def setGA(gaclass='gacore',Opts='',Bin='grads',Quiet=1,Window=0,verb=0,doLogger=0):

    if(gaclass == 'gacore'):

        MF.sTimer(tag='load grads gacore')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore')
        
        from sBTcl import W2GaBase,GradsEnv,GradsPlot,gxout,gxset,gxdefvar,gxget
        
        class W2GaCore(GaCore,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin=Bin, Echo=True, Opts=Opts, Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)
        

        ga=W2GaCore(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    if(gaclass == 'galats'):

        MF.sTimer(tag='load grads gacore - galats')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore - galats')
        

        class W2GaLats(GaCore,GaLatsQ,GrADSError,MFbase):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)

                # -- lats vars
                #
                
                self.dtg=dtg
                self.model=model
                self._cmd=self.cmd2

                self.frequency=frequency

                self.regrid=regrid
                self.remethod=remethod
                self.smth2d=smth2d
                self.doyflip=doyflip
                self.reargs=reargs

                self.area='global'

                self.btau=btau
                self.etau=etau
                self.dtau=dtau

                if(taus == None):
                    self.taus=range(btau,etau+1,dtau)
                else:
                    self.taus=taus


                self("set_lats parmtab %s"%(ptable))
                self("set_lats convention %s"%(outconv))
                self("set_lats calendar %s"%(calendar))
                self("set_lats model %s"%(model))
                self("set_lats center %s"%(center))
                self("set_lats comment %s"%(comment))
                self("set_lats timeoption %s"%(timeoption))
                self("set_lats frequency %s"%(frequency))

                if(self.frequency == 'forecast_hourly'):
                    self("set_lats deltat %d"%(dtau))
                elif(self.frequency == 'forecast_minutes'):
                    self("set_lats deltat %d"%(dtau*60))

                self("set_lats gridtype %s"%(gridtype))

                if(hasattr(ga,'fh')):
                    self.fh=ga.fh
                else:
                    print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
                    sys.exit()

                ge.getFileMeta(self)


        ga=W2GaLats(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    elif(gaclass == 'ganum'):

        MF.sTimer(tag='load grads gacore-ganum')
        from grads import GaNum,GrADSError
        MF.dTimer(tag='load grads gacore-ganum')


        class W2GaNum(GaNum,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)



        ga=W2GaNum(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)
        

    # -- decorate with verb
    ga.verb=verb
    ga.ge.verb=verb

    ga.gxout=gxout(ga)
    ga.set=gxset(ga)
    ga.dvar=gxdefvar(ga)
    ga.get=gxget(ga)
        
    return(ga)


def setXgrads(useStandard=0,useX11=1,returnBoth=0):
    
    if(useStandard):
        xgrads='grads'
        rc=xgrads
        if(returnBoth): rc=(xgrads,xgrads)
        return(rc)
    
    bdirApp=os.getenv('W2_BDIRAPP')
    gradsVersion='opengrads-2.2.1.oga.1'

    xgradsX='%s/%s/Contents/gradsX11'%(bdirApp,gradsVersion)
    xgrads='%s/%s/Contents/grads'%(bdirApp,gradsVersion)

    if(xgrads == None):
        print 'EEEE----XXXGGGRRRAAADDDSSS - xgrads not set!!!'
        sys.exit()
    
    if(useX11):     rc=xgradsX
    else:           rc=xgrads
    if(returnBoth): rc=(xgradsX,xgrads)
    return(rc)

def setPngquant():
    
    xpngquant='/usr/bin/pngquant'
    return(xpngquant)


def is0012Z(dtg):
    rc=0
    if(dtg[8:10] == '00' or dtg[8:10] == '12'): rc=1
    return(rc)


def is0618Z(dtg):
    rc=0
    if(dtg[8:10] == '06' or dtg[8:10] == '18'): rc=1
    return(rc)

def IsOffTime(dtg):
    dtghh=int(dtg[8:10])
    if(dtghh == 6 or dtghh == 18):
        return(1)
    else:
        return(0)

def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
            
    else:
        yyyy=y
    return(yyyy)

# -- MMMMMMMMMM -- tcVM methods
#
def CurShemOverlap(curdtg):

    #
    # need to run twice in overlap between shem and nhem seasons
    #

    cy=curdtg[0:4]


    icym0=int(cy)
    icyp1=icym0+1
    cyp1=str(icyp1)

    icymd0=int(curdtg[0:8])

    ccymd0e=str(icym0)+'1231'
    icymd0e=int(ccymd0e)

    ccymdshemb=str(icym0)+'0701'
    icymdshemb=int(ccymdshemb)

    shemoverlap=0
    if(icymd0 >= icymdshemb and icymdshemb <= icymd0e): shemoverlap=1

    return(shemoverlap,cy,cyp1)



def gc_dist(rlat0,rlon0,rlat1,rlon1,tcunits=tcunits):

    # -- based on the spherical law of cosines 
    #

    dlat=abs(rlat0-rlat1)
    dlon=abs(rlon0-rlon1)
    if(dlon == 360.0): dlon=0.0
    zerotest=(dlat<epsilon and dlon<epsilon)
    if(zerotest): return(0.0)

    f1=deg2rad*rlat0
    f2=deg2rad*rlat1
    rm=deg2rad*(rlon0-rlon1)
    finv=cos(f1)*cos(f2)*cos(rm)+sin(f1)*sin(f2)
    rr=rearth*acos(finv)
    if(tcunits =='english'): rr=rr*km2nm 

    return(rr)


def mercat(rlat,rlon):

    lat=rlat*deg2rad

    if(rlon < 0.0):
        lon=360.0+rlon
    else:
        lon=rlon

    x=lon*deg2rad
    y=log(tan(pi4+lat*0.5))

    return(x,y)


def gc_theta(blat1,blon1,flat1,flon1):

    verb=0
    (xa,ya)=mercat(flat1,flon1)
    (xr,yr)=mercat(blat1,blon1)

    difx=xa-xr
    dify=ya-yr

    difx=difx*rad2deg*deglat2nm
    dify=dify*rad2deg*deglat2nm

    if (difx == 0.0):

        if(dify >= 0.0): theta=pi2
        if(dify < 0.0): theta=3*pi/2.0 

    else:

        slope=dify/difx
        if (abs(slope) < 1e-10):
            if(dify >= 0.0): theta=pi2 
            if(dify <= 0.0): theta=pi
        else:
            theta=atan2(dify,difx)
            #if(theta < 0.0):
            #   theta=theta + 2.0*pi
            theta=theta*rad2deg
            return(difx,dify,theta)

        if (difx > 0.0):
            if(dify < 0.0): theta=pi-theta
        else:
            if (dify > 0.0):
                theta=2*pi+theta
                theta=theta
            else:
                theta=pi+theta
                theta=theta


    #if(theta < 0.0):
    #    theta=theta + 2.0*pi

    theta=theta*rad2deg
    return(difx,dify,theta)


def dist_err(blat,blon,blat1,blon1,flat,flon,tcunits=tcunits):

    verb=0
    (xa,ya)=mercat(flat,flon)
    (xb,yb)=mercat(blat,blon)
    (xr,yr)=mercat(blat1,blon1)

    difx=xb-xr
    dify=yb-yr

    if (difx == 0.0):

        if(dify >= 0.0): theta=0.0
        if(dify < 0.0): theta=pi 

    else:

        slope=dify/difx
        if (abs(slope) < 1e-10):
            if(difx > 0): theta=pi2 
            if(difx < 0): theta=3*pi/2.0
        else:
            theta=atan(1./slope)
            if (difx > 0.0):
                if(dify < 0.0): theta=pi-theta
            else:
                if (dify > 0.):
                    theta=2*pi+theta
                else:
                    theta=pi+theta

    biasx=cos(theta)*(xa-xb)-sin(theta)*(ya-yb)
    biasy=sin(theta)*(xa-xb)+cos(theta)*(ya-yb)
    factor=cos(deg2rad*(blat+flat)*0.5)
    biasx=biasx*rearth*factor
    biasy=biasy*rearth*factor

    biasew=(xa-xb)*rearth*factor
    biasns=(ya-yb)*rearth*factor
    rr=sqrt(biasx*biasx+biasy*biasy)
    #dist_x=abs(biasx)
    #dist_y=abs(biasy)

    if(tcunits =='english'):
        rr=rr*km2nm
        biasx=biasx*km2nm
        biasy=biasy*km2nm
        biasew=biasew*km2nm
        biasns=biasns*km2nm


    if(verb):
        print "mmm ",blat,blon,flat,flon,rr,biasx,biasy

    return(rr,biasx,biasy,biasew,biasns)


def rumltlg(course,speed,dt,rlat0,rlon0):

    ####  print "qqq course,speed,dt,rlat0,rlon0\n"
    #c****	    routine to calculate lat,lon after traveling "dt" time
    #c****	    along a rhumb line specifed by the course and speed
    #c****	    of motion
    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #  assume speed is in kts and dt is hours
    #
    #      
    distnce=speed*dt

    icrse=int(course+0.01)

    if(icrse == 90.0 or icrse == 270.0):

    #      
    #*****		  take care of due east and west motion
    #
        dlon=distnce/(60.0*cos(rlat0*deg2rad))
        if(icrse == 90.0): rlon1=rlon0+dlon
        if(icrse == 270.0): rlon1=rlon0-dlon 
        rlat1=rlat0
    else:
        rlat1=rlat0+distnce*cos(course*deg2rad)/60.0
        d1=(45.0+0.5*rlat1)*deg2rad
        d2=(45.0+0.5*rlat0)*deg2rad
        td1=tan(d1)
        td2=tan(d2)
        #
        # going over the poles!
        #
        if(abs(rlat0) >= 90.0 or abs(rlat1) >= 90.0):
            rlat1=rlon1=None
        else:
            rlogtd1=log(td1)
            rlogtd2=log(td2)
            rdenom=rlogtd1-rlogtd2 
            rlon1=rlon0+(tan(course*deg2rad)*rdenom)*rad2deg

    return(rlat1,rlon1)




def basin2Chk(b2id):
    """
    convert local b2id to standard atcf b2id
    """

    if(b2id == 'SI' or b2id == 'SP' or b2id == 'SL'):
        b2id='SH'

    elif(b2id == 'AA' or b2id == 'BB' or b2id == 'NI' or b2id == 'NA'):
        b2id='IO'

    elif(b2id == 'AT'):
        b2id='AL'

    return(b2id)



def Clatlon2Rlatlon(clat,clon):

    if(len(clat) == 1):
        return(0.0,0.0)

    hemns=clat[len(clat)-1:]
    hemew=clon[len(clon)-1:]
    if(mf.find(clat,'.')):
        rlat=float(clat[0:(len(clat)-1)])
    else:
        ilat=clat[0:(len(clat)-1)]
        rlat=int(ilat)*0.1
        
    if(mf.find(clon,'.')):
        rlon=float(clon[0:(len(clon)-1)])
    else:
        ilon=clon[0:(len(clon)-1)]
        rlon=int(ilon)*0.1

    if(hemns == 'S'):
        rlat=-rlat

    if(hemew == 'W'):
        rlon=360.0-rlon

    return(rlat,rlon)

def Clatlon2RlatlonFull(clat,clon):

    if(len(clat) == 1):
        return(0.0,0.0,0,0,'X','X')

    hemns=clat[len(clat)-1:]
    hemew=clon[len(clon)-1:]
    ilat=clat[0:(len(clat)-1)]
    rlat=int(ilat)*0.1
    ilon=clon[0:(len(clon)-1)]
    rlon=int(ilon)*0.1

    if(hemns == 'S'):
        rlat=-rlat

    if(hemew == 'W'):
        rlon=360.0-rlon

    return(rlat,rlon,ilat,ilon,hemns,hemew)



def Rlatlon2ClatlonFull(rlat,rlon,dotens=1):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999

    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=mf.nint(rlat*10)
        else:
            ilat=mf.nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'

        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=mf.nint(rlon*10)
        else:
            ilon=mf.nint(rlon)

    if(dotens):
        clat="%03d%s"%(ilat,hemns)
        clon="%04d%s"%(ilon,hemew)
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
    else:
        clat="%2d%s"%(ilat,hemns)
        clon="%3d%s"%(ilon,hemew)

    return(clat,clon,ilat,ilon,hemns,hemew)



def Rlatlon2Clatlon(rlat,rlon,dotens=1,dodec=0,dozero=0):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999

    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=mf.nint(rlat*10)
        else:
            ilat=mf.nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'
            rlat=abs(rlat)

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'

        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=mf.nint(rlon*10)
        else:
            ilon=mf.nint(rlon)

    if(dotens):
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
        if(dozero):
            clat="%03d%s"%(ilat,hemns)
            clon="%04d%s"%(ilon,hemew)
    else:
        if(dozero):
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)
        else:
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)

    if(dodec):
        clat="%5.1f%s"%(rlat,hemns)
        clon="%5.1f%s"%(rlon,hemew)

    return(clat,clon)



def MakeAdeckCards(model,dtg,trk,stmid,ttaus=None,doString=0,verb=0):


    taus=trk.keys()
    taus.sort()

    stmid=stmid.upper()
    from ATCF import Aid
    AA=Aid(model)

    stmnum=stmid[0:2]
    basin1=stmid[2:3]
    basin2=Basin1toBasin2[basin1]
    adeckname=AA.AdeckName
    adecknum=AA.AdeckNum

    # use model name for adeckname AA return generic model name
    #
    adeckname=model.upper()

    acards=[]
    acardsString=''

    for tau in taus:

        if(ttaus != None and not(tau in ttaus)): continue
        
        itau=int(tau)

        vmax=-99
        pmin=0
        r34quad=None
        r50quad=None
        r64quad=None

        extra=None
        tt=trk[tau]
        for i in range(0,len(tt)):
            if(i == 0): lat=tt[i]
            if(i == 1): lon=tt[i]
            if(i == 2): vmax=tt[i]
            if(i == 3): pmin=tt[i]
            if(i == 4): r34quad=tt[i]
            if(i == 5): r50quad=tt[i]
            if(i == 6): r60quad=tt[i]
            if(i == 7): extra=tt[i]


        if(lat < -88.0 or lat > 88.0): continue

        ivmax=int(vmax)
        try:
            ipmin=int(pmin)
        except:
            ipmin=0

        if(ipmin < 0): ipmin=0

        (clat,clon,ilat,ilon,hemns,hemew)=Rlatlon2ClatlonFull(lat,lon)

        try:
            (r34ne,r34se,r34sw,r34nw)=r34quad
        except:
            r34ne=r34se=r34sw=r34nw=0

        try:
            (r50ne,r50se,r50sw,r50nw)=r50quad
            gotr50=1
        except:
            r50ne=r50se=r50sw=r50nw=0
            gotr50=0

        try:
            (r64ne,r64se,r64sw,r64nw)=r64quad
            gotr64=1
        except:
            r64ne=r64se=r64sw=r64nw=0
            gotr64=0

        acard1=''
        acard2=''
        acard3=''

        acard0="%2s, %2s, %10s, %2s, %4s, %3d,"%(basin2,stmnum,dtg,adecknum,adeckname,itau)

        if(extra == None):
            oextra=''
        else:
            oextra=" PMBR, %4d,"%(int(extra))

        # add \n at end of card to be consistent with real adecks
        #
        acard1=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  34, NEQ, %4d, %4d, %4d, %4d,%s\n"%\
            (ilat,hemns,ilon,hemew,ivmax,ipmin,r34ne,r34se,r34sw,r34nw,oextra)

        if(verb): print acard1[0:-1]
        acards.append(acard1)
        
        if(doString): acardsString=acardsString+acard1

        if(gotr50):
            acard2=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  50, NEQ, %4d, %4d, %4d, %4d,\n"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r50ne,r50se,r50sw,r50nw)
            acards.append(acard2)
            if(doString): acardsString=acardsString+acard2


        if(gotr64):
            acard3=acard0+" %3d%1s, %4d%1s, %3d, %4d,   ,  64, NEQ, %4d, %4d, %4d, %4d,\n"%\
                (ilat,hemns,ilon,hemew,ivmax,ipmin,r64ne,r64se,r64sw,r64nw)
            acards.append(acard3)
            if(doString): acardsString=acardsString+acard3

    if(doString): acards=acardsString

    return(acards)



def getHemis(stmids):

    rc=None
    hemis=[]
    for stmid in stmids:
        (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
        hemis.append(Basin1toHemi[b1id.upper()])

    if('nhem' in hemis and 'shem' in hemis): rc='global'
    if('nhem' in hemis and not('shem' in hemis)): rc='nhem'
    if('shem' in hemis and not('nhem' in hemis)): rc='shem'

    return(rc)

def stm1idTostm2id(stm1id):

    b1id=stm1id[2].upper()
    snum=stm1id[0:2]
    b2id=Basin1toBasin2[b1id]
    stm2id=b2id + snum + '.'+stm1id.split('.')[1]
    stm2id=stm2id.lower()
    return(stm2id)


def stm2idTostm1id(stm2id):

    ss=stm2id.split('.')
    sid=ss[0]
    syear=ss[1]

    b2id=sid[0:2].upper()
    if(mf.find(sid,'cc')):
        snum='CC'+sid[-3:]
    else:
        snum=sid[2:4]

    b1id=Basin2toBasin1[b2id]
    stm1id=snum + b1id + '.'+syear
    return(stm1id)



def getAdeckYearBasinFromPath(adeckpath):

    """recover 2-char basin id and year from adeck path"""

    adyear=None
    adbasin=None
    (dir,file)=os.path.split(adeckpath)
    (base,ext)=os.path.splitext(file)
    # -- check if standard adeck file name a??NNYYYY.dat
    #
    if( (ext.lower() == '.dat') and (len(base) == 9) ):
        adyear=base[-4:]
        adbasin=base[1:3]
    return(adyear,adbasin)
    
def scaledTC(vmax):

    stc=0.0
    if(vmax >= tdmin and vmax < tsmin):
        stc=0.25

    elif(vmax >= tsmin and vmax < tymin):
        dvmax=(vmax-tsmin)/(tymin-tsmin)
        stc=0.5+dvmax*0.5

    elif(vmax >= tymin and vmax < stymin):
        dvmax=(vmax-tymin)/(stymin-tymin)
        stc=1.0+dvmax*1.0

    elif(vmax >= stymin):
        stc=2.0

    return(stc)



def aceTC(vmax):
    if(vmax >= tsmin):
        ace=vmax*vmax
    else:
        ace=0.0
    return(ace)


def TCType(vmax):

    if(vmax <= 34): tctype='TD'
    if(vmax >= 35 and vmax <= 63): tctype='TS'
    if(vmax >= 64 and vmax <= 129): tctype='TY'
    if(vmax >= 130): tctype='STY'
    return(tctype)


def getSaffirSimpsonCat(vmax):

    if(vmax < 35.0): cat='TD'
    if(vmax >= 35.0 and vmax < 65.0): cat='TS'
    if(vmax >= 64.0 and vmax <= 82.0): cat='HU1'
    if(vmax >= 83.0 and vmax <= 95.0): cat='HU2'
    if(vmax >= 96.0 and vmax <= 113.0): cat='HU3'
    if(vmax >= 114.0 and vmax <= 135.0): cat='HU4'
    if(vmax > 135.0): cat='HU5'
    return(cat)


def getTyphoonCat(vmax):

    if(vmax < 35.0): cat='td'
    if(vmax >= 35.0 and vmax < 65.0): cat='ts'
    if(vmax >= 64.0 and vmax < 100.0): cat='ty'
    if(vmax >= 100.0 and vmax < 135.0): cat='Mty'
    if(vmax >= 135.0): cat='STY'
    return(cat)



def LatLonOpsPlotBounds(alats,alons,
                        latbuffPoleward=10.0,
                        latbuffEq=7.5,
                        lonbuff=10.0,
                        latinc=5.0,
                        loninc=5.0,
                        aspectmin=0.75,
                        dlonplotmax=80.0,
                        verb=0,
                        ):

    #
    # no lat/lons
    #
    if(len(alats) == 0):
        latplotmin=None
        latplotmax=None
        lonplotmin=None
        lonplotmax=None


    latmin=min(alats)
    latmax=max(alats)
    lonmin=min(alons)
    lonmax=max(alons)

    if(latmax < 0.0):
        latbuffS=latbuffPoleward
        latbuffN=latbuffEq
    else:
        latbuffN=latbuffPoleward
        latbuffS=latbuffEq

    latbar=(latmin+latmax)*0.5
    lonbar=(lonmin+lonmax)*0.5

    if(latmin < 0):
        nj1=int( (latmin/latinc)-0.5 )
        nj2=int( (latmax/latinc)-0.5 )
    else:
        nj1=int( (latmin/latinc)+0.5 )
        nj2=int( (latmax/latinc)+0.5 )

    nj3=int( (lonmin/loninc)+0.5 )
    nj4=int( (lonmax/loninc)+0.5 )

    j1=nj1*latinc
    j2=nj2*latinc
    j3=nj3*loninc
    j4=nj4*loninc

    latplotmin=j1-latbuffS
    latplotmax=j2+latbuffN
    lonplotmin=j3-lonbuff
    lonplotmax=j4+lonbuff

    dlonplot=lonplotmax-lonplotmin
    dlatplot=latplotmax-latplotmin

    aspect=dlatplot/dlonplot

    if(verb):
        print 'BBB (iter000) reftrk min,max: ',latmin,latmax,lonmin,lonmax
        print 'BBB (iter000) dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

    if(dlonplot > dlonplotmax):
        dlonplot=dlonplotmax
        print 'WWW (bounds): dlonplot > dlonplotmax: ',dlonplotmax,' set to dloplotmax'

    #
    # make initial adjustment
    #

    if(aspect < aspectmin):
        #dlatplot=dlonplot*aspectmin
        dlonplot=dlatplot/aspectmin
        dlatplot=int((dlatplot/latinc)+0.5)*latinc
        aspect=dlatplot/dlonplot
        if(verb):
            print 'BBB (iter---) 0000: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

    elif(aspect > aspectmin):

        #dlatplot=dlonplot*aspectmin
        dlonplot=dlatplot/aspectmin
        dlatplot=int((dlatplot/latinc)+0.5)*latinc
        aspect=dlatplot/dlonplot
        if(verb):
            print 'BBB (iter+++) 0000: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect,aspectmin


    #
    # iterate
    #

    if(aspect > aspectmin):

        while(aspect > aspectmin):
            dlonplot=dlonplot+loninc*0.5
            aspect=dlatplot/dlonplot
            if(verb):
                print 'BBB (iter+++) 1111: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

        if(latmax < 0.0):
            latplotmin=latplotmax-dlatplot
        else:
            latplotmax=latplotmin+dlatplot

    elif(aspect < aspectmin):

        while(aspect < aspectmin):
            dlatplot=dlatplot-latinc*0.5
            aspect=dlatplot/dlonplot
            if(verb):
                print 'BBB (iter---) 1111: dlatplot,dlonplot: ',dlatplot,dlonplot,' aspect: ',aspect

        if(latmax < 0.0):
            latplotmin=latplotmax-dlatplot
        else:
            latplotmax=latplotmin+dlatplot



    #
    # recenter in longitude
    #
    lonplotmin=j3-dlonplot*0.5
    lonplotmax=j4+dlonplot*0.5

    if(verb):
        print 'BBB (bounds): ','  latplotmin,latplotmax: ',latplotmin,latplotmax,'  lonplotmin,lonplotmax: ',lonplotmin,lonplotmax
        print 'BBB (bounds): ','           dlat/lonplot: ',dlatplot,dlonplot,'            aspect: ',aspect


    return(latplotmin,latplotmax,lonplotmin,lonplotmax)



def getStmName3id(stmid):

    stm3id=stmid.split('.')[0].upper()
    stmyear=stmid.split('.')[1]

    tcnames=GetTCnamesHash(stmyear)
    kk=tcnames.keys()

    stmname='unknown'
    stmname=stmname.upper()

    for k in kk:
        stm3=k[1]
        if(stm3 == stm3id): stmname=tcnames[k]

    return(stm3id,stmname)


def GetTCnamesHash(yyyy,source=''):

    ndir=TcNamesDatDir
    sys.path.append(ndir)
    if(source == 'neumann'):
        impcmd="from TCnamesNeumann%s import tcnames"%(yyyy)
    else:
        impcmd="from TCnames%s import tcnames"%(yyyy)
        exec(impcmd)
    return(tcnames)


def getSubbasinStmid(stmid):

    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    stm3id=stm1id.split('.')[0].upper()
    stmyear=stm1id.split('.')[1]
    
    tcnames=GetTCnamesHash(stmyear)

    kk=tcnames.keys()

    stmname='unknown'
    stmname=stmname.upper()

    stmFullid=stmid
    if(isIoShemSubbasinStm1id(stmid)):
        stmFullid=stmid
        return(stmFullid)


    # -- only look for IO/SHEM subbasins in the tcnames.keys() if not a specific io/shem subbasin, i.e., 'i' or 's' or 'h'
    #
    for k in kk:
        stm3=k[1]
        if(isIoShemSubbasin(stmid,stm3)):
            stmFullid="%s.%s"%(stm3,stmyear)
            return(stmFullid)

    return(stmFullid)





def isIoShemSubbasin(stm1id,stm2id,convertAlpha=0):

    # -- if [A-Z][0-9] 9x comes in, convert
    #
    chkstm1id=stm1id

    # -- really want to do this?
    #
    if(stm1id[0].isalpha() and convertAlpha):
        chkstm1id='9'+stm1id[1:]
        chkstm1id=chkstm1id.upper()

    rc=0
    bnum=(chkstm1id[0:2] == stm2id[0:2])
    b1id=(
        (chkstm1id[2] == 'S' and (stm2id[2] == 'S' or stm2id[2] == 'P')) or
        (chkstm1id[2] == 'I' and (stm2id[2] == 'A' or stm2id[2] == 'B'))
    )

    if(bnum and b1id): rc=1

    return(rc)

def isIoShemSubbasinStm1id(stm1id):
    """ only look for uniq b1id
"""
    rc=0
    b1id=stm1id[2].upper()
    btest=( (b1id == 'A' or b1id == 'B' or b1id == 'P') )
    if(btest): rc=1

    return(rc)

def getBasinOptFromStmids(tstmids):

    if(not(type(tstmids) is ListType)):
        tstmids=[tstmids]
    basins=[]
    for stmid in tstmids:
        b1id=stmid[2].lower()
        basin=b1id2tcgenBasin[b1id]
        basins.append(basin)

    basins=MF.uniq(basins)

    return(basins)
    

def get9XstmidFromNewForm(stmid9x):
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid9x)
    if(snum[0:2].upper() == 'XX'):
        stmid9x='XXX'+'.XXXX'
        stmid9x='___.____'
    elif(snum[0].isalpha()):
        stmid9x='9'+snum[1:]+b1id+'.'+year
    return(stmid9x)

def aceTC(vmax):
    if(vmax >= tsmin):
        ace=vmax*vmax
    else:
        ace=0.0
    return(ace)

def isXStimd(stmid):
    isXstm=0
    try:
        xx=int(stmid[1:3])
        isXstm=1
    except:
        isXstm=0
        
    return(isXstm)

def getStmParams(stmid,convert9x=0):

    istmid=stmid
    if(convert9x): istmid=get9XstmidFromNewForm(stmid)

    tt=istmid.split('.')

    # -- case of genesis stmid tgNNNNN
    #
    if(len(tt) == 1):
        year=-9999
        snum='-99'
        b1id='X'
        b2id='XX'
        stm2id='NNXX.YYYY'
        stm1id='NNX.YYYY'
        if(istmid[0:2] == 'tg'):     snum='-1'
        
        return(snum,b1id,year,b2id,stm2id,stm1id)

    else:
        year=tt[1]

    if(len(tt[0]) == 4):
        snum=istmid[2:4]
        b2id=istmid[0:2]
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=istmid
    elif(len(tt[0]) == 7):
        snum=istmid[4:7]
        b2id=istmid[0:2].lower()
        b1id=Basin2toBasin1[b2id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
    elif(len(tt[0]) == 6):
        snum=istmid[2:5]
        b1id=istmid.split('.')[0][-1]
        b2id=Basin1toBasin2[b1id.upper()]
        stm2id=b2id+'cc'+snum+'.'+year
        stm2id=stm2id.lower()
    else:
        isXstm=isXStimd(istmid)
        if(isXstm):
            # -- 20240926 -- special case of bdeck2 NOT having an adeck to detect warning
            #
            snum=istmid[1:3]
            b1id=istmid[0]
            b2id=Basin1toBasin2[b1id.upper()]
            stm1id=b1id+snum+'.'+year
            stm2id=b2id+snum+'.'+year
            stm2id=stm2id.lower()
            
        else:
            snum=istmid[0:2]
            b1id=istmid[2]
            b2id=Basin1toBasin2[b1id.upper()]
            stm2id=b2id+snum+'.'+year
            stm2id=stm2id.lower()
            stm1id=snum+b1id+'.'+year

    return(snum,b1id,year,b2id,stm2id,stm1id)

def getBD2stmid4Xstmid(istmid):
    ostmid=istmid
    if(isXStimd(istmid)):
        b1id=istmid[0]
        bnum=istmid[1:3]
        ostmid=bnum+b1id+istmid[3:]
    return(ostmid)
    

def get9Xnum(stmid):
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid,convert9x=1)
    
def Is9XSnum(snum):
    rc=0
    if(snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) ): rc=1
    return(rc)


def Is9X(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    
    # -- case where no 9x for a NN storm and the storm is coded as BNN.YYYY
    #
    isXstm=0
    try:
        xx=int(stmid[1:3])
        isXstm=1
    except:
        isXstm=0
        
    if(stmid[0:2].lower() == 'xx' or isXstm):
        rc=1
    elif((snum[0].isalpha() and int(snum[1]) >=0 and int(snum[1]) <= 9) or
       (snum.isdigit() and (int(snum) >= 90 and int(snum) <= 99) )
       ):
        rc=1

    return(rc)

def Is9XNN(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    
    # -- case where no 9x for a NN storm and the storm is coded as BNN.YYYY
    #
    try:
        xx=int(stmid[1:3])
        isXstm=1
    except:
        isXstm=0
    return(isXstm)


def IsNN(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if(
        (snum.isdigit() and (int(snum) >= 1 and int(snum) <= maxNNnum) )
        ):
        rc=1
    return(rc)

def IsNNWarn(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    if(
        (snum.isdigit() and (int(snum) >= 1 and int(snum) <= maxNNnum) and b1id != 'x')
        ):
        rc=1
        
    #print 'qq11',stmid,snum,b1id,year,rc
    return(rc)

def IsJtwcBasin(b1id):

    bid=b1id.lower()
    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1  and
       bid == 'w' or bid == 'b' or bid == 'a' or  bid == 'i' or
       bid == 's' or bid == 'p'
       ):
        rc=1

    # overlap
    #
    elif(len(bid) == 1  and
         bid == 'e' or bid == 'c'
         ):
        rc=2

    elif(len(bid) == 2 and
         bid == 'wp' or bid == 'io' or bid == 'sh'):
        rc=1

    # overlap
    #
    elif(len(bid) == 2 and
         bid == 'ep' or bid == 'cp'):
        rc=2

    return(rc)

def IsNhcBasin(b1id):

    bid=b1id.lower()

    if(len(bid) == 1):
        bid=b1id.lower()
    elif(len(bid) >= 3):
        # assume stmid if not 1char
        tt=b1id.split('.')
        bid=tt[0][2].lower()

    rc=0
    if(len(bid) == 1 and
       bid == 'l' or bid == 'e' or bid == 'c' or bid == 'q'
       ):
        rc=1
    elif(len(bid) == 2 and
         bid == 'al' or bid == 'ep' or bid == 'cp' or bid == 'sl'
         ):
        rc=1

    return(rc)

def IsTc(tcstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    # if undefined = -1
    #
    tcstate=tcstate.upper()

    if(
        tcstate == 'TD' or
        tcstate == 'TS' or
        tcstate == 'TY' or
        tcstate == 'HU' or
        tcstate == 'ST' or tcstate == 'STY' or
        tcstate == 'TC' 
        #or tcstate == 'TW' no -- this is a Tropical Wave
        ):
        tc=1
    elif(
        tcstate == 'SS' or
        tcstate == 'SD'
        ):
        tc=2
    elif(
        tcstate == 'EX'
        ):
        tc=3
    elif(
        tcstate == 'TW'
        ):
        tc=4
    elif(
        tcstate.lower() == 'xx' or
        tcstate == '  ' or
        len(tcstate) == 0
        ):
        tc=-1
    else:
        tc=0

    return(tc)

def IsTcWind(vmax):

    tc=0
    if(vmax >= TCvmin): tc=1
    return(tc)


def IsWarn(warnstate):
    #
    # if tc = 1
    # if stc = 2
    # if neither = 0
    #
    if(
        warnstate == 'WN'
        ):
        warn=1
    else:
        warn=0

    return(warn)



def IsValidStmid(stmid):
    rc=0
    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    rc=(IsNN(stmid) or Is9X(stmid) or int(snum) == -1)
    return(rc)

def pltHist(lista,listi,listo,
            stmopt,basin,year,
            tlist=None,
            ptitle2=None,
            filttype='season',
            donorm=1,
            docum=1,
            xmax=None,
            xmin=None,
            xint=None,
            ymax=None,
            ymin=0,
            yint=5,
            binint=None,
            dostacked=0,
            ptype='bar',
            var1='Dev',
            var2='NonDev',
            pngpath=None,
            doAllOnly=0,
            tag='',
            doshow=1,
            verb=0):

    import matplotlib.pyplot as plt
    from numpy import array,arange

    xa=array(lista)
    xi=array(listi)
    xo=array(listo)

    ymaxi=xi.max()
    try:
        ymaxi=x.max()
    except:
        ymaxi=undef
        
    try:
        ymaxo=xo.max()
    except:
        ymaxo=undef

    rca=SimpleListStats(lista,hasflag=0)
    rci=SimpleListStats(listi,hasflag=0)
    rco=SimpleListStats(listo,hasflag=0)
    
    meana=rca[0]
    
    mediana=rca[-3]
    sigmaa=rca[2]

    meani=rci[0]
    mediani=rci[-3]
    sigmai=rci[2]

    meano=rco[0]
    mediano=rco[-3]
    sigmao=rco[2]

    if(donorm):
        ymax=0.75
        yint=0.25

    pyaxis=None
    if(docum):
        ymax=1.0
        yint=0.25
        pyaxis=[0,0.25,0.50,0.75,0.90,1.0]


    if(xmax == None): xmax=15
    if(xmin == None): xmin=0
    if(xint == None): xint=1

    if(binint == None):
        nbins=(xmax/xint)
        nbins=nbins*5
    else:
        nbins=(xmax-xmin)/binint

    xa=lista

    hrange=[xmin,xmax]

    fc1='green'
    fc2='red'
    ec1='black'
    ec2='black'


    if(donorm or docum):
        ylab='prob [0-1]'
    else:
        ylab='N'

    nbins=nint(nbins)

    if(doAllOnly):

        (n1, bins, patches) = plt.hist(xa,bins=nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=0.75,rwidth=1.0)

        if(verb):
            print '1111111111111' ,n1,bins
        
        n2=n1
        
        


    elif(dostacked):

        ptype='barstacked'
        ptype='bar'

        xplot=(xi,xo)
    
        (n1, bins, patches) = plt.hist(xplot,nbins,histtype=ptype,range=hrange,\
                                       normed=donorm,cumulative=docum,
                                       color=['green', 'red'],
                                       alpha=1.0,rwidth=1.0)

    else:

        fa1=0.75
        fa2=1.0
        fr1=1.0
        fr2=0.50
        if(docum):
            fr1=fr2=0.25
            fa1=fa2=0.50
        
        (n1, bins, patches) = plt.hist(xi,nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc1,edgecolor=ec1,
                                       alpha=fa1,rwidth=fr1)

        
        (n2, bins, patches) = plt.hist(xo,nbins,histtype=ptype,range=hrange,\
                                       density=donorm,cumulative=docum,
                                       facecolor=fc2,edgecolor=ec2,
                                       alpha=fa2,rwidth=fr2)
        if(verb):
            print '1111111111111--n1--bins' ,n1,bins
            print '2222222222222--n2--bins ',n2,bins
        
        # -- make x&y for line plots if docum=1
        #
        if(docum):
            x=[]
            y90=[]
            for n in range(0,len(bins)-1):
                xb=(bins[n]+bins[n+1])*0.5
                x.append(xb)
                y90.append(0.9)
                
            y1=smooth(n1,window_len=7)
            y2=smooth(n2,window_len=7)
            rc=plt.plot(x,y1,color=fc1)
            rc=plt.plot(x,y2,color=fc2)
            rc=plt.plot(x,y90,color='black')


    ymax1=n1.max()
    ymax2=n2.max()

    if(ymax1 > ymax2):
        maxy=ymax1
    else:
        maxy=ymax2

    if(maxy >= 100):
        yint=20
    elif(maxy >= 50 and maxy < 100):
        yint=10
        
    if(ymax == None):
        ymax=int((float(maxy)/float(yint))+0.5 + 1)*float(yint)
    
        
    xs=[]
    for i in range(0,len(bins)-1):
        xs.append( (bins[i]+bins[i+1])*0.5 )

    def zerolt0(ys):
        oys=[]
        for y in ys:
            if(y < 0.0):
                oys.append(0.0)
            else:
                oys.append(y)
        return(oys)


    xlab='Nada'
    if(tlist == 'stmlife'):
        xlab='Storm Life [d]'

    elif(tlist == '9xlife'):
        xlab='pre-genesis 9X Life [d]'

    elif(tlist == 'latb'):
        xlab='Begin Latitude [deg]'

    elif(tlist == 'time2gen'):
        xlab='Time to Genesis [d]'

    plt.xlabel(xlab)
    plt.ylabel(ylab)

    if(ptitle2 == None):
        ptitle2="Basin: %s Stmopt: %s"%(basin,stmopt)

    if(tlist == 'time2gen'):

        ptitle="N: %d  Mn: %3.1f $\sigma$: %3.1f  Median: %3.1f\n%s"%(
            len(lista),meana,sigmaa,mediana,
            stmopt)

    elif(find(filttype,'dev')):

        ni=len(listi)
        no=len(listo)
        nn=no-ni
        devratio=(float(ni)/float(no))*100.0
        ptitle="%s(G) Ndev %d Mn: %3.1f $\sigma$: %3.1f\n%s(R) Nnon %d Mn: %3.1f $\sigma$: %3.1f \nForm Rate: %3.0f%%  %s"%(
            var1,ni,meani,sigmai,
            var2,nn,meano,sigmao,
            devratio,
            ptitle2)

    elif(find(filttype,'seas')):
        
        ndev=len(listi)
        ntot=len(listo)
        nnon=ntot-ndev
        ptitle="%s(G) Nd: %d Mn: %3.1f $\sigma$: %3.1f %s(R) Nn: %d Mn: %3.1f $\sigma$: %3.1f\n%s"%(
            var1,ndev,meani,sigmai,
            var2,nnon,meano,sigmao,
            stmopt)


        
    #ptitle="$\sigma=$"
    plt.title(r"%s"%(ptitle),fontsize=10)
    

   
    plt.xlim(xmin,xmax)
    xaxis=arange(xmin,xmax+1,xint)
    plt.xticks(xaxis)

    if(ymax != None):
        plt.ylim(ymin,ymax)
        yaxis=arange(ymin,ymax+0.001,yint)
        if(pyaxis != None):
            plt.yticks(pyaxis)

    plt.grid(True)

    if(pngpath == None):
        pngpath="/tmp/9x.%s.%s.png"%(basin,year)

    #print 'ppppppppppppppppppppppp ',pngpath
    plt.savefig(pngpath)
    
    doCp2Aori=0
    if(doCp2Aori):
        cmd="cp %s ~/pCloudDrive/AORI/TALKS/plt/"%(pngpath)
        runcmd(cmd)

    if(doshow): plt.show()

def SimpleListStats(dlist,verb=0,undef=-77,undef2=1e20,hasflag=1,flagval=None):
    """
    added undef2 which is semi-universal undef -- used in vdVM in processing VdeckS()
"""
    mean=0.0
    amean=0.0
    sigma=0.0
    mean2=0.0
    max=-1e20
    min=1e20
    
    odlist=[]
    n=0
    for ll in dlist:

        if(hasflag):
            flag=ll[0][0]
            val=ll[1]
            # -- if not a float set to undef
            if(type(val) is StringType): val=undef
        else:
            flag=1
            val=float(ll)
            
        # -- flag test
        #
        flagtest=(flag >= 1)
        if(flagval != None): flagtest=(flag == flagval)
        
        if(val == float(undef) or val == undef2): flagtest=0
                
        if(flagtest):
            odlist.append(val)
            mean=mean+val
            mean2=mean2+val*val
            amean=amean+fabs(val)
            if(val > max): max=val
            if(val < min): min=val
            if(verb):
                print 'stats n: ',n,'flag: ',flag,' val: ',val,' flagtest: ',flagtest
            n=n+1

    if(n > 0):
        mean=mean/float(n)
        amean=amean/float(n)
        var=mean2/float(n) - mean*mean
        if(fabs(var) > epsilonm5):
            sigma=sqrt(var)
        else:
            sigma=0.0
    else:
        mean=None
        amean=None
        sigma=None
        mean=amean=sigma=max=min=undef

    odlist.sort()
    if(n <= 1):
        ptl25=median=ptl75=ptl90=undef
    else:
        width=float(n-1)
        ptl25=width*0.25 ; n250=int(ptl25); n251=n250+1 ; d25=ptl25-n250
        ptl50=width*0.50 ; n500=int(ptl50); n501=n500+1 ; d50=ptl50-n500
        ptl75=width*0.75 ; n750=int(ptl75); n751=n750+1 ; d75=ptl75-n750
        ptl90=width*0.90 ; n900=int(ptl90); n901=n900+1 ; d90=ptl90-n900

        ptl25 =odlist[n250]*(1.0-d25) + odlist[n251]*d25
        median=odlist[n500]*(1.0-d50) + odlist[n501]*d50
        ptl75 =odlist[n750]*(1.0-d75) + odlist[n751]*d75
        ptl90 =odlist[n900]*(1.0-d90) + odlist[n901]*d90

        if(verb):
            print '50: ',n500,n501,d50,odlist[n500],odlist[n501],median
            print '25: ',n250,n251,d25,odlist[n250],odlist[n251],ptl25
            print '75: ',n750,n751,d75,odlist[n750],odlist[n751],ptl75
            print '90: ',n900,n901,d90,odlist[n900],odlist[n901],ptl90
    
    
    rc=(mean,amean,sigma,max,min,n,ptl25,median,ptl75,ptl90)
    return(rc)


def setFilter(filtopt,basin,stmopt):
    
    tt=filtopt.split('.')
    if(len(tt) != 3):
        print """EEE improper form of filtopt
FF.TT.NN
FF: all|season|dev|CC|CC-bt|CC-9x
TT: latb|latmn|stmlife|9xlife
NN: 0 - counts; 1 - donorm=1; 2 donorm=1,docum=1
"""
        sys.exit()


    filtBySeason=0
    filtByDev=0
    filtByCC=0

    tlist='stmlife'

    ymax=None
    yint=None
    xmax=10
    xmin=0
    xint=1

    ftype=tt[0]
    tlist=tt[1]
    dtype=int(tt[2])
    binint=0.25

    ptitle2="Basin: %s  stmopt: %s"%(basin.upper(),stmopt)
    
    if(find(ftype,'sea')): filtBySeason=1
    if(find(ftype,'dev')): filtByDev=1

    if(tlist == '9xlife'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.25
        binint=0.33
        
    elif(tlist == 'stmlife' or tlist == 'time2gen'):
        yint=5
        xmax=10
        xmin=0
        xint=1
        binint=0.5
        if(tlist == 'time2gen'):
            ptitle2="%s Time to Genesis Stmopt: %s"%(basin.upper(),stmopt)
        
    
    elif(tlist == 'latb'):
        yint=5
        xmax=45
        xmin=0
        xint=5
        binint=5

    donorm=0
    docum=0
    if(dtype == 1):donorm=1
    if(dtype == 2):donorm=1; docum=2

    return(filtBySeason,filtByDev,filtByCC,tlist,donorm,docum,
           ymax,yint,xmax,xmin,xint,binint,ptitle2)


def smooth(x,window_len=5,
           window='hanning',
           #window='flat',
           adjustWindowLen=1):

    import numpy

    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string   
    """

    if(x.size < window_len and adjustWindowLen): window_len=x.size-1
    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def uv2dirspd(u,v):
    sdir=atan2(u,v)*rad2deg
    if(sdir < 0.0): sdir=360.0+sdir
    sspd=sqrt(u*u+v*v)
    return(sdir,sspd)



def rumhdsp(rlat0,rlon0,rlat1,rlon1,dt,units='english',verb=0):

    verb=0

    if(verb):
        print "***** ",rlat0,rlon0,rlat1,rlon1,dt,units,opt

    if(units == 'metric'):
        distfac=111.19
        spdfac=0.2777
    else:
        distfac=60.0
        spdfac=1.0


    #
    # assumes deg W
    #
    rnumtor=(rlon0-rlon1)*deg2rad

    #
    #--- assume DEG E!!!!!!!!!!!!!!!!!!!!!!!!
    #

    rnumtor=(rlon1-rlon0)*deg2rad
    d1=(45.0+0.5*rlat1)*deg2rad
    d2=(45.0+0.5*rlat0)*deg2rad

    td1=tan(d1)
    td2=tan(d2)
    rlogtd1=log(td1)
    rlogtd2=log(td2)
    rdenom=rlogtd1-rlogtd2
    rmag=rnumtor*rnumtor + rdenom*rdenom

    course=0.0
    if(rmag != 0.0):
        course=atan2(rnumtor,rdenom)*rad2deg

    if(course <= 0.0):  
        course=360.0+course

    #
    #...     now find distance
    #

    icourse=int(course+0.1)
    if(icourse ==  90.0 or icourse == 270.0 ):
        distance=distfac*abs(rlon0-rlon1)*cos(rlat0*deg2rad)
    else:
        distance=distfac*abs(rlat0-rlat1)/abs(cos(course*deg2rad))

    #
    #...     now get speed
    #
    speed=distance/dt

    #
    #...      convert to u and v motion
    #

    spdmtn=speed*spdfac
    ispeed=int(spdmtn*100+0.5)/100
    angle=(90.0-course)*deg2rad

    umotion=spdmtn*cos(angle)
    vmotion=spdmtn*sin(angle)
    iumotion=int(umotion*100+0.5)/100
    ivmotion=int(vmotion*100+0.5)/100
    rumotion=float(iumotion)
    rvmotion=float(ivmotion)
    rcourse=float(course)
    rspeed=float(spdmtn)
    if(verb):
        print "%5.2f %4.0f %5.2f %5.2f %5.2f %5.2f\n"%\
              (distance,icourse,spdmtn,angle,umotion,vmotion)

    return(rcourse,rspeed,umotion,vmotion)



# -- MMMMMMMMMM -- sBT methods
#

def getShemYear(dtg):
    """
     convert year in stm dtg to basinyear
    """

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1
    cyyyy=str(yyyy)
    return(cyyyy)

def getStmopts(stmopt):
    
    ss=stmopt.split('.')
    bb=ss[0].split(',')
    yy=ss[1]

    if(len(yy) == 2):
        if(int(yy) <= 30): 
            yy='20%s'%(yy)
        else:
            yy='19%s'%(yy)

    stmopts=[]
    
    if(ss[0] == 'all'):
        for b1 in ['w','e','c','l','i','h']:
            stm="%s.%s"%(b1,yy)
            stmopts.append(stm)

    elif(len(bb) > 1):
        for b1 in bb:
            stm="%s.%s"%(b1,yy)
            stmopts.append(stm)
    else:
        bb=ss[0]
        stmopt="%s.%s"%(bb,yy)
        stmopts.append(stmopt)
        
    return(stmopts)
            


def getPyp(pyppath):

    ppath=pyppath

    if(os.path.exists(ppath)):
        PS=open(ppath)
        pyp=pickle.load(PS)
        PS.close()
        return(pyp)
    else:
        return(None)


def putPyp(pyp,pyppath):

    ppath=pyppath
    pyppckle=pyp

    try:
        PS=open(ppath,'w')
        pickle.dump(pyppckle,PS)
        PS.close()
    except:
        print 'EEEEE unable to pickle.dump: ',ppath
        sys.exit()


def printTrk(stmid,dtg,rlat,rlon,vmax,pmin,
             dir=-999,spd=-999,dirtype='X',
             tdo='---',
             tccode='XX',
             wncode='XX',
             ntrk=0,
             ndtgs=0,
             r34m=None,
             r50m=None,
             alf=None,
             sname='---------',
             gentrk=0,
             doprint=1):

    (clat,clon)=Rlatlon2Clatlon(rlat,rlon,dodec=1)

    if(vmax == None or vmax == undef or vmax == 0):  cvmax='---'
    else:              cvmax="%03d"%(vmax)
    if(pmin == None):  cpmin='----'
    else:              cpmin="%4d"%(pmin)

    if(r34m == None or r34m == undef):
        cr34m='---'
    else:
        cr34m="%3.0f"%(float(r34m))

    if(r50m == None or r50m == undef):
        cr50m='---'
    else:
        cr50m="%3.0f"%(r50m)

    # -- if first posit set to 360.0 and -0 spd
    #
    if(dir == -999.): dir=360.0
    if(spd == -999.): spd=-0.0

    cdir="%5.1f"%(dir)
    cspd="%4.1f"%(spd)

    if(alf == None or alf == undef):
        clf='----'
    else:
        clf="%4.2f"%(alf)

    if(gentrk):
        card="%s* %12s "%(dtg,stmid.upper())
    else:
        card="%s  %12s "%(dtg,stmid.upper())

    if(tdo == 'NaN' or tdo == ''): tdo='---'
    card=card+"%s %s %s  %s  %s %s"%(cvmax,cpmin,clat,clon,cr34m,cr50m)
    card=card+"  %s %s %s  %3s %s  %s"%(cdir,cspd,dirtype,tccode,wncode,tdo)
    card=card+" %3d/%-3d lf: %s %-9s"%(ntrk,ndtgs,clf,sname[0:9])
    if(gentrk): card=card+" <**Genesis"
    if(doprint): print card
    return(card)

def printMd3Trk(md3trk,dtg,doprint=0):

    (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tccode,wncode,
     roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=md3trk
        
    card=printTrk(ostmid,dtg,rlat,rlon,vmax,pmin,
                   tdir,tspd,tdo=tdo,
                   tccode=tccode,wncode=wncode,
                   r34m=r34m,r50m=r50m,alf=alf,
                   sname=ostmname,doprint=0)
    
    if(doprint):
        print card
        
    return(card)


def mergeMd3Cvs(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}
    btcards=[]

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=btcard
        mcardsbt[dtg]=btcard
        
        
    dtgs=mcards.keys()
    dtgs.sort()

    for dtg in dtgs:
        mcard=mcards[dtg]
        ocards.append(mcard)
        try:
            mcardb=mcardsbt[dtg]
        except:
            None
            mcardb='nnnooobbbttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt'
            
        if(verb):
            print 'dtg: ',dtg,'  M:',mcard[0:50],'  B:',mcardb[0:50]
        
    return(ocards)
        
    
def setCvsYearOptPaths(sbtSrcDir,oyearOpt,headAll,headSum,doMergeOnly=1,doWBTonly=0):
    
    allCvsPath="%s/all-md3-%s.csv"%(sbtSrcDir,oyearOpt)
    allCvsPathBT="%s/all-md3-%s-BT.csv"%(sbtSrcDir,oyearOpt)
    allCvsPathMRG="%s/all-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)

    sumCvsPath="%s/sum-md3-%s.csv"%(sbtSrcDir,oyearOpt)
    sumCvsPathBT="%s/sum-md3-%s-BT.csv"%(sbtSrcDir,oyearOpt)
    sumCvsPathMRG="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)
    

    if(doMergeOnly):
        
        if(MF.ChkPath(allCvsPathMRG)):
            cmd='rm  %s'%(allCvsPathMRG)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPathMRG)):
            cmd='rm  %s'%(sumCvsPathMRG)
            runcmd(cmd)
        
        cmd="cat %s > %s"%(headAll,allCvsPathMRG)
        runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPathMRG)
        runcmd(cmd)

        return(allCvsPathMRG,sumCvsPathMRG)
        
    else:
        
        if(MF.ChkPath(allCvsPath)):
            cmd='rm  %s'%(allCvsPath)
            runcmd(cmd)
    
        if(MF.ChkPath(allCvsPathBT)):
            cmd='rm  %s'%(allCvsPathBT)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPath)):
            cmd='rm  %s'%(sumCvsPath)
            runcmd(cmd)
        
        if(MF.ChkPath(sumCvsPathBT)):
            cmd='rm %s'%(sumCvsPathBT)
            runcmd(cmd)
            
        # -- headers
        #
        cmd="cat %s > %s"%(headAll,allCvsPath)
        runcmd(cmd)

        if(not(doWBTonly)):
            cmd="cat %s > %s"%(headAll,allCvsPathBT)
            runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPath)
        runcmd(cmd)
        
        cmd="cat %s > %s"%(headSum,sumCvsPathBT)
        runcmd(cmd)
            
        return(allCvsPath,allCvsPathBT,sumCvsPath,sumCvsPathBT)

def setCvsSbtYearOptPaths(sbtSrcDir,oyearOpt,version,headAll,dorm=0):
    
    allCvsPath="%s/sbt-%s-%s-MRG.csv"%(sbtSrcDir,version,oyearOpt)
    sumCvsPath="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOpt)

    if(MF.ChkPath(allCvsPath) and dorm):
        cmd='rm  %s'%(allCvsPath)
        runcmd(cmd)
    
    cmd="cat %s > %s"%(headAll,allCvsPath)
    runcmd(cmd)
    
    return(allCvsPath,sumCvsPath)

def setCvsSbtFinalPaths(sbtDir,
                        oyearOpt='2007-2022',
                        oyearOptMd3='2007-2023'):
    
    sbtCvsPath="%s/sbt-%s-%s-MRG.csv"%(sbtSrcDir,version,oyearOpt)
    
    md3CvsPath="%s/all-md3-%s-MRG.csv"%(sbtSrcDir,oyearOptMd3)
    sumCvsPath="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOptMd3)

    md3CvsPathP1="%s/all-md3-%s-MRG.csv"%(sbtSrcDir,oyearOptMd3)
    sumCvsPathP1="%s/sum-md3-%s-MRG.csv"%(sbtSrcDir,oyearOptMd3)

    if(MF.ChkPath(allCvsPath) and dorm):
        cmd='rm  %s'%(allCvsPath)
        runcmd(cmd)
    
    cmd="cat %s > %s"%(headAll,allCvsPath)
    runcmd(cmd)
    
    return(allCvsPath,sumCvsPath)

def getBasin4b1id(b1id):
    ib1id=b1id.lower()
    if(ib1id == 'l'):
        basin='lant'
    elif(ib1id == 'w'):
        basin='wpac'
    elif(ib1id == 'e' or ib1id == 'c'):
        basin='epac'
    elif(ib1id == 'i' or ib1id == 'b' or ib1id == 'a'):
        basin='io'
    elif(ib1id == 'h' or ib1id == 's' or ib1id == 'p'):
        basin='shem'
    else:
        print 'EEE in getBasin4b1id b1id: ',b1id
        sys.exit()
        
        
    return(basin)
        
def mkFloat(var,convU2Uvar=0):
    ovar=undef
    if(var != 'NaN' and var != ''): 
        ovar=float(var)
    if(convU2Uvar and ovar == undef):
        ovar=undefVar
        
    return(ovar)

def mkFloatU(var,convU2Uvar=1):
    ovar=undef
    if(var != 'NaN' and var != ''): 
        ovar=float(var)
    if(convU2Uvar and ovar == undef):
        ovar=undefVar
        
    return(ovar)


def setMd3track(m3trk,stmid,verb=0):
    
    def interpM3trk(m1,m2,f1,f2):
        
        def dointerp(v1,v2,f1,f2):
            if(v1 != undef and v1 != undef): vi=v1*f1+v2*f2
            if(v1 != undef and v2 == undef): vi=v1
            if(v2 != undef and v1 == undef): vi=v2
            if(v1 == undef and v2 == undef): vi=undef
            return(vi)
            
            
        (rlat1,rlon1,vmax1,pmin1,tdir1,tspd1,r34m1,r50m1,tcstate1,warn1,roci1,poci1,alf1,depth1,eyedia1,tdo1,ostmid1,ostmname1,r341,r501)=m1
        (rlat2,rlon2,vmax2,pmin2,tdir2,tspd2,r34m2,r50m2,tcstate2,warn2,roci2,poci2,alf2,depth2,eyedia2,tdo2,ostmid2,ostmname2,r342,r502)=m2
        
        rlati=rlat1*f1+rlat2*f2
        rloni=rlon1*f1+rlon2*f2
        vmaxi=dointerp(vmax1,vmax2,f1,f2)
        pmini=dointerp(pmin1,pmin2,f1,f2)
        tdiri=dointerp(tdir1,tdir2,f1,f2)
        tspdi=dointerp(tspd1,tspd2,f1,f2)
        r34mi=dointerp(r34m1,r34m2,f1,f2)
        r50mi=dointerp(r50m1,r50m2,f1,f2)
        tcstatei=tcstate1
        warni=warn1
        rocii=dointerp(roci1,roci2,f1,f2)
        pocii=dointerp(poci1,poci2,f1,f2)
        alfi=dointerp(alf1,alf2,f1,f2)
        depthi=depth1
        eyediai=eyedia1
        tdoi=tdo1
        ostmidi=ostmid1
        ostmnamei=ostmname1
        r34i=r341
        r50i=r501
        
        mi=(rlati,rloni,vmaxi,pmini,tdiri,tspdi,r34mi,r50mi,tcstatei,warni,rocii,pocii,alfi,depthi,eyediai,tdoi,ostmidi,ostmnamei,r34i,r50i)
        return(mi)
        
    # -- check if we need to interpolate for missing dtgs
    #
    idtgs=m3trk.keys()
    idtgs.sort()
    fdtgs=dtgrange(idtgs[0],idtgs[-1],6)
    li=len(idtgs)
    lf=len(fdtgs)
    
    # -- we do need to interpolate... can handle 12 and 18 gaps
    
    if(li != lf):
    
        mdtgs=[]
        if(verb): print 'li lf',stmid,li,lf
        for n in range(0,lf):
            fdtg=fdtgs[n]
            try:
                m3i=m3trk[fdtg]
            except:
                
                dtg1=fdtgs[n-1]
                indx=idtgs.index(dtg1)
                dtg2=idtgs[indx+1]
                
                if(verb): print 'have to interpolate...',fdtg,'dtg1 2',dtg1,dtg2
                # -- do the interpolation here...
                #
                dtgib=dtginc(dtg1,+6)
                dtgie=dtginc(dtg2,-6)
                dtgis=dtgrange(dtgib, dtgie)
                iden=dtgdiff(dtg1, dtg2)
                
                if(iden > 36.0):
                    print'EEE --setMd3track big--- iterp interval for stmid',stmid,dtg1,dtg2,iden
                    sys.exit()
                
                m1=m3trk[dtg1]
                m2=m3trk[dtg2]
    
                for dtgi in dtgis:
    
                    inum1=dtgdiff(dtg1, dtgi)
                    inum2=dtgdiff(dtgi,dtg2)
    
                    f1=inum2/iden
                    f2=inum1/iden
                
                    if(verb): print 'interp for dtg',dtg1,dtgi,dtg2,inum1,inum2,f1,f2
                    m3trk[dtgi]=interpM3trk(m1,m2,f1,f2)
                    mdtgs.append(dtgi)
                    n=n+1
                n=n+1
                
    return(m3trk)
    
    
    

def parseMd3Card(mm,dobt=0,verb=0):
    
    #n:  0 2019122118
    #n:  1 30w.2019
    #n:  2 PHANFONE
    #n:  3 TY
    #n:  4 NN
    #n:  5 6.4
    #n:  6 139.9
    #n:  7 30
    #n:  8 1002
    #n:  9 293
    #n: 10 14
    #n: 11 293
    #n: 12 14
    #n: 13 NaN
    #n: 14 NaN
    #n: 15 NaN
    #n: 16 NaN
    #n: 17 NaN
    #n: 18 NaN
    #n: 19 NaN
    #n: 20 NaN
    #n: 21 NaN
    #n: 22 NaN
    #n: 23 TD
    #n: 24 WN
    #n: 25 B  dirtype
    #n: 26 B  posttype
    #n: 27 140
    #n: 28 1006
    #n: 29 NaN
    #n: 30 S
    #n: 31 30
    #n: 32 RCB
 
    if(verb == 2):
        for n in range(0,len(mm)):
            print 'n: %2d'%(n),mm[n]
        sys.exit()
        
    dtg=mm[0]
    ostmid=mm[1]

    ostmname=mm[2].strip()
    tcstate=mm[3].strip()
    stmDev=mm[4].strip()
    
    # -- handle NN here vice with dobt and continue if 9X
    #
    if(dobt and ((IsNN(ostmid) and stmDev != 'NN') or (Is9X(ostmid)) ) ):
        return(None)
        
    n=5
    rlat=mm[n] ; n=n+1
    rlon=mm[n] ; n=n+1
    vmax=mm[n] ; n=n+1
    pmin=mm[n] ; n=n+1
    cdir=mm[n] ; n=n+1
    cspd=mm[n] ; n=n+1
    tdir=mm[n] ; n=n+1
    tspd=mm[n] ; n=n+1
    
    # -- get full r34
    #
    r34m=mm[n] ; n=n+1
    r34ne=mm[n] ; n=n+1
    r34se=mm[n] ; n=n+1
    r34sw=mm[n] ; n=n+1
    r34nw=mm[n] ; n=n+1

    # -- get full r50
    #
    r50m=mm[n]  ; n=n+1
    r50ne=mm[n] ; n=n+1
    r50se=mm[n] ; n=n+1
    r50sw=mm[n] ; n=n+1
    r50nw=mm[n] ; n=n+1
    
    tcstate=mm[n] ; n=n+1
    warn=mm[n] ; n=n+1
    dirtype=mm[n] ; n=n+1
    posttype=mm[n] ; n=n+1
    
    roci=mm[n] ; n=n+1
    poci=mm[n] ; n=n+1
    
    alf=mm[n] ; n=n+1
    depth=mm[n] ; n=n+1
    eyedia=mm[n] ; n=n+1
    tdo=mm[n].strip() 
    
    if(dirtype == ''):
        dirtype='NaN'
    if(posttype == ''):
        posttype='NaN'
        
    rlat=float(rlat)
    rlon=float(rlon)
    tdir=mkFloat(tdir)
    tspd=mkFloat(tspd)
    vmax=mkFloat(vmax)
    pmin=mkFloat(pmin)

    r34m=mkFloat(r34m)
    r34ne=mkFloat(r34ne)
    r34se=mkFloat(r34se)
    r34sw=mkFloat(r34sw)
    r34nw=mkFloat(r34nw)
    
    r50m=mkFloat(r50m)
    r50ne=mkFloat(r50ne)
    r50se=mkFloat(r50se)
    r50sw=mkFloat(r50sw)
    r50nw=mkFloat(r50nw)
    
    
    if(alf == 'NaN' or alf == ''): alf=0.0
    else:                          alf=float(alf)

    roci=mkFloat(roci)
    poci=mkFloat(poci)
    
    #if(warn == 'NaN' or warn == ''): warn='--'
    #if(depth == 'NaN' or depth == ''): depth='-'
    
    eyedia=float(eyedia)
    r34=(r34ne,r34se,r34sw,r34nw)
    r50=(r50ne,r50se,r34sw,r50nw)

    #if(verb):
        #print 'rrrrr',dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,ostmid

    rc=(dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
    return(rc)


def makeMd3Card(dtg,m3t,m3i,m2t,useM3Iname=0,verb=0):

    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
    
    
    #n:  0 2019122118
    #n:  1 30w.2019
    #n:  2 PHANFONE
    #n:  3 TY
    #n:  4 NN
    #n:  5 6.4
    #n:  6 139.9
    #n:  7 30
    #n:  8 1002
    #n:  9 293
    #n: 10 14
    #n: 11 293
    #n: 12 14
    #n: 13 NaN
    #n: 14 NaN
    #n: 15 NaN
    #n: 16 NaN
    #n: 17 NaN
    #n: 18 NaN
    #n: 19 NaN
    #n: 20 NaN
    #n: 21 NaN
    #n: 22 NaN
    #n: 23 TD
    #n: 24 WN
    #n: 25 B  dirtype
    #n: 26 B  posttype
    #n: 27 140
    #n: 28 1006
    #n: 29 NaN
    #n: 30 S
    #n: 31 30
    #n: 32 RCB
    
        
    ostmid=m3i[0]
    ostmname=m3i[1].strip()
    if(Is9X(ostmid)):
        ostmname="9X-%s"%(ostmid.split('.')[0].upper())
    tctype=m3i[2].strip()
    stmDev=m3i[3].strip()
    
    if(verb):
        print 'mmm',dtg,m3t[0:9],m3i,len(m3t),len(m3i),m2t.sname,m2t.stmid
        print '000',dtg,ostmid,ostmname,tctype,stmDev
    #(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn

    n=0
    nb=n
    rlat=m3t[n] ; n=n+1
    rlon=m3t[n] ; n=n+1
    vmax=m3t[n] ; n=n+1
    pmin=m3t[n] ; n=n+1
    trkdir=m3t[n] ; n=n+1
    trkspd=m3t[n] ; n=n+1
    r34m=m3t[n] ; n=n+1
    r50m=m3t[n] ; n=n+1
    tccode=m3t[n] ; n=n+1
    wncode=m3t[n] ; n=n+1
    
    if(verb):
        print 'mmm',nb,n,m3t[nb:n]
        print '111',rlat,rlon,vmax,pmin,trkdir,trkspd,r34m,r50m,tccode,wncode
        
    nb=n
    #(roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
    roci=m3t[n] ; n=n+1
    poci=m3t[n] ; n=n+1
    alf=m3t[n] ; n=n+1
    depth=m3t[n] ; n=n+1
    eyedia=m3t[n] ; n=n+1
    tdo=m3t[n].strip() ; n=n+1
    
    if(verb):
        print 'mmm',nb,n,m3t[nb:n]
        print '222',roci,poci,alf,depth,eyedia,tdo

    nb=n
    ne=len(m3t)
    ostmidm3=m3t[n] ; n=n+1
    ostmname3=m3t[n] ; n=n+1
    if(not(useM3Iname)): ostmname=ostmname3
    r34=m3t[n] ; n=n+1
    r50=m3t[n] ; n=n+1
    
    if(verb):
        print 'mmm',nb,ne,m3t[nb:ne]
        print '333',ostmidm3,ostmname,r34,r50

    # -- this done below
    3
    #r34ne=r34[0]
    #r34se=r34[1]
    #r34sw=r34[2]
    #r34nw=r34[3]

    ## -- get full r50
    ##
    #r50ne=r50[0]
    #r50se=r50[1]
    #r50sw=r50[2]
    #r50nw=r50[3]
    #print '444',r34ne,r34se,r34sw,r34nw,'50',r50ne,r50se,r50sw,r50nw
        
    # -- 2222222222222222222222222222 - from m2.trk object made in class MD3trk
    #
    cdir=m2t.dir         #275.449145529
    dirtype=m2t.dirtype   #B
    ndtgs=m2t.ndtgs       #40
    ntrk=m2t.ntrk         #19
    posttype=m2t.postype  #B
    cspd=m2t.spd          #15.7957548819
    stmid=m2t.stmid.lower()      #30W.2019
    stmidm2=stmid
    sname=m2t.sname
    undef=m2t.undef      #-999
    rmax=m2t.rmax        #15
    
    # -- use m3 sname
    #
    sname=ostmname
    if(sname != None and sname != undef and len(sname) > 0):
        osname="%-15s"%(sname)
    else:
        osname="%-15s"%('NaN')
 
    oroci='NaN'
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='NaN '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)

    ovmax='NaN '
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='NaN '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34m != None and r34m != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34=' NaN , NaN , NaN , NaN ,'
        or34m='NaN , '
    
    got50=0
    if(r50m != None and r50m!= undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50=' NaN , NaN , NaN , NaN ,'
        or50m=' NaN , '
        if(got34):
            or50m='NaN , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth=' %s '%(depth)
        

    odtgstm="%s , %s , %s , %s , %s ,"%(dtg,ostmid,osname,tctype,stmDev)
    omotion="%3.0f , %2.0f , "%(cdir,cspd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf=' NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    tdo=tdo.strip()
    if(tdo == '---' or tdo == ''): tdo='NaN'
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm,stmidm2,stmid,ostmid
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    ocard=ocard.replace(' ','')
    ocard=ocard+','
    if(verb): print 'ooo---ooo',ocard
    return(ocard)
    
    

def parseStmSumCard(card):
    
    tt=card.split(",")
    tstmid=tt[0]
    sname=tt[3]
    bdtg=tt[9]
    edtg=tt[10]
    stm9x=tt[22]
    t2gen=tt[23]
    dtggen=tt[24].strip()
    rc=(tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)
    return(rc)
    

def getTcData(year,basin):
    
    if(basin =='shem'):
        stmopt='h.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='io'):
        stmopt='i.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='epac'):
        stmopt='c.%s,e.%s'%(year,year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='lant'):
        stmopt='l.%s'%(year)
        tD=TcData(stmopt=stmopt)
    elif(basin =='wpac'):
        stmopt='w.%s'%(year)
        tD=TcData(stmopt=stmopt)
    return(tD)

def getMd3path(tstmid):
    
    rc=getStmParams(tstmid)
    stm3id="%s%s"%(rc[0],rc[1])
    stm3id=stm3id.upper()
    
    tyear=rc[2]
    tmask="%s/%s/*/%s*"%(sbtSrcDir,tyear,stm3id)
    odirs=glob.glob("%s"%(tmask))
    if(len(odirs) == 1):
        sdir=odirs[0]
    else:
        print 'EEE -- finding sdir in getMd3path for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
        sys.exit()

    if(IsNN(tstmid)):
        md3mask="%s/*-%s-md3-BT.txt"%(sdir,tyear)
        md3paths=glob.glob(md3mask)
    else:
        md3mask="%s/*-%s-md3.txt"%(sdir,tyear)
        md3paths=glob.glob(md3mask)
        
    if(len(md3paths) == 1):
        md3path=md3paths[0]
    else:
        print 'EEE -- finding md3path in getMd3Spath for sbtSrcDir: ',sbtSrcDir,' tstmid: ',tstmid,'sayounara'
        sys.exit()
        
    return(md3path)
    


def getTstmidsSum(year,basin,spath,ropt='norun',doBTonly=0,verb=0):
    
    (ddir,ffile)=os.path.split(spath)
    cards=open(spath).readlines()
    
    basinStm={}
    allStm={}
    for card in cards:
        
        if(verb):
            n=0
            tt=card.split(',')
            for n in range(0,len(tt)):
                print 'n: %2d'%(n),tt[n]
        
        rc=parseStmSumCard(card)
        (tstmid,bdtg,edtg,sname,stm9x,t2gen,dtggen)=rc
        
        # -- option to do BT only
        #
        if(doBTonly and not(IsNN(stm1id))):
            continue

        basinStm[rc[0]]=(bdtg,edtg,sname,stm9x,t2gen,dtggen)
        
    bstmids=basinStm.keys()
    for bstmid in bstmids:
        allStm[bstmid]=basinStm[bstmid]
        

    return(allStm)    



def getMd3trackSpath(md3path,dobt=0,verb=0):
    
    m3trk={}
    m3info={}
        
    stmcards=open(md3path).readlines()

    for m3card in stmcards:

        mm=m3card.split(',')
        rc=parseMd3Card(mm,dobt=dobt,verb=verb)
        if(rc == None):continue

        (dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,
         tcstate,warn,
         roci,poci,alf,
         depth,eyedia,tdo,ostmid,ostmname,r34,r50)=rc
        m3info[dtg]=mm[1:5]
        if(verb):
            print 'rrrrr',dtg,rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,ostmid
        m3trk[dtg]=(rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)
        
    return(m3trk,m3info)
    


def getTstmidsSumOLD(year,basin,spath,ropt='norun',doBTonly=0):
    
    (ddir,ffile)=os.path.split(spath)
    cards=open(spath).readlines()
    tstmids=[]
    
    for card in cards:
        tt=card.split(":")
        stm3id=tt[0].split()[1]
        stm1id="%s.%s"%(stm3id,year)
        
        # -- option to do BT only
        #
        if(doBTonly and not(IsNN(stm1id))):
            continue

        tstmids.append(stm1id)

    return(tstmids)    



def getTstmidsByYearBasin(years,basins,stbdir):
    
    tstmids=[]
    for year in years:
        tdir="%s/%s"%(stbdir,year)
        MF.ChkDir(tdir,'mk')
        
        for basin in basins:
            spath="%s/stm-%s-%s.txt"%(tdir,basin,year)
            tstmids=tstmids+getTstmidsSum(year,basin,spath)
    
    return(tstmids)        

    
def getPrStatus(tstmid,oPrsiz,oPrpath,verb=0):
    
    def getstatus(siz):
        if(siz < 0):
            stat=0
        elif(siz == 0):
            stat=-1
        else:
            stat=1
        return(stat)
        
    dPr=MF.PathCreateTime(oPrpath)
    prdtg=dPr[1]
    curdtg=dtg('dtgcurhr')
    #print 'adsf',curdtg,prdtg
    sPrdiff=mf.dtgdiff(prdtg,curdtg)
    sPr=getstatus(oPrsiz)

    if(verb):
        print 'tstmid: %s'%(tstmid),' sPr: ',sPr
        
    card="%s sPr: %d sPrdiff: %d"%(tstmid,sPr,int(sPrdiff))
    
    return(card)
        
    
def getTClatlonNew(bdtg,tau,m3trk,undef=-999,verb=0):

    tdtg=dtginc(bdtg,tau)

    rlat=rlon=tdir=undef
    try:
        trk=m3trk[tdtg]
    except:
        print 'WWW -- no BT for tdtg: ',tdtg
        return(rlat,rlon,tdir)
    
    (rlat,rlon,vmax,pmin,tdir,tspd,r34m,r50m,tcstate,warn,roci,poci,alf,depth,eyedia,tdo,ostmid,ostmname,r34,r50)=trk
    if(tdir == undef): tdir=270.0
    
    if(verb): print 'md3:',rlat,rlon,tdir
    
    return(rlat,rlon,tdir)


def getEraTrk(eraDir,tstmid,model,dtg,verb=0):
    
    etrk={}
    
    tdmask="%s/tcmeta.*%s*"%(eraDir,tstmid.lower())
    tdfiles=glob.glob(tdmask)
    if(len(tdfiles) == 1):
        trkpath=tdfiles[0]
        print 'TTT trkpath: ',trkpath
    else:
        print 'NOOOOO ERA5 tcmeta for: ',tstmid,'dtg: ',dtg,' return etrk={}'
        return(etrk)
    
    if(MF.getPathSiz(trkpath) > 0):
        cards=open(trkpath).readlines()
    else:
        print 'EEE - no tcmeta at ',trkpath
        return(etrk)

    if(len(cards) == 1):
        print 'EEE-badTCmeta in getEraTrk: ',trkpath
        return(etrk)

    sname=cards[0].split()[-1]
    ntaus=cards[1].split()[-2]
    
    
    for card in cards[2:]:
        tt=card[0:-1].split()
        tau=int(tt[0])
        elat=float(tt[1])
        elon=float(tt[2])
        epmin=float(tt[-3])
        edir=float(tt[-2])
        espd=float(tt[-1])
    
        etrk[tau]=(elat,elon,edir,epmin,espd)
        if(verb): print 'eeeeeeeeeeeeeeee',tau,elat,elon,epmin,edir,espd
        
    return(etrk)

def makePrCard(dtgdat,tcdat,ctpr6bm,ctpr6em,gtpr6bm,gtpr6em,itpr6bm,itpr6em,eprm,eprmc,
               doRad=0,verb=0):
    
    (tstmid,dtg,tau)=dtgdat
    card1="%10s , %s , "%(tstmid,dtg)

    (pblat,pblon,pbdir,pelat,pelon,pedir)=tcdat
    cardb="BT:, %5.1f , %5.1f , %3.0f , "%(pblat,pblon,pbdir)
    carde='E5:, %5.1f , %5.1f , %3.0f , '%(pelat,pelon,pedir)
    card1=card1+cardb+carde
    
    kk=ctpr6bm.keys()
    kk.sort()

    if(doRad):
        cardpr="rad, "
        for k in kk:
            r=radInfPrKM[k]
            cardpr=cardpr+"%3d , "%(r)
    else:
        cardpr=''
        
    cardpr=cardpr+'obBT, '
    for k in kk:
        c6bm=float(ctpr6bm[k])
        g6bm=float(gtpr6bm[k])
        i6bm=float(itpr6bm[k])
        cardpr=cardpr+"C%-5.1f , G%-5.1f , I%-5.1f , "%(c6bm,g6bm,i6bm)

    cardpr=cardpr+' obE5, '
    for k in kk:
        c6em=float(ctpr6em[k])
        g6em=float(gtpr6em[k])
        i6em=float(itpr6em[k])
        cardpr=cardpr+"C%-5.1f , G%-5.1f , I%-5.1f , "%(c6em,g6em,i6em)
    
    cardpr=cardpr+' E5pr, '
    for k in kk:
        e6em=float(eprm[k])
        r6em=float(eprmc[k])
        cardpr=cardpr+"%5.1f , %5.0f , "%(e6em,r6em)
    
    fcard=card1+cardpr
    
    if(verb): print fcard
    return(fcard)

def getTCCode4Vmax(vmax):
        
    tctype='DB'
    if(vmax >= 25 and vmax <= 34): tctype='TD'
    if(vmax >= 35 and vmax <= 63): tctype='TS'
    if(vmax >= 64 and vmax <= 129): tctype='TY'
    if(vmax >= 130): tctype='STY'
    if(vmax <= 20): tctype='NT'
    return(tctype)

def getVmax4TCCode4(tctype):
        
    vmax=-99
    if(tctype == 'DB' or tctype == 'NT'): vmax=20
    elif(tctype == 'TD'): vmax=25
    elif(tctype == 'TS'): vmax=50
    elif(tctype == 'TY' or tctype == 'HU'): vmax=75
    elif(tctype == 'STY'): vmax=130
    return(vmax)

def parseDssTrk(dtg,dds,useVmax4TcCode=1,verb=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    osname='               , '
    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
 
    oroci='   '
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='    '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)

    ovmax='NaN'
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
 
    opmin='    '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34 != None and r34 != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34='     ,     ,     ,     ,'
        or34m='    , '
    
    got50=0
    if(r50 != None and r50 != undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50='     ,     ,     ,     ,'
        or50m='     , '
        if(got34):
            or50m='    , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth='%s'%(depth)
        
    otdo='NaN'
    
    # -- use TC wind for code
    #
    itccode=tccode
    rcTcCode=IsTc(itccode)
    if(useVmax4TcCode and vmax != 'NaN' and rcTcCode == 0):
        tccode=getTCCode4Vmax(vmax)
        #print 'ttttt-----',itccode,vmax,tccode,rcTcCode
            
    if(ovmax == 'NaN' and rcTcCode >= 1):
        vmax=getVmax4TCCode4(tccode)
        ovmax="%3.0f"%(vmax)
        print 'NNN---AAA---NNN vmax: ',tccode,ovmax,'pmin: ',opmin
        
        
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    odtgstm="%s , %s , %s , "%(dtg,stmid,osname)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf='NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,otdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)
    return(ocard)
    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
    elif(Is9X(stmid)):
        stype='9X'
        stm9xid=stmid
        sname=ss[2]
        if(find(sname,'NON')):
            stm1id='XXX.%s'%(ss[1])
        else:
            stm1id="%s.%s"%(ss[-1],ss[1])
        
    return(stype,stm1id,sname,stm9xid)         
    
# -- bug in parseDssTrk -- handle here since we can't redo making NNW-sum.txt
#
def parseDssTrkMD3(dtg,dds,stm1id,stm9xid,basin,rcsum=None,sname=None,verb=0,warn=0):
    
    def getr34(r34):
        or34='   '
        if(r34 != undef):
            or34="%3.0f"%(r34)
        return(or34)
            
    def getr50(r50):
        or50='   '
        if(r50 != undef):
            or50="%3.0f"%(r50)
        return(or50)
            
    #alf=b1id=depth=dir=dirtype=ndtgs=ntrk=ostmid=pmin=poci=posttype=r34=r34m=r50=r50m=rlat\
    #    =rlon=rmax=roci=sname=spd=stmid=tccode=tdo=trkdir=trkspd=undef=vmax=wncode=None
    
    tctype='Nan'
    stmDev='Nan'
    if(rcsum != None):
        tctype=rcsum[0]
        stmDev=rcsum[1]
        
    alf=dds.alf          #0.0
    b1id=dds.b1id        #W
    depth=dds.depth      #M
    dir=dds.dir          #275.449145529
    dirtype=dds.dirtype  #B
    ndtgs=dds.ndtgs      #40
    ntrk=dds.ntrk        #19
    ostm2id=dds.ostm2id  #wp30.2019
    pmin=dds.pmin        #984
    poci=dds.poci        #1009
    posttype=dds.postype #B
    r34=dds.r34          #[90, 45, 50, 80]
    r34m=dds.r34m        #66.25
    r50=dds.r50          #[40, 15, 15, 35]
    r50m=dds.r50m        #26.25
    rlat=dds.rlat        #10.8
    rlon=dds.rlon        #127.7
    rmax=dds.rmax        #15
    roci=dds.roci        #165
    # -- not here...sname=dds.sname      #PHANFONE
    spd=dds.spd          #15.7957548819
    stmid=dds.stmid      #30W.2019
    tccode=dds.tccode    #TY
    tdo=dds.tdo          #AMN
    trkdir=dds.trkdir    #275.449145529
    trkspd=dds.trkspd    #15.7957548819
    undef=dds.undef      #-999
    vmax=dds.vmax        #75
    wncode=dds.wncode    #WN

    if(sname != None and sname != undef):
        osname="%-15s"%(sname)
    else:
        osname="%-15s"%('NaN')
 
    oroci='NaN'
    if(roci != None and roci != undef and roci != 0):
        oroci="%3.0f"%(roci)
        
    opoci='NaN '
    if(poci != None and poci != undef and poci != 0):
        opoci="%4.0f"%(poci)
        
    ovmax='NaN '
    if(vmax != None and vmax != undef):
        ovmax="%3.0f"%(vmax)
        
    opmin='NaN '   
    if(pmin != None and pmin != undef):
        opmin="%4.0f"%(pmin)

    
    got34=0
    if(r34m != None and r34m != undef):
        got34=1
        or34ne=getr34(r34[0])
        or34se=getr34(r34[1])
        or34sw=getr34(r34[2])
        or34nw=getr34(r34[3])
        or34=' %s , %s , %s , %s , '%(or34ne,or34se,or34sw,or34nw)
        or34m='    , '
        if(r34m != None and r34m != undef):
            or34m="%3.0f , "%(r34m)
    else:
        or34=' NaN , NaN , NaN , NaN ,'
        or34m='NaN , '
    
    got50=0
    if(r50m != None and r50m!= undef):
        got50=1
        or50ne=getr50(r50[0])
        or50se=getr50(r50[1])
        or50sw=getr50(r50[2])
        or50nw=getr50(r50[3])
        or50=' %s , %s , %s , %s , '%(or50ne,or50se,or50sw,or50nw)
        or50m='    , '
        if(r50m != None and r50m != undef):
            or50m="%3.0f , "%(r50m)
    else:
        or50=' NaN , NaN , NaN , NaN ,'
        or50m=' NaN , '
        if(got34):
            or50m='NaN , '

    ormax='NaN'
    if(rmax != None and rmax != undef and rmax != 0):
        ormax="%3.0f"%(rmax)
        
    odepth='NaN'
    if(depth != None and depth != undef and depth != ''):
        odepth=' %s '%(depth)
        
        
    # -- replace md2 stmid with stmid from DIRECTORY
    # -- stm1id is set to NN or 9X
    #
    ostmid=stmid.lower()
    if(stmDev == 'DEV' and Is9X(ostmid)): 
        ostmid=stm1id.lower()
    elif(stmDev == 'NONdev' and Is9X(ostmid)): 
        ostmid=stm9xid.lower()
    elif(stmDev == 'NN' and Is9X(ostmid)): 
        ostmid=stmid.lower()
    elif(IsNNWarn(ostmid)): 
        #print 'ooooo---------',stmDev,ostmid
        ostmid=stm1id.lower()

    odtgstm="%s , %s , %s , %s , %s ,"%(dtg,ostmid,osname,tctype,stmDev)
    omotion="%3.0f , %2.0f , "%(dir,spd)
    otrkmotion="%3.0f , %2.0f , "%(trkdir,trkspd)
    oposition="%5.1f , %5.1f , "%(rlat,rlon)
    ointensity="%s , %s ,"%(ovmax,opmin)
    ocodes="%s , %s , %s , %s , "%(tccode,wncode,dirtype,posttype)
    orocipoci="%s , %s , "%(oroci,opoci)

        
    if(alf == 0.0 or alf == undef):
        oalf=' NaN'
    else:
        oalf="%4.2f"%(alf)
        
    # -- 20230125 -- bug in odepth -- has extra ','  adds extra column
    #
    tdo=tdo.strip()
    if(tdo == '---' or tdo == ''): tdo='NaN'
    omisc="%s , %s , %s , %s "%(oalf,odepth,ormax,tdo)    
    
    if(verb):
        print 'dtg        : ',odtgstm
        print 'position   : ',oposition
        print 'intensity  : ',ointensity
        print 'motion:    : ',omotion,'type: ',dirtype
        print 'trkmotion  : ',otrkmotion
        print 'tc|wncodes : ',ocodes
        print 'roci/poci  : ',orocipoci
        print 'r34        : ',or34m,or34
        print 'r50        : ',or50m,or50
        print 'misc       : ',omisc
    
    opart1="%s %s %s"%(odtgstm,oposition,ointensity)
    opart2="%s %s"%(omotion,otrkmotion)
    opart3="%s %s %s %s"%(or34m,or34,or50m,or50)
    if(got50): ocodes="%s"%(ocodes)
    else:      ocodes=" %s"%(ocodes)
    opart4="%s %s %s"%(ocodes,orocipoci,omisc)
    ocard="%s %s %s %s"%(opart1,opart2,opart3,opart4)                                                        
    return(ocard)

    
def getStmids4SumPath(sumPath):
    (sdir,sfile)=os.path.split(sumPath)
    ss=sdir.split("/")
    storm=ss[-1]
    basin=ss[-2]
    ss=storm.split('-')
    stmid="%s.%s"%(ss[0],ss[1])
    if(IsNN(stmid)):
        stype='NN'
        stm1id=stmid
        if(len(ss) == 5):
            sname="%s-%s"%(ss[2],ss[3])
        else:
            sname=ss[2]
        stm9xid="%s.%s"%(ss[-1],ss[1])
        stm9xid=stm9xid.lower()
    elif(Is9X(stmid)):
        sname='9X-%s'%(ss[0])
        stm9xid=stmid
        stype=ss[2]
        if(stype == 'NONdev'):
            stm1id=stmid
        elif(stype == 'DEV'):
            stm1id="%s.%s"%(ss[-1],ss[1])
        else:
            stm1id='XXX.%s'%(ss[1])
            stm1id=stm1id
            
        stm1id=stm1id.lower()
        
    return(stype,stm1id,sname,stm9xid,basin,sdir)         
    
def getW2fldsRtfimCtlpath(model,dtg,maxtau=None,dtau=6,details=1,override=0,verb=0,doSfc=0):

    from M2 import setModel2

    def getNfields(wgribs,verb=1):

        nfields={}

        for wgrib in wgribs:
            (dir,file)=os.path.split(wgrib)
            tt=file.split('.')
            tau=tt[len(tt)-3][1:]
            nf=len(open(wgrib).readlines())
            nfields[int(tau)]=nf

        return(nfields)


    def gettaus(gribs,verb=0):

        datpaths={}
        taus=[]
        gribver=None
        gribtype=None

        for grib in gribs:
            (dir,file)=os.path.split(grib)
            tt=file.split('.')
            tau=tt[len(tt)-2][1:]
            gribtype=tt[len(tt)-1]
            gribver=gribtype[-1:]
            siz=MF.GetPathSiz(grib)

            if(siz > 0):
                tau=int(tau)
                taus.append(tau)
                datpaths[tau]=grib
                if(verb): print file,tau,gribtype,gribver

        taus=MF.uniq(taus)

        return(taus,gribtype,gribver,datpaths)


    # -- default is to get 'all' taus, called only if maxtau is set...in
    #    getCtlpathTaus(self,model,dtg,maxtau=168)
    #
    def reducetaus(taus,maxtau='all',dtau=6):

        taus.sort()
        ftaus=[]
        if(maxtau == 'all'): maxtau=taus[-1]
        rtaus=range(0,maxtau+1,dtau)
        for tau in taus:
            if(not(tau in rtaus)): continue
            ftaus.append(tau)

        ftaus=MF.uniq(ftaus)

        return(ftaus)

    def dofail(details):
        if(not(details)):
            return(0,None,None)
        else:
            return(0,None,None,None,None,None,None,None)


    dtype='w2flds'
    imodel=model

    m2=setModel2(imodel)  
    m2.setDbase(dtg)

    dataDtg=dtg
    tauOffset=0
    
    if(is0618Z(dtg) and m2.modelDdtg == 12):
        tauOffset=6
        dataDtg=mf.dtginc(dtg, -6)

    nfields={}

    # -- check m2 for use obj bddir
    #
    useBddir=0
    if(hasattr(m2,'useBddir')): useBddir=m2.useBddir
    if(useBddir):
        bdirs=[m2.bddir]
        
        
    for bdir in bdirs:
        
        if(bdir == '/Volumes' and dtype == 'w2flds'):
            rootdir="%s/%s/%s"%(bdir,dtype,imodel)
        elif(useBddir):
            rootdir=bdir
        else:
            rootdir="%s/%s/dat/%s"%(bdir,dtype,imodel)
            
        maskdir="%s/%s"%(rootdir,dataDtg)

        mask="%s/*%s*.ctl"%(maskdir,imodel)

        if(verb): print "getW2fldsRtfimCtlpath: ",mask
        ctlpaths=glob.glob(mask)
        
        # -- special case for era5 where we have ua and sfc .ctl
        #
        if(len(ctlpaths) == 2 and (imodel == 'era5' or imodel == 'ecm5') ):
            for ctl in ctlpaths:
                if(doSfc and mf.find(ctl,'sfc')): 
                    ctlpaths=[ctl]
                    
                elif(not(doSfc) and mf.find(ctl,'ua')): 
                    ctlpaths=[ctl]
                
        if(len(ctlpaths) == 1):
            ctlpath=ctlpaths[0]
            
            # -- use M2 for w2flds -- cgd6 does not have a wgrib?.txt inventory...this makes it...
            #
            if(dtype == 'w2flds'):
                fm=m2.DataPath(dataDtg,dtype=dtype,dowgribinv=1,override=override,doDATage=1) 
                fd=fm.GetDataStatus(dataDtg)
                
            if(details):
                
                # -- handle situation where taus in w2flds != taus in nwp2 fields
                # -- tossed tau78 in ngp2
                #
                gmask="%s/*%s*.grb?"%(maskdir,imodel)
                if(dtype == 'w2flds'): gmask="%s/*%s*%s*.grb?"%(maskdir,imodel,dtype)
                
                # -- use fd object first...
                #
                if(hasattr(fd,'statuss')):
                    
                    try:
                        fds=fd.statuss[dataDtg]
                    except:
                        dofail(details)
                    
                    taus=fds.keys()
                    datpaths=fd.datpaths
                    gribtype=fd.gribtype
                    gribver=fd.gribver
                    
                    # get nfields hash
                    #
                    nfields={}
                    for n in range(0,len(fds)):
                        ntau=taus[n]
                        nf=fds[ntau][-1]
                        nfields[ntau]=nf
                        
                    taus.sort()

                else:
                    gribs=glob.glob(gmask)
                    (taus,gribtype,gribver,datpaths)=gettaus(gribs)
                
                    wmask="%s/*%s*.f???.wgrib?.txt"%(maskdir,imodel)
                    wgribs=glob.glob(wmask)
                    nfields=getNfields(wgribs)
                
                # -- cull taus
                if(maxtau != None): taus=reducetaus(taus,maxtau,dtau)

            else:
                taus=gribtype=gribver=datpaths=None

            if(not(details)):
                return(1,rootdir,ctlpath)
            else:
                return(1,ctlpath,taus,gribtype,gribver,datpaths,nfields,tauOffset)


    if(len(ctlpaths) == 0 or len(ctlpaths) > 1):
        if(verb): print 'WWW ctlpaths: ',ctlpaths

    dofail(details)

    
def getCtlpathTaus(model,dtg,maxtau=168,verb=0,doSfc=0,doBail=1):
    
    taus=[]
    ctlpath=taus=nfields=tauOffset=sfcpath=None
    rc=getW2fldsRtfimCtlpath(model,dtg,maxtau=maxtau,verb=verb,doSfc=doSfc)
    if(rc == None):
        if(doBail):
            print 'EEEE---tcVM-getCtlpathTaus-w2base.getW2fldsRtfimCtlpath...sayounara...for model: ',model,' dtg: ',dtg
            sys.exit()
        else:
            return(ctlpath,taus,nfields,tauOffset,sfcpath)

    if(rc[0]):
        ctlpath=rc[1]
        taus=rc[2]
        nfields=rc[-2]
        tauOffset=rc[-1]
        sfcpath=ctlpath.replace('-ua.','-sfc.')
        

    return(ctlpath,taus,nfields,tauOffset,sfcpath)

def getInvPath4Dtgopt(dtgopt,invdir='./inv',getonly=0,override=0):

    invmask="%s/inv-sbt-track-v??-%s.txt"%(invdir,dtgopt)
    invs=glob.glob(invmask)
    
    nnver=0
    npver=0
    if(len(invs) > 0):
        previnv=invs[-1]
        tt=previnv.split('-')
        pver=tt[-2]
        npver=int(pver[-2:])
        nnver=npver+1
        
    if(getonly): nnver=npver
        
    if(override): nver='v00'
    else:         nver="v%02d"%(nnver)
    
    invpath="inv/inv-sbt-track-%s-%s.txt"%(nver,dtgopt)
    return(invpath)

def Rlatlon2Clatlon(rlat,rlon,dotens=1,dodec=0,dozero=0):

    hemns='X'
    hemew='X'
    ilat=999
    ilon=9999

    if(rlat > -90.0 and rlat < 88.0):

        if(dotens):
            ilat=nint(rlat*10)
        else:
            ilat=nint(rlat)

        hemns='N'
        if(ilat<0):
            ilat=abs(ilat)
            hemns='S'
            rlat=abs(rlat)

        if(rlon > 180.0):
            rlon=360.0-rlon
            hemew='W'
        else:
            hemew='E'

        if(rlon < 0.0):
            rlon=abs(rlon)
            hemew='W'

        if(dotens):
            ilon=nint(rlon*10)
        else:
            ilon=nint(rlon)

    if(dotens):
        clat="%3d%s"%(ilat,hemns)
        clon="%4d%s"%(ilon,hemew)
        if(dozero):
            clat="%03d%s"%(ilat,hemns)
            clon="%04d%s"%(ilon,hemew)
    else:
        if(dozero):
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)
        else:
            clat="%02d%s"%(ilat,hemns)
            clon="%03d%s"%(ilon,hemew)

    if(dodec):
        clat="%5.1f%s"%(rlat,hemns)
        clon="%5.1f%s"%(rlon,hemew)

    return(clat,clon)

def isIOBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'I' or ustmid == 'A' or ustmid == 'B'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'IO' or ustmid == 'BB' or ustmid == 'AA'):
            return(1)
        else:
            return(0)
def isShemBasinStm(stmid):

    tt=stmid.split('.')
    stmid=tt[0]

    if(len(stmid) > 4):
        return(-1)

    if(len(stmid) == 1):
        ustmid=stmid.upper()
    elif(len(stmid) == 2):
        ustmid=stmid.upper()
    elif(len(stmid) == 3):
        ustmid=stmid[2].upper()
    elif(len(stmid) == 4):
        ustmid=stmid[0:2].upper()

    if(len(ustmid) == 1):
        if(ustmid == 'S' or ustmid == 'P' or ustmid == 'Q' or ustmid == 'H'):
            return(1)
        else:
            return(0)
    elif(len(ustmid) == 2):
        if(ustmid == 'SH' or ustmid == 'SP' or ustmid == 'SI' or ustmid == 'SL'):
            return(1)
        else:
            return(0)


def appendDictList(kdict,key,value):
    
    try:
        kdict[key].append(value)
    except:
        kdict[key]=[]
        kdict[key].append(value)

def dtg2gtime(dtg):
    try:
        (y,m,d,h)=dtg2ymdh(dtg)
    except:
        return(none)
    mo=mname3[m]
    gtime="%sZ%s%s%s"%(h,d,mo,y)
    return(gtime)


def getSrcSumTxt(stmid,qc2paths=1,bd2Update=0,verb=0):

    (snum,b1id,year,b2id,stm2id,stm1id)=getStmParams(stmid)
    basin=sbtB1id2Basin[b1id]
    if(basin == 'cpac'): basin='epac'
    stmid3=stm1id.split('.')[0].upper()
        
    tdir="%s/%s/%s"%(sbtSrcDir,year,basin)
     
    
    # -- avoid looking for 9x in one basin that goes into another...
    #
    tdir="%s/%s/*"%(sbtSrcDir,year)
    mmask="%s/%s*/*-sum.txt"%(tdir,stmid3)
    mmaskM2B="%s/%s*/*-sum-M2B.txt"%(tdir,stmid3)
    mmaskBT="%s/%s*/*-sum-BT.txt"%(tdir,stmid3)
    if(bd2Update):
        mmaskBT="%s/%s*/*-sum-BT2.txt"%(tdir,stmid3)
    mmaskMBT="%s/%s*/*-sum-MBT.txt"%(tdir,stmid3)

    if(verb):
        print 'tdir:      ',tdir,basin
        print 'bd2Update: ',bd2Update
        print 'mmask:     ',mmask
        print 'mmaskBT:   ',mmaskBT
        print 'mmaskMBT:  ',mmaskMBT

    mpaths=glob.glob(mmask)
    mpathBTs=glob.glob(mmaskBT)
    mpathMBTs=glob.glob(mmaskMBT)
    
    if(len(mpaths) == 1): mpath=mpaths[0]
    
    elif(len(mpaths) == 2): 
        # -- cases where dev 9X in different basin
        #
        if(qc2paths):
            rc=raw_input("""2 mpaths for stmid: %s
0 %s
1 %s
which one do you want to use? 0 | 1?"""%(stmid,mpaths[0],mpaths[1]))
            if(rc == '0'):
                mpath=mpaths[0]
                print 'using: %s'%(mpaths[0])
            elif(rc == '1'):
                mpath=mpaths[1]
                print 'using: %s'%(mpaths[1])
            else:
                print 'invalid choice...'
                sys.exit()
        else:
            mpath=mpaths[0]
            
    else: mpath=None

    if(len(mpathMBTs) == 1): 
        mpathBT=mpathMBTs[0]
        print 'III -- using bd2 for mpathBT: ',mpathBT
    elif(len(mpathBTs) == 1): 
        mpathBT=mpathBTs[0]
    else: 
        mpathBT=None
        
    mpath9X=None
    stmid9X=None
    
    if(mpath != None):
        
        rc=getStmids4SumPath(mpath)
        (stmDev,stm1id,sname,stm9xid,basin,sdir)=rc
        
        # -- if NN look for 9X
        #
        if(stmDev == 'NN'):
            stmid3=stm9xid.upper()[0:3]
            mmask9X="%s/%s*/*-sum.txt"%(tdir,stmid3)
            mpaths9X=glob.glob(mmask9X)
            if(len(mpaths9X) == 1):
                mpath9X=mpaths9X[0]
                
        elif(stmDev == 'DEV'):
            stmid3=stm1id.upper()[0:3]
            mmaskBT="%s/%s*/*-sum.txt"%(tdir,stmid3)
            mpathsBT=glob.glob(mmaskBT)
            if(len(mpathsBT) == 1):
                mpathBT=mpathsBT[0]
            rc=getStmids4SumPath(mpath)
            stmid9X=rc[3]
            mpath9X=mpath
        
        elif(stmDev == 'NONdev'):
            mpathBT=None
        else:
            print 'EEE invalid stmDev: ',stmDev,'for stmid: ',stmid
            sys.exit()
        
    else:
        print 'EEE no sum.txt for stmid: ',stmid,'sayounara'
        sys.exit()
    
    
    if(verb):
        print 'mpath:   ',mpath
        print 'mpathBT: ',mpathBT
        if(mpath9X != None): 
            print 'mpath9X: ',mpath9X
            print 'stmid9X: ',stmid9X
    
    # -- don't handle NN & 9X together
    #
    return(mpath,mpathBT)
    
def addQCspd2sum(sumPath,spdCards,verb=0):

    qcSpd={}
    for card in spdCards:
        ndtg=6
        if(find(card,'NONdev')): ndtg=5
        tt=card.split()
        spd=tt[1].strip()
        dtg=tt[ndtg].strip()
        if(verb): print 'qcSpd ',dtg,spd
        qcSpd[dtg]=int(spd)
    # -- read the cards
    #
    icards=open(sumPath).readlines()
    
    # -- convert to hash
    #
    iDict=cards2dict(icards)
    
    # -- add qc speed
    #
    qcards=[]
    
    dtgs=iDict.keys()
    dtgs.sort()
    
    for dtg in dtgs:
        try:
            qs=qcSpd[dtg]
        except:
            qs=-999

        qcard="%4i %s"%(qs,iDict[dtg])
        qcard=qcard[0:-10]
        qcards.append(qcard)
        
    return(icards,qcards)

def cards2dict(icards):
    
    oDict={}
    for icard in icards:
        tt=icard.split(',')
        dtg=tt[0].strip()
        oDict[dtg]=icard
        
    return(oDict)

def qcSpd(ocdev,lcdev,bspdmax,doMeld=0,doX=0,override=0,verb=0):    

    from sBTcl import MD3trk
    
    xgrads='grads'
    xgrads=setXgrads(useX11=0,useStandard=0)
    zoomfact=None
    background='black'
    dtgopt=None
    ddtg=6
    dtg0012=0

    ocardsDev=ocdev.values()
    ocardsDev.sort()

    for ocard in ocardsDev:
        if(verb): print
        print ocard
        tt=ocard.split()
        stmid=tt[0]
        stmspd=tt[1]
        stmspd=float(stmspd)
        stmidNN=tt[4]

        (sumPath,mpathBT,mpath9X,stmid9X)=getSrcSumTxt(stmid,verb=verb)

        if(sumPath != None):
            
            qcSumPath=sumPath.replace('.txt','.txt-QC%i'%(int(bspdmax)))
            savSumPath=sumPath.replace('.txt','.txt-SAV')
            rc=getStmids4SumPath(sumPath)
            (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
            stm1id=ostm1id.lower()
            stm9xid=ostm9xid.lower()
            if(stmDev == 'nonDev'): 
                stm1id=ostm9xid.lower()
                stm9xid=ostm9xid.lower()
            elif(stmDev == 'DEV'):
                stm1id=ostm9xid.lower()
                stm9xid=ostm1id.lower()

            spdCards=lcdev[stmid]
            (icards,qcards)=addQCspd2sum(sumPath,spdCards,verb=verb)
            
            rc=WriteList(qcards,qcSumPath,verb=verb)
            if(verb):
                print 'long ls for: ',stmid
                for card in lcdev[stmid]:
                    print card
                
            dom3=0
            md3=MD3trk(icards,stm1id,stm9xid,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
            dtgs=md3.dtgs
            btrk=md3.trk
            basin=md3.basin
            
            # -- make the plot
            MF.sTimer('trkplot')
            tP=TcBtTrkPlot(stm1id,btrk,dobt=0,
                           Window=0,Bin=xgrads,
                           zoomfact=zoomfact,override=override,
                           background=background,dopbasin=0,
                           dtgopt=dtgopt,pltdir=sdir)
        
            tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg)
            MF.dTimer('trkplot')
            if(doX): tP.xvPlot(zfact=0.75)
            
            if(doMeld):
                cmd="meld %s %s"%(sumPath,qcSumPath)
                runcmd(cmd)
                
            
        else:
            print 'EEEEE---whoa---no -SUM.txt for stmid: ',stmid,'WTF?'
            (sumPath,mpathBT,mpath9X,stmid9X)=getSrcSumTxt(stmid,verb=1)
            
            sys.exit()
            
         
        if(verb):
            print 'long ls for: ',stmid
            for card in lcdev[stmid]:
                print card
                
    return
        
def mergeMd3CvsBT(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0]
        stmid=tt[1]
        mcardsbt[dtg]=btcard
        
    dtgs=mcards.keys()
    dtgs.sort()

    for dtg in dtgs:
        mcard=mcards[dtg]

        try:
            mcardb=mcardsbt[dtg]
        except:
            mcardb=None
            
        if(mcardb != None):
            omcard=mcardb
            #omcard=mergePosit(mcard, mcardb)
        else:
            omcard=mcards[dtg]

        ocards.append(omcard)
            
        if(verb):
            
            if(mcardb == None): ocardb='None'
            else:               omcardb=mcardb
            print 'dtg: ',dtg,'  M:',omcard[0:50],'  B:',omcardb[0:50]
        
    return(ocards)

def mergeMdCvsBT(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0].strip()
        stmid=tt[1].strip()
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0].strip()
        stmid=tt[1].strip()
        mcardsbt[dtg]=btcard
        
    dtgs=mcards.keys()
    btdtgs=mcardsbt.keys()
    alldtgs=dtgs+btdtgs
    alldtgs=mf.uniq(alldtgs)

    for dtg in alldtgs:
        
        try:
            mcard=mcards[dtg]
        except:
            mcard=None

        try:
            mcardb=mcardsbt[dtg]
        except:
            mcardb=None
            
        if(mcard == None and mcardb == None):
            print 'EEEEEEEEEEEEEEEEEE problem with mcards for dtg: ',dtg,' mpath: ',mpath
            sys.exit()
            
        if(mcardb != None):
            omcard=mcardb
        else:
            omcard=mcard

        ocards.append(omcard)
            
        if(verb):
            
            if(mcardb == None): ocardb='None'
            else:               omcardb=mcardb
            print 'dtg: ',dtg,'  M:',omcard[0:50],'  B:',omcardb[0:50]
        
    return(ocards)


def mergePosit(mcard,mcardb,verb=0):
    
    mcard=mcard.replace('\n','')
    mcardb=mcard.replace('\n','')
    
    m=mcard.split(',')
    mo=mcard.split(',')
    
    mb=mcardb.split(',')
    
    nm=len(m)
    nmb=len(mb)

    if(nm != nmb):
        print 'problem with mcard,mcardb'
        print 'mcard  :',nm,mcard
        print 'mcardb :',nmb,mcardb
        sys.exit()
        
    mocard=''
    for n in range(0,nm-1):
        #print 'n',n,mo[n],mb[n]
        posit=(n >= 5 and n <= 12)
        td=(n >= 23 and n <= 32)
        if(posit or td):
            mo[n]=mb[n]
            
        if(n == 5 and verb):
            print 'nn',n,m[n],mo[n],mb[n]

        mocard="%s%s,"%(mocard,mo[n])
            
    mocard=mocard
    if(verb):
        print ' mcard: ',mcard
        print 'mocard: ',mocard
        print 'mcardb: ',mcardb

    return(mocard)
    

def mergeMd3Cvs9X(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}
    btcards=[]

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0]
        stmid=tt[1]
        mcardsbt[dtg]=btcard
        
        
    dtgs=mcards.keys()
    dtgs.sort()

    for dtg in dtgs:
        mcard=mcards[dtg]
        try:
            mcardb=mcardsbt[dtg]
        except:
            mcardb=None
        
        if(mcardb != None):
            mcard=mergePosit(mcard,mcardb)
            
        ocards.append(mcard)
        
        if(verb):
            print 'dtg: ',dtg,'  M:',mcard[0:50],'  B:',mcardsbt[dtg][0:50]
        
    return(ocards)
        
def mergeMdCvs9X(mpath,mpathBT,opath,verb=0):

    mcards={}
    mcardsbt={}
    btcards=[]

    ocards=[]
    
    cards=open(mpath).readlines()
    if(mpathBT != None):
        btcards=open(mpathBT).readlines()
        
    for card in cards:
        tt=card.split(",")
        dtg=tt[0]
        stmid=tt[1]
        mcards[dtg]=card
        
    for btcard in btcards:
        tt=btcard.split(',')
        dtg=tt[0]
        stmid=tt[1]
        mcardsbt[dtg]=btcard
        
        
    dtgs=mcards.keys()
    dtgs.sort()

    for dtg in dtgs:
        mcard=mcards[dtg]
        try:
            mcardb=mcardsbt[dtg]
        except:
            mcardb=None
        
        if(mcardb != None):
            mcard=mergePosit(mcard,mcardb)
            
        ocards.append(mcard)
        
        if(verb):
            print 'dtg: ',dtg,'  M:',mcard[0:50],'  B:',mcardsbt[dtg][0:50]
        
    return(ocards)



def lsSbtVars(verb=0):

    # -- meta
    #
    smcards=open('%s/%s'%(sbtVerDirDat,sbtMeta)).readlines()
    sMdesc={}
    sMkeys=[]

    for n in range(0,len(smcards)):
        tt=smcards[n].split(',')
        tt0=tt[0].replace("\n",'')
        tt1=tt[1].replace("\n",'')
        tt0=tt0.replace("""'""",'')
        tt1=tt1.replace("""'""",'')
        if(not(find(tt1,'title'))):
            sMdesc[tt0]=tt1
            sMkeys.append(tt0)
        
    if(verb):
        print 'superBT-%s listing'%(versionBT)
        print '         var : description'
        print '--------------------------'
        kk=sMkeys
        for k in kk:
            key="""'%s'"""%(k)
            print "%12s : %s"%(key,sMdesc[k])
    print
            
    return(sMdesc)
 
# -- md3

def lsMd3Vars(verb=0):

    # -- meta
    #
    smcards=open('%s/%s'%(sbtVerDirDat,md3VarsMeta)).readlines()
    mD3desc={}
    mD3keys=[]
    for n in range(0,len(smcards)):
        tt=smcards[n].split(',')
        tt0=tt[0].replace("\n",'')
        tt1=tt[1].replace("\n",'')
        tt0=tt0.replace("""'""",'')
        tt1=tt1.replace("""'""",'')
        if(not(find(tt1,'title'))):
            mD3keys.append(tt0)
            mD3desc[tt0]=tt1
        
    if(verb):
        kk=mD3keys
        print 'mD3-%s  variable listing'%(versionBT)
        print '         var : description'
        print '--------------------------'
        for k in kk:
            key="""'%s'"""%(k)
            print """%12s : %s"""%(key,mD3desc[k])
        print
            
    return(mD3desc)

def lsMd3SumVars(verb=0):

    # -- meta
    #
    smcards=open('%s/%s'%(sbtVerDirDat,md3SumMeta)).readlines()
    mD3desc={}
    mD3keys=[]
    for n in range(0,len(smcards)):
        tt=smcards[n].split(',')
        tt0=tt[0].replace("\n",'')
        tt1=tt[1].replace("\n",'')
        tt0=tt0.replace("""'""",'')
        tt1=tt1.replace("""'""",'')
        if(not(find(tt1,'title'))):
            mD3keys.append(tt0)
            mD3desc[tt0]=tt1
        
    if(verb):
        kk=mD3keys
        print 'mD3-%s summary variable listing'%(versionBT)
        print '         var : description'
        print '--------------------------'
        for k in kk:
            key="""'%s'"""%(k)
            print """%12s : %s"""%(key,mD3desc[k])
            
        print
            
    return(mD3desc)



def cleanMD3Opaths(sdir,ostm1id,verb=0):
    
    omask="%s/%s-*txt"%(sdir,ostm1id.upper())
    opaths=glob.glob(omask)
    if(verb): 
        print 'oooooo',omask
        for opath in opaths:
            print opath
            
    cmd="rm %s"%(omask)
    mf.runcmd(cmd)
            
def getMd2Years(stmopt=None,dtgopt=None,lastyear=None):

    from tcbase import TcData
    
    curdtg=mf.dtg()
    
    years=[int(curdtg[0:4])]
    
    if(dtgopt != None):
        
        dtgs=mf.dtg_dtgopt_prc(dtgopt,ddtg=6)

        years=[]
        for dtg in dtgs:
            (rc,nhemyears)=getNhemYearsInt(dtg)
            years=years+nhemyears

            curyear=int(dtg[0:4])
            shemyear=int(getShemYear(dtg))

            # -- 20250311 -- new logic for making sure we don't go past the 
            #    md3 last year (lastyear,em3yearq)
            #
            lasttest=(lastyear != None and int(shemyear) <= int(lastyear))
            curtest=(curyear != shemyear )

            if(curtest and lasttest):
                years.append(shemyear)
                
        years=mf.uniq(years)

    if(stmopt != None):

        if(type(stmopt) is ListType):
            stmids=stmopt
        else:
            # -- use this one because makeStmListMdeck is a method on TcData() -- this is stand-alone
            stmids=MakeStmList(stmopt)

        # -- use TcData if no ids...
        #
        if(len(stmids) == 0):
            
            stmopts=getStmopts(stmopt)
            if(len(stmopts) == 1):
                stmopt=stmopts[0]
                year=stmopt.split('.')[-1]
                year=int(year)
            
            tcD=TcData(years=[year])
            stmids=tcD.makeStmListMdeck(stmopt)
            

        if(len(stmids) > 0):
            years=[]
            for stmid in stmids:
                year=int(stmid.split('.')[1])
                if(year <= em3year):
                    years.append(year)
            years=mf.uniq(years)
        
    return(years)


def getShemYear(dtg):
    """
     convert year in stm dtg to basinyear
    """

    yyyy=int(dtg[0:4])
    mm=int(dtg[4:6])

    if(mm >= 7): yyyy=yyyy+1
    cyyyy=str(yyyy)
    return(cyyyy)

def getNhemYears(dtg):
    """
     get nhem years for case of storm crossing new year
    """

    year1=dtg[0:4]
    dtgnhemMax=year1+'011500'
    dtnhem=mf.dtgdiff(dtg,dtgnhemMax)
    year2=year1
    if(dtnhem >= 0.0): year2=str(int(year1)-1)
    years=[year2,year1]
    return(years)

def getNhemYearsInt(dtg,mmddhh='011500'):
    """
     get nhem years for case of storm crossing new year as Int
    """

    year1=dtg[0:4]
    dtgnhemMax=year1+mmddhh
    dtnhem=mf.dtgdiff(dtg,dtgnhemMax)
    year1=int(year1)
    year2=year1
    if(dtnhem >= 0.0): year2=year2-1
    rc=0
    if(year2 != year1):rc=1
    years=[year2,year1]
    return(rc,years)

def getNhemShemYearsFromDtg(dtg):
    """
get years for a dtg to handle two situations nhem storms crossing new year
shem storms 070100-123118
"""
    (rcnhem,nhemyears)=getNhemYearsInt(dtg)
    shemyear=int(getShemYear(dtg))
    
    if(rcnhem):
        rc=1
        year=nhemyears[0]
        shemyear=nhemyears[1]
    else:
        rc=2
        year=nhemyears[0]
        if(year == shemyear): rc=0
        
    return(rc,year,shemyear)

def add2000(y):
    if(len(y) == 1):
        yyyy=str(2000+int(y))
    elif(len(y) == 2):
        if(int(y) > 25):
            yyyy=str(1900+int(y))
        else:
            yyyy=str(2000+int(y))
    else:
        yyyy=y
    return(yyyy)


def getyears(yyy):

    if(yyy == 'cur'):
        curdtg=mf.dtg()
        yyy=curdtg[0:4]

    years=[]
    n1=0
    n2=0

    tt0=yyy.split('-')
    tt1=yyy.split(',')

    if(len(tt1) > 1):
        for tt in tt1:
            yyyy=add2000(tt)
            years.append(yyyy)
        return(years)

    if(len(tt0) > 1):
        y1=tt0[0]
        y2=tt0[1]
        yyyy1=add2000(y1)
        yyyy2=add2000(y2)

        if(len(yyyy1) != 4 or len(yyyy2) != 4):
            print 'EEEE getyears tt:',tt
            return(None)

        else:
            n1=int(yyyy1)
            n2=int(yyyy2)
            for n in range(n1,n2+1):
                years.append(str(n))

    else:
        if(len(yyy) <= 2): yyy=add2000(yyy)
        years=[yyy]

    return(years)


def MakeStmList(stmopt,yearopt=None,dofilt9x=0,verb=0):

    def getyears(yyy):

        if(yyy == 'cur'):
            curdtg=mf.dtg()
            yyy=curdtg[0:4]

        years=[]
        n1=0
        n2=0

        tt0=yyy.split('-')
        tt1=yyy.split(',')

        if(len(tt1) > 1):
            for tt in tt1:
                yyyy=add2000(tt)
                years.append(yyyy)
            return(years)

        if(len(tt0) > 1):
            y1=tt0[0]
            y2=tt0[1]
            yyyy1=add2000(y1)
            yyyy2=add2000(y2)

            if(len(yyyy1) != 4 or len(yyyy2) != 4):
                print 'EEEE getyears tt:',tt
                return(None)

            else:
                n1=int(yyyy1)
                n2=int(yyyy2)
                for n in range(n1,n2+1):
                    years.append(str(n))

        else:
            if(len(yyy) <= 2): yyy=add2000(yyy)
            years=[yyy]

        return(years)


    def getstmids(sss,year,dofilt9x=dofilt9x):

        sids=[]
        n1=0
        n2=0
        tt=sss.split('-')

        if(len(tt) > 1):
            if(len(tt[0]) != 2 or len(tt[1]) != 3):
                print 'EEEE getstmids tt:',tt
                return(None)

            else:
                n1=int(tt[0])
                n2=int(tt[1][0:2])
                bid=tt[1][2].upper()

                for n in range(n1,n2+1):
                    sid="%02d%1s.%s"%(n,bid,year)
                    sids.append(sid)

        elif(len(sss) == 1):

            tcnames=GetTCnamesHash(year)
            bchk=sss.upper()

            for tcname in tcnames:
                # -- improved subbasin checking...
                #
                tcsubbasin=tcname[1][2:3]
                chk1=(tcsubbasin == bchk)
                chk2=(isIOBasinStm(tcsubbasin) and isIOBasinStm(bchk))
                chk3=(isShemBasinStm(tcsubbasin) and isShemBasinStm(bchk))
                if(chk1 or chk2 or chk3):
                    sid="%s.%s"%(tcname[1],tcname[0])
                    sids.append(sid)
                else:
                    sid=None
                    
        elif(len(tt) == 1):

            if(len(sss) == 3):
                if(sss[0].upper() == 'M'):
                    nback=int(sss[1])
                    bchk=sss[2].upper()
                    tcnames=GetTCnamesHash(year)
                    for tcname in tcnames:
                        if(tcname[1][2:3] == bchk):
                            sid="%s.%s"%(tcname[1],tcname[0])
                            sids.append(sid)
                        else:
                            sid=None

                    sids.sort()
                    osids=[]

                    nsids=len(sids)
                    for n in range(nsids-nback,nsids):
                        osids.append(sids[n])

                    return(osids)

                elif(mf.find(sss[0:2].lower(),'9x')):

                    # -- turn off dofilt9x if here...
                    if(dofilt9x): print 'WWW(tcVM.MakeStmList) -- dofilt9x=1 but you want 9X stmids...set dofilt9x=0'
                    for n in range(90,100):
                        sid="%2d"%(n) + sss[2].upper() + '.'+year
                        sids.append(sid)
                    

                else:

                    sid="%s.%s"%(sss.upper(),year)
                    sids.append(sid)



        else:
            print 'EEEE getstmids sss:',sss
            return(None)


        sids.sort()
        return(sids)

    #
    # start.......................
    #

    curdtg=mf.dtg()
    curyear=curdtg[0:4]

    #
    # single storm
    #

    if(stmopt == None):

        sopt='w,e,c,l,i,a,b,p,s'
        if(yearopt == None):
            yopt='cur'
        else:
            yopt=yearopt
        years=getyears(yopt)

    elif(stmopt != None and stmopt != 'all'):

        ttt=stmopt.split('-')
        ttc=stmopt.split(',')
        tt=stmopt.split('.')
        
        if(len(tt) == 1 and len(ttt) == 1 and len(ttc) == 1):
            if(len(tt[0]) == 3):
                stmid=tt[0][2]
            elif(len(tt[0]) != 1):
                print 'tcVM.MakeStmList() EEEE bad stm3id: tt:',tt,'ttt: ',ttt,'ttc: ',ttc,'stmopt: ',stmopt
                sys.exit()
            else:
                stmid=tt[0]

            if(isShemBasinStm(stmid)):
                stmyear=getShemYear(curdtg)
            else:
                stmyear=curyear

            if(isIOBasinStm(stmid)):
                stmyear=curyear
                
            stmyear=add2000(stmyear)

            stmopt=stmopt+'.'+stmyear
            tt=stmopt.split('.')
            
        #
        # stm spanning using current year
        #

        elif(len(ttt) > 1 and len(ttc) == 1 and len(tt) == 1):

            stmids=getstmids(stmopt,curyear,dofilt9x)
            return(stmids)

        #
        # list of individual stmid (sss.y)
        #

        if(len(ttc) > 1):

            stmids=[]
            for stmopt in ttc:
                stmids=stmids+MakeStmList(stmopt,dofilt9x=dofilt9x,
                                          verb=verb)

            return(stmids)


        if(len(ttc) > 1 and len(tt) > 2):

            stmids=[]

            for stmid in ttc:
                ss1=stmid.split('.')
                if(len(ss1) != 2):
                    print 'EEE invalid individual stm: ',stmmid
                    sys.exit()

                sid=ss1[0]
                yid=ss1[1]
                if(len(yid) >= 1): yid=add2000(yid)
                rc=getstmids(sid,yid,dofilt9x)
                stmids=stmids+rc

            return(stmids)

        sopt=tt[0]
        yopt=tt[1]
        years=getyears(yopt)

    else:

        sopt='w,e,c,l,i,a,b,p,s'
        if(yearopt == None):
            yopt='cur'
        else:
            yopt=yearopt
        years=getyears(yopt)


    if(verb):
        print '(tcbase.makeStmList) sopt: ',sopt
        print '(tcbase.makeStmList) yopt: ',yopt,years


    stmids=[]

    for year in years:

        ss=sopt.split(',')
        if(len(ss) > 1):
            for sss in ss:
                rc=getstmids(sss,year,dofilt9x=dofilt9x)
                if(rc != None):
                    stmids=stmids+rc

        else:
            stmopt="%s.%s"%(sopt,year)
            rc=getstmids(sopt,year,dofilt9x=dofilt9x)
            if(rc != None):
                stmids=stmids+rc

    #
    # filter out 9X
    #
    if(dofilt9x):
        nstmids=[]
        for stmid in stmids:
            num=int(stmid[0:2])
            if(num < 80):
                nstmids.append(stmid)

        stmids=nstmids


    if(verb):
        for stmid in stmids:
            print '(tcbase.makeStmList) stmid: ',stmid

    # -- case 
    return(stmids)

def getYears4Opts(stmopt,dtgopt,yearOpt):
    
    oyearOpt=None
    doBdeck2=0
    
    if(yearOpt != None):
        
        if(mf.find(yearOpt,'-')):
            return(yearOpt,doBdeck2)
        
        tt=yearOpt.split('.')
        
        if(len(tt) == 2):
            byear=tt[0]
            eyear=tt[1]
            years=yyyyrange(byear, eyear)
            oyearOpt="%s-%s"%(byear,eyear)
        
        elif(len(tt) == 1):
        
            years=[yearOpt]
            oyearOpt=yearOpt
            
        for year in years:
            if(int(year) < 2007):
                doBdeck2=1
                
        return(oyearOpt,doBdeck2)
    
    else:
        
        syears=getMd2Years(stmopt,dtgopt,em3year)
        
        if(len(syears) == 0):
            print 'qqq--invalid stmopt,dtgopt',stmopt,dtgopt
            sys.exit()
            
        elif(len(syears) == 1):
            byear=syears[0]
            eyear=syears[0]

        elif(len(syears) > 1):
            byear=syears[0]
            eyear=syears[-1]
            
        if(byear == eyear):
            oyearOpt="%s"%(byear)
        else:
            oyearOpt="%s-%s"%(byear,eyear)
            oyearOpt="%s.%s"%(byear,eyear)
            
        if(byear < 2007 or eyear < 2007):
            doBdeck2=1
            doBT=1
        
    return(oyearOpt,doBdeck2)


     

def getMD3Opaths(mpath,doM2=1,verb=0):
    
    isBT=0
    if(mf.find(mpath, '-BT.txt') or mf.find(mpath, '-BT2.txt')):  isBT=1

    rc=getStmids4SumPath(mpath)
    (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()
        
    (sdir,sfile)=os.path.split(mpath)

    if(verb):
        print 'spath: ',mpath
    ostm1id=stm1id.replace('.','-')

    if(verb):
        print 'stm1id:  ',stm1id
        print 'stm9xid: ',stm9xid
        print 'sdir:    ',sdir
        print 'sfile:    ',sfile
        
    
    ofile="%s-md3.txt"%(ostm1id.upper())
    if(mf.find(sfile,'BT')):
        ofile="%s-md3-BT.txt"%(ostm1id.upper())
        

    if(doM2):
        ofile="%s-md3-MRG.txt"%(ostm1id.upper())
        if(mf.find(sfile,'BT')):
            ofile="%s-md3-BT.txt"%(ostm1id.upper())
        ofileS=ofile.replace('md3','sum-md3')
    else:
        ofile="%s-md3.txt"%(ostm1id.upper())
        if(mf.find(sfile,'BT')):
            ofile="%s-md3-BT.txt"%(ostm1id.upper())
        ofileS=ofile.replace('md3','sum-md3')

    opathS="%s/%s"%(sdir,ofileS)
    opath="%s/%s"%(sdir,ofile)

    opathSThere=(MF.getPathNlines(opathS) > 0)
    opathThere=(MF.getPathNlines(opath) > 0)
    
    rc=(opath,opathS,opathThere,opathSThere,ofile,ofileS,sdir,
        isBT,sfile,stmDev,ostm1id,sname,stm1id,stm9xid,basin)

    return(rc)


def makeMD3(mpath,rcM3,gendtg=None,doM2=1,verb=0):

    from sBTcl import MD3trk

    (opath,opathS,opathThere,opathSThere,ofile,ofileS,sdir,
     isBT,sfile,stmDev,ostm1id,sname,stm1id,stm9xid,basin)=rcM3
    
    try:
        icards=open(mpath).readlines()
    except:
        print """EEE can't read mpath: %s -- sayounara"""%(mpath)
        sys.exit()

    opathSTmp="/tmp/%s"%(ofileS)
    opathTmp="/tmp/%s"%(ofile)

    print
    print 'spath:  ',mpath
    print 'opath:  ',opath
    print 'opathS: ',opathS
    print 'gendtg: ',gendtg

    if(verb):
        print 'stm1id: ',stm1id	
        print 'sname:  ',sname
        print 'stmDev: ',stmDev
        print 'sdir:   ',sdir
        print 'sfile:  ',sfile
        print 'ofile:  ',ofile
        print 'ofileS: ',ofileS
        
        print 'opath:  ',opath
        print 'opathS: ',opathS

    if(verb):    
        for icard in icards:
            print 'iii',icard[0:-1]
        
    ocards=[]
    dom3=0
    md3=MD3trk(icards,stm1id,stm9xid,gendtg=gendtg,dom3=dom3,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    dtgs=md3.dtgs
    trk=md3.trk
    basin=md3.basin
    
    # -- analyze the stm to make summary card
    #
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=1,warn=1)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    if(isBT):
        print '222-BBB',rcsum,m3sum[0:-1]
    else:
        print '222-999',rcsum,m3sum[0:-1]

    # -- now do trk
    #

    ktrk=trk.keys()
    ktrk.sort()
    ocards=[]
    
    for kt in ktrk:
        ocard=parseDssTrkMD3(kt,trk[kt],stm1id,stm9xid,basin,rcsum=rcsum,sname=sname)
        ocard=ocard.replace(' ','')
        if(verb): print 'ooo---iii',ocard,len(ocard.split(','))
        ocards.append(ocard)

    rc=MF.WriteList2Path(ocards, opathTmp,verb=verb)
    (m3trk,m3info)=getMd3trackSpath(opathTmp,verb=verb)
    m3trki=setMd3track(m3trk,stm1id,verb=verb)
    dtgs=m3trki.keys()
    dtgs.sort()
    
    m3cards=[]
    for dtg in dtgs:
        try:
            m3i=m3info[dtg]
            m2trk=trk[dtg]
        except:
            None
        im3trk=m3trki[dtg]
        m3card=makeMd3Card(dtg,im3trk, m3i,m2trk,verb=verb)
        m3cards.append(m3card)

    rc=MF.WriteList2Path(m3cards, opath,verb=verb)

    md3=MD3trk(m3cards,stm1id,stm9xid,gendtg=gendtg,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opathS)
    if(isBT):
        print '333-NNN',rcsum,m3sum[0:-1]
    else:
        print '333-999',rcsum,m3sum[0:-1]
        
    return(opath,m3sum,rcsum)
    

def mergeMD3(mpath3,mpath3BT,doM2=0,verb=0):

    from sBTcl import MD3trk
    
    # -- write out mpath -> opath for 9X; mergeMd3Cvs handles no BT
    #
    rc=getStmids4SumPath(mpath3)
    (stmDev,stm1id,sname,stm9xid,basin,sdir)=rc
    
    isBT=0
    isDev=0
    isNon=0
    if(stmDev == 'NN'):  isBT=1
    if(stmDev == 'DEV'):  isDev=1
    
    if(doM2):
        # -- if do merge with md2 do merge here, just make the md3 and sum 
        #
        ocards=open(mpath3).readlines()
        opath3=mpath3
        opath3S=opath3.replace('md3','sum-md3')
        
    else:
        opath3=None
        (odir,ofile)=os.path.split(mpath3)
        (obase,oext)=os.path.splitext(ofile)
        opath3="%s/%s-MRG.txt"%(odir,obase)
        opath3S=opath3.replace('md3','sum-md3')
        # -- merge md3   
        #
        if(isBT):
            ocards=mergeMd3CvsBT(mpath3,mpath3BT,opath3,verb=verb)
        else:
            ocards=mergeMd3Cvs9X(mpath3,mpath3BT,opath3,verb=verb)

    MF.WriteList2Path(ocards, opath3,verb=verb)
    
    # -- switch names if 9X DEV
    #
    ostm1id=stm1id
    ostm9xid=stm9xid
    if(isDev):
        ostm1id=stm9xid
        ostm9xid=stm1id
        
    md3=MD3trk(ocards,ostm1id,ostm9xid,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    (m3sum,rcsum)=md3.lsDSsStmSummary(doprint=0)
    m3sum=m3sum.replace(' ','')
    m3sum=m3sum+',\n'
    rc=MF.WriteString2Path(m3sum, opath3S)
    if(isBT):
        print '333-NNN-MRG',rcsum,m3sum[0:-1]
    else:
        print '333-999-MRG',rcsum,m3sum[0:-1]
    
    return(opath3)
    
def mergeMD(mpath,mpathBT,verb=0):
    
    # -- write out mpath -> opath for 9X; mergeMd3Cvs handles no BT
    #
    rc=getStmids4SumPath(mpath)
    (stmDev,stm1id,sname,stm9xid,basin,sdir)=rc
    isBT=0
    if(stmDev == 'NN'):  isBT=1
    
    opath=None
    (odir,ofile)=os.path.split(mpath)
    (obase,oext)=os.path.splitext(ofile)
    opath="%s/%s-M2B.txt"%(odir,obase)

    if(isBT):
        ocards=mergeMdCvsBT(mpath,mpathBT,opath,verb=verb)
    else:
        ocards=mergeMdCvs9X(mpath,mpathBT,opath,verb=verb)

    MF.WriteList2Path(ocards, opath,verb=verb)

    return(opath)
    
    
def getStmidsDirs(years,basins,doQC=0,bspdmax=30):
    
    ostmids=[]
    osdirs={}
    for year in years:
        sbdir="%s/%s"%(sbtSrcDir,year)
        if(not(MF.ChkDir(sbdir))):
            print 'sbdir not there...'
            sys.exit()
        
        for basin in basins:
            bsdir="%s/%s"%(sbdir,basin)
            if(not(MF.ChkDir(bsdir))):
                print 'bsdir not there...'
                sys.exit()
            
            if(doQC):
                smask="%s/%s/*/*QC-%d"%(sbdir,basin,bspdmax)
            else:
                smask="%s/%s/*"%(sbdir,basin)
                
            sdirs=glob.glob(smask)
            sdirs.sort()
            for sdir in sdirs:
                if(doQC):
                    (qdir,qfile)=os.path.split(sdir)
                    ss=qdir.split('/')
                else:
                    ss=sdir.split('/')
                    
                stm=ss[-1]
                sss=stm.split('-')
                stmid="%s.%s"%(sss[0].lower(),sss[1])
                ostmids.append(stmid)
                osdirs[stmid]=sdir
                
    return(ostmids,osdirs)


def doTrkPlot(mpath,plttag=None,override=1,title2=None,doM3=0,doX=1,verb=0):

    from sBTcl import MD3trk,TcBtTrkPlot

    xgrads='grads'
    xgrads=setXgrads(useX11=0,useStandard=0)
    zoomfact=None
    background='black'
    dtgopt=None
    ddtg=6
    dtg0012=0
    
    rc=getStmids4SumPath(mpath)
    (stmDev,ostm1id,sname,ostm9xid,basin,sdir)=rc
    stm1id=ostm1id.lower()
    stm9xid=ostm9xid.lower()
    if(stmDev == 'nonDev'): 
        stm1id=ostm9xid.lower()
        stm9xid=ostm9xid.lower()
    elif(stmDev == 'DEV'):
        stm1id=ostm9xid.lower()
        stm9xid=ostm1id.lower()

    icards=open(mpath).readlines()

    if(doM3):
        md3=MD3trk(icards,stm1id,stm9xid,dom3=1,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
    else:
        md3=MD3trk(icards,stm1id,stm9xid,dom3=0,sname=sname,basin=basin,stmDev=stmDev,verb=verb)
        
    dtgs=md3.dtgs
    btrk=md3.trk
    basin=md3.basin
    
    # -- make the plot
    MF.sTimer('trkplot')
    tP=TcBtTrkPlot(stm1id,btrk,dobt=0,
                   Window=0,Bin=xgrads,
                   zoomfact=zoomfact,override=override,
                   background=background,dopbasin=0,
                   dtgopt=dtgopt,pltdir=sdir,
                   plttag=plttag)

    tP.PlotTrk(dtg0012=dtg0012,ddtg=ddtg,title2=title2)
    MF.dTimer('trkplot')
    if(doX): tP.xvPlot(zfact=0.75)
    

def setQcPassPath(rcc,qcpath,opath3,stmid,qcpass=0,bspdmax=30.0,
                  verb=0,override=0):
    
    
    (pqcdir,pqcfile)=os.path.split(opath3)
    pqclines=[]
    
    rccQC=0
    if(rcc == 1 and qcpath == None):
        print 'GGGoodQQCC - NNN qcpath for %s rcc: %d NNNNN qcpath'%(stmid,rcc)
        rccQC=1
    elif(rcc == 1 and qcpath != None):
        print 'GGGoodQQCC - YYY qcpath for %s rcc: %d YYYYY qcpath: %s'%(stmid,rcc,qcpath)
        rccQC=2
    elif(rcc == 0 and qcpath == None):
        print 'FFFailQQCC - NNN qcpath for %s rcc: %d NNNNN qcpath: %s'%(stmid,rcc,qcpath)
        rccQC=3
    elif(rcc == 0 and qcpath != None):
        print 'FFFailQQCC - YYY qcpath for %s rcc: %d YYYYY qcpath: %s'%(stmid,rcc,qcpath)
        rccQC=4
    else:
        print 'IIIvalid return code: ',rcc
    
    ibspdmax=int(bspdmax)
    pqcline="QC-P%02d-S%02d-RC-%02d-CurTime:%s"%(qcpass,ibspdmax,rccQC,mf.dtg('dtg.hms'))
    pqclines.append(pqcline)
    pqclineNotime="QC-P%02d-S%02d-RC-%02d"%(qcpass,ibspdmax,rccQC)
    pqcfile="%s-%s"%(pqclineNotime,pqcfile)
    pqcpath="%s/%s"%(pqcdir,pqcfile)
    nlQc=MF.getPathNlines(pqcpath)
    
    if(override):
        cmd="rm -i %s"%(pqcpath)
        mf.runcmd(cmd)
    
    if(verb):
        print 'pqcpath:      ',pqcpath
        print 'pqclines:     ',pqclines
        print 'pqcpath nlQc: ',nlQc
        
    if(nlQc > 0):
        rc=MF.WriteList2Path(pqclines,pqcpath,append=1,verb=0)
    else:
        rc=MF.WriteList2Path(pqclines,pqcpath,append=0,verb=0)
        
    return(rccQC)
    
    


def chkSpdDirMd3Mrg(mpath3,mpath,
                    mpathBT=None,
                    doRedo=0,
                    bspdmax=30.0,
                    bspdmaxNN=40.0,
                    latMaxNN=35.0,
                    verb=0,
                    killSngl=1,
                    override=0,
                    ):


    exDtgs=[]
    qcM3Cards={}

    qcpath="%s-QC-%02.0f"%(mpath,bspdmax)
    iqcpath=qcpath
    iqcThere=MF.getPathNlines(iqcpath)
    if(iqcThere < 0): iqcThere=0
    
    pp=mpath.split('/')
    ss=pp[-2][0:8].replace('-','.')
    stmid=ss.lower()
    
    posits={}
    spds={}
        
    m3cards=open(mpath3).readlines()
    mcards=open(mpath).readlines()
    if(mpathBT != None):
        mcardsBT=open(mpathBT).readlines()
    
    nm3=len(m3cards)
    nm=len(mcards)

    # -- change to warning vice kill...
    #
    if(nm == 1):
        (sdir,sfile)=os.path.split(mpath)
        #if(killSngl):
            #ropt=''
            #rc=raw_input("KILL-SSSIIInngggllleeetttooonnn? y|n  ")
            #if(rc.lower() == 'y'):
                #cmd="rm -r %s"%(sdir)
                #mf.runcmd(cmd,ropt)
        #else:
        print 'WWWWWWWWWWWWWWWWWW-SSSIIInngggllleeetttooonnn: ',mpath
        #return(2,None)
            
        
    if(nm3 != nm and verb):
        print 'EEE??? -- nm3 ',nm3,' != nm ',nm,' for m3: ',mpath3,' m: ',mpath
    
    for m3card in m3cards:

        mm=m3card.split(',')
        
        (dtg,rlat,rlon,vmax,pmin,
         tdir,tspd,r34m,r50m,tcstate,warn,
         roci,poci,alf,depth,eyedia,
         tdo,ostmid,ostmname,r34,r50)=parseMd3Card(mm)
        blat=rlat
        blon=rlon
        bvmax=vmax
        posits[dtg]=(blat,blon,bvmax)
        qcM3Cards[dtg]=m3card
        
    for mcard in mcards:
        mm=mcard.split(',')
        dtg=mm[0].strip()
        #qcM3Cards[dtg]=mcard

    dtgs=posits.keys()
    dtgs.sort()
    
    ndtgs=len(dtgs)
    
    for n in range(0,ndtgs):
        
        odtg=dtgs[n]
        if(ndtgs == 1):
            dtgm1=dtgs[0]
            dtg=dtgs[0]
        elif(n == 0 and ndtgs > 1):
            dtgm1=dtgs[0]
            dtg=dtgs[n+1]
        else:
            dtgm1=dtgs[n-1]
            dtg=dtgs[n]

        blat=posits[dtg][0]
        blatm1=posits[dtgm1][0]

        blon=posits[dtg][1]
        blonm1=posits[dtgm1][1]

        (bdir,bspd,bu,bv)=rumhdsp(blatm1,blonm1,blat,blon,6)

        obspd=bspd
        spds[odtg]=bspd

        stmidNN=stmid
        
            
        stest9X=(bspd > bspdmax)
        stestNN=(bspd > bspdmaxNN)
        ltest=(abs(blat) < latMaxNN)
        ntest=IsNN(stmid)
        
        dtest=(stest9X and not(ntest))
        btest=(stestNN and ltest and ntest)
        
        # -- ignore last three dtgs -- typically ET below latMaxNN
        #
        lastdtgtest=(n <= ndtgs-3)
        if((dtest or btest) and lastdtgtest):
            exDtgs.append(dtg)
            
    
    
    # -- if have a problem...
    #
    oqcpath=None
    if(len(exDtgs) > 0):
        oqccards=[]
        for dtg in dtgs:
            try:
                oqccard="%4.0f %s"%(spds[dtg],qcM3Cards[dtg])
            except:
                continue
            oqccards.append(oqccard)

        rc=MF.WriteList2Path(oqccards,qcpath,verb=0)
        oqcpath=qcpath
        
    if(oqcpath == None):
        if(iqcThere > 0):
            #print '<<<<< QC PPPAAASSSSSS for stmid: ',stmid,'BUT qcpath: ',iqcpath
            return(1,iqcpath)
        else:
            #print '<<<<<<<<<<<<<<<<<<<<<QC PPPAAASSSSSS for stmid: ',stmid,' return qcpath=None'
            return(1,None)
        
    else:
        print '>>>>>>>>>>>>>>>>>>>>>QC FFAAIILL for stmid: ',stmid
        return(0,oqcpath)
    

def doQCTrk(mpath3,mpath,mpathBT,qcpath,savPath,plttag=None,title2=None,ropt=''):
    
    rc=doTrkPlot(mpath3,doM3=1,plttag=plttag,title2=title2)
    
    print 'doing edit of mpath: ',mpath
    if(mpathBT != None):
        cmd='meld %s %s %s'%(qcpath,mpath,mpathBT)
    else:
        cmd='meld %s %s'%(qcpath,mpath)
    mf.runcmd(cmd,ropt)
    
    cmd='diff %s %s'%(savPath,mpath)
    rc=MF.runcmdLog(cmd)
    lrc=len(rc)
    
    if(lrc == 1):
        rcQC=1
        print 'NNNNN No changes made...'
        
        #rc=raw_input("NNNNN No change made and still okay? ")
        #if(rc.lower() == 'y'):
            #mf.runcmd("rm -i %s"%(qcpath),ropt)
    else:
        rcQC=0
        print "YYYYY You changed the sum.txt file..."
        #rc=raw_input("YYYYY You changed the sum.txt file...y/n to del ")
        #if(rc.lower() == 'y'):
            #mf.runcmd("rm -i %s"%(qcpath),ropt)

    #cmd='rm -i %s'%(qcpath)
    #mf.runcmd(cmd,ropt)

    return(rcQC)
    

def doMd2Md3Mrg(stmid,doM2=1,doRedo=0,qc2paths=1,
                doGenChk=0,override=0,
                bd2Update=0,
                ropt='',verb=0):
    
    (mpath,mpathBT)=getSrcSumTxt(stmid,bd2Update=bd2Update,verb=1)
    
    savPath="%s-SAV"%(mpath)
    if(mpathBT != None):
        savPathBT="%s-SAV"%(mpathBT)
    else:
        savPathBT=None
        savThereBT=0
    
    savThere=(MF.getPathNlines(savPath) > 0)
    if(not(savThere)):
        cmd="cp %s %s"%(mpath,savPath)
        mf.runcmd(cmd,ropt)
        
    # -- BT
    if(mpathBT != None):
        savThereBT=(MF.getPathNlines(savPathBT) > 0)
        if(not(savThereBT)):
            cmd="cp %s %s"%(mpathBT,savPathBT)
            mf.runcmd(cmd,ropt)
            
    if(doRedo):
        if(savThere):
            cmd="cp -i %s %s"%(savPath,mpath)
            mf.runcmd(cmd,ropt)
        if(savThereBT):
            cmd="cp -i %s %s"%(savPathBT,mpathBT)
            mf.runcmd(cmd,ropt)
                        
    # -- first get paths and do clean
    #
    rcM3=getMD3Opaths(mpath,doM2=1,verb=1)
    (opath,opathS,opathThere,opathSThere,ofile,ofileS,sdir,
     isBT,sfile,stmDev,ostm1id,sname,stm1id,stm9xid,basin)=rcM3
    print 'QQ!!!',rcM3
    
    # -- get the NN if dev
    #
    gendtg=None
    if(stmDev == 'DEV' and doGenChk):
        (mpath9X,mpathBT9x)=getSrcSumTxt(stm9xid,bd2Update=bd2Update,verb=0)
        rcM39X=getMD3Opaths(mpath9X,verb=verb)
        opathS39X=rcM39X[1]
        opathS39XThere=rcM39X[3]
        
        gendtg=last9xdtg=None
        if(opathS39XThere):
            m3sum9x=open(opathS39X).readlines()
            mm=m3sum9x[0].strip().split(',')
            gendtg=mm[-3]
            
        if(opathSThere):
            m3sum=open(opathS).readlines()
            mm=m3sum[0].strip().split(',')
            last9xdtg=mm[10]
            
        if(gendtg != None and last9xdtg != None):
            gen9xdtg=dtginc(gendtg,-6)
            
            gen9xdiff=dtgdiff(gen9xdtg,last9xdtg)
            
            if(gen9xdiff != 0):
                print 'gendtg:    ',gendtg
                print 'last9xdtg: ',last9xdtg
                print 'gen9xdtg:  ',gen9xdtg
                print 'gen9xdiff:  %4.0f'%(gen9xdiff)
                    
                print 'RRREEEDDDOOO dev 9x: ',stmid,' NN: ',stm9xid,'gen9xdiff: %4.0f'%(gen9xdiff)
                if(gen9xdiff < 0.0 and not(override)):
                    print 'PPPPPPPPPPPPPPPPPPPPPPPPP with -sum.txt'
                    print 'original  opath: ',opath
                    print 'original opathS: ',opathS
                    cmd="meld %s %s"%(mpath9X,mpath)
                    runcmd(cmd)
                    
                    cmd="m-md3-All.py -S %s -O "%(stmid)
                    mf.runcmd(cmd)

                print 'original  opath: ',opath
                print 'original opathS: ',opathS

                # -- save original with too many dtgs...
                #
                cropt='norun'
                cropt=''

                cmd="cp %s %s-SAV"%(opath,opath)
                mf.runcmd(cmd,cropt)
            
                cmd="cp %s %s-SAV"%(opathS,opathS)
                mf.runcmd(cmd,cropt)
                
                (odir,ofile)=os.path.split(opath)
                lmask="%s/*lsd*"%(odir)
                lfiles=glob.glob(lmask)
                if(len(lfiles) > 0):

                    for lfile in lfiles:
                        cmd="rm %s"%(lfile)
                        mf.runcmd(cmd,cropt)
                        
                override=1
            
            
            
        
        
    
    if(not(override) and opathSThere and opathThere):
        print 'WWW md3 paths already there...and override=0...return opath'
        opath3=None
        rc=(opath3,mpath,mpathBT,savPath,savPathBT)
        return(rc)
    elif(opathThere):
        rc=cleanMD3Opaths(sdir,ostm1id)

    # -- merge m2 first...
    #
    mpathm=mpath
    print '000---1111',doM2,mpath,mpathBT
    if(doM2):
        mpathm=mergeMD(mpath, mpathBT)

    (mpath3,m3sum,rcsum)=makeMD3(mpathm,rcM3,gendtg=gendtg,doM2=doM2,verb=verb)
    mpath3BT=m3sumBT=rcsumBT=None
    if(mpathBT != None and IsNN(stmid)): 
        rcM3=getMD3Opaths(mpathBT,doM2=doM2,verb=verb)
        (mpath3BT,m3sumBT,rcsumBT)=makeMD3(mpathBT,rcM3,verb=verb)

    if(verb):
        print 'mpath:   ',mpath
        print 'mpath3:  ',mpath3,m3sum,rcsum
        print 'mpathBT: ',mpathBT
        print 'mpath3BT: ',mpath3BT,m3sumBT,rcsumBT

    opath3=opath39X=None
    #if(mpathBT != None and IsNN(stmid)):
    if(not(doM2)):
        opath3=mergeMD3(mpath3, mpath3BT,doM2=doM2,verb=verb)
    else:
        opath3=mpath3
    
    rc=(opath3,mpath,mpathBT,savPath,savPathBT)
    return(rc)


def doMd2Md3MrgGenChk(stmid,doM2=1,doRedo=0,qc2paths=1,doGenChk=0,
                      bd2Update=0,
                      override=0,ropt='',verb=0):
    
    (mpath,mpathBT)=getSrcSumTxt(stmid,bd2Update=bd2Update,verb=0)
    
    savPath="%s-SAV"%(mpath)
    if(mpathBT != None):
        savPathBT="%s-SAV"%(mpathBT)
    else:
        savPathBT=None
        savThereBT=0
    
    savThere=(MF.getPathNlines(savPath) > 0)
    if(not(savThere)):
        cmd="cp %s %s"%(mpath,savPath)
        mf.runcmd(cmd,ropt)
        
    # -- BT
    if(mpathBT != None):
        savThereBT=(MF.getPathNlines(savPathBT) > 0)
        if(not(savThereBT)):
            cmd="cp %s %s"%(mpathBT,savPathBT)
            mf.runcmd(cmd,ropt)
            
    if(doRedo):
        if(savThere):
            cmd="cp -i %s %s"%(savPath,mpath)
            mf.runcmd(cmd,ropt)
        if(savThereBT):
            cmd="cp -i %s %s"%(savPathBT,mpathBT)
            mf.runcmd(cmd,ropt)
                        
    # -- first get paths and do clean
    #
    
    rcM3=getMD3Opaths(mpath,doM2=1,verb=1)
    (opath,opathS,opathThere,opathSThere,ofile,ofileS,sdir,
     isBT,sfile,stmDev,ostm1id,sname,stm1id,stm9xid,basin)=rcM3
    
    
    # -- get the NN if dev
    #
    gendtg=None
    if(stmDev == 'NN' and doGenChk):
        
        (mpath9X,mpathBT9x)=getSrcSumTxt(stm9xid,bd2Update=bd2Update,verb=1)
        
        rcM39X=getMD3Opaths(mpath9X,verb=1)
        opathS39X=rcM39X[1]
        opathS39XThere=rcM39X[3]
        
        print 'asdf',opathS39X,opathS39XThere
        print 'mmmm',mpath,mpathBT
        print 'rrr333',rcM3
        print 'rrr999',rcM39X

        if(not(opathS39XThere)):
            mpathm=mergeMD(mpath, mpathBT)
            gendtg=None
            (mpath3,m3sum,rcsum)=makeMD3(mpathm,rcM3,gendtg=gendtg,doM2=doM2,verb=verb)
    
            (mpath3BT,m3sumBT,rcsumBT)=makeMD3(mpathBT,rcM3,verb=verb)
            (mpath39X,m3sum9X,rcsum9X)=makeMD3(mpath9X,rcM39X,verb=verb)
    
            print 'mpath:    ',mpath
            print 'mpath3:   ',mpath3,m3sum,rcsum
            print 'mpathBT:  ',mpathBT
            print 'mpath3BT: ',mpath3BT,m3sumBT,rcsumBT
            print 'mpath39X: ',mpath39X,m3sum9X,rcsum9X
        
        
        # -- get last9xdtg and gendtg
        #
        gendtg=last9xdtg=None
        
        # -- last9xdtg from 9x
        #
        if(opathS39XThere):
            m3sum9x=open(opathS39X).readlines()
            mm=m3sum9x[0].strip().split(',')
            last9xdtg=mm[10]
            
        # -- gendtg from NN
        #
        if(opathSThere):
            m3sum=open(opathS).readlines()
            mm=m3sum[0].strip().split(',')
            gendtg=mm[-3]
            
        
        if(gendtg != None and last9xdtg != None):
            
            gen9xdtg=dtginc(gendtg,-6)
            
            gen9xdiff=dtgdiff(gen9xdtg,last9xdtg)
            
            print 'gggg',gendtg,last9xdtg,gen9xdtg,gen9xdiff

            if(gen9xdiff > 0 or override):
                print 'gendtg:    ',gendtg
                print 'last9xdtg: ',last9xdtg
                print 'gen9xdtg:  ',gen9xdtg
                print 'gen9xdiff:  %4.0f'%(gen9xdiff)
                    
                print 'RRREEEDDDOOO dev 9x: ',stmid,' NN: ',stm9xid,'gen9xdiff: %4.0f'%(gen9xdiff)
                print 'original  opath: ',opath
                print 'original opathS: ',opathS
                cmd="meld %s %s %s"%(mpath9X,mpath,mpathBT)
                print 'mmmccc',cmd
                mf.runcmd(cmd)

                # -- now regen md3
                #
                mpathm=mergeMD(mpath, mpathBT)
                (mpath3,m3sum,rcsum)=makeMD3(mpathm,rcM3,gendtg=gendtg,doM2=doM2,verb=verb)
                mpath3BT=m3sumBT=rcsumBT=None
                if(mpathBT != None and IsNN(stmid)): 
                    rcM3=getMD3Opaths(mpathBT,doM2=doM2,verb=verb)
                    (mpath3BT,m3sumBT,rcsumBT)=makeMD3(mpathBT,rcM3,verb=verb)
                    (mpath39X,m3sum9X,rcsum9X)=makeMD3(mpath9X,rcM39X,verb=verb)
            
                if(verb):
                    print 'mpath:    ',mpath
                    print 'mpath3:   ',mpath3,m3sum,rcsum
                    print 'mpathBT:  ',mpathBT
                    print 'mpath3BT: ',mpath3BT,m3sumBT,rcsumBT
                    print 'mpath39X: ',mpath39X,m3sum9X,rcsum9X
                    
            
                opath3=opath39X=None
                #if(mpathBT != None and IsNN(stmid)):
                opath3=mergeMD3(mpath3, mpath3BT,doM2=0,verb=verb)
                
                # -- now do 9x
                #
                opath39X=mergeMD3(mpath39X, mpath3BT,doM2=0,verb=verb)


                print 'OOOOONNNN',opath3
                print 'OOOOO9999',opath39X
                rc=(opath3,mpath,mpathBT,savPath,savPathBT)
                
                return(rc)
            


def setModel2(model,bdir2=None):

    model=model.lower()
    from sBTcl import Era5
    
    if(model == 'era5'): return(Era5(bdir2=bdir2))

    ####lif(model == 'fimx'): return(Fimx())
    else:
        print 'EEE(M2.setModel2) invalid model: ',model,' in setModel2...sayoonara'
        sys.exit()
        return(None)

    return(fmodel)


# -- tttttcccccVVVVVMMMMM methods
#
def VeriTcFlag(tcind,tcwarn):
    vflg=0
    if(tcind == 'TC' or tcwarn == 'WN'):
        vflg=1

    return(vflg)


def ParseMdeckCard2Btcs(mdcard):

#new format for mdeck
#
#  0 2007090800
#  1 09L.2007
#  2 020
#  3 1009
#  4 23.5
#  5 274.5
#  6 -999
#  7 -999
#  8 360.0
#  9 0.0
#  10 0
#  11 FL:
#  12 NT
#  13 DB
#  14 NC
#  15 NC
#  16 NW
#  17 LF:
#  18 0.00
#  19 TDO:
#  20 ___
#  21 C:
#  22 -99.9
#  23 -999.9
#  24 -999
#  25 999.9
#  26 99.9
#  27 ______
#  28 W:
#  29 -99.9
#  30 -999.9
#  31 -999
#  32 999.9
#  33 99.9
#  34 RadSrc:
#  35 none
#  36 r34:
#  37 -999
#  38 -999
#  39 -999
#  40 -999
#  41 r50:
#  42 -999
#  43 -999
#  44 -999
#  45 -999
#  46 CP/Roci:
#  47 9999.0
#  48 999.0
#  49 CRm:
#  50 999.0
#  51 CDi:
#  52 999.0
#  53 Cdpth:
#  54 K

    tt=mdcard.split()
    ntt=len(tt)

    #for n in range(0,ntt):
    #    print 'mmmmmmm ',n,tt[n]

    i=0

    dtg=tt[i] ; i=i+1
    sid=tt[i] ; i=i+1
    bvmax=float(tt[i])  ; i=i+1
    bpmin=float(tt[i]) ; i=i+1
    blat=float(tt[i]) ; i=i+1
    blon=float(tt[i]) ; i=i+1
    r34=float(tt[i]) ; i=i+1
    r50=float(tt[i]) ; i=i+1
    bdir=float(tt[i]) ; i=i+1
    bspd=float(tt[i]) ; i=i+1
    tsnum=int(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    flgtc=tt[i] ; i=i+1
    flgind=tt[i] ; i=i+1
    flgcq=tt[i] ; i=i+1
    flgwn=tt[i] ; i=i+1
    dum=tt[i] ; i=i+1
    lf=float(tt[i]) ; i=i+1
    dum=tt[i] ; i=i+1
    tdo=tt[i] ; i=i+1

    ic=21
    cqlat=float(tt[ic])  ; ic=ic+1
    cqlon=float(tt[ic])  ; ic=ic+1
    cqvmax=float(tt[ic]) ; ic=ic+1
    cqdir=float(tt[ic])  ; ic=ic+1
    cqspd=float(tt[ic])  ; ic=ic+1
    cqpmin=float(tt[ic])  ; ic=ic+1

    iw=29
    wlat=float(tt[iw])  ; iw=iw+1
    wlon=float(tt[iw])  ; iw=iw+1
    wvmax=float(tt[iw]) ; iw=iw+1

    if(ntt == 55):
        ir=37
        r34ne=int(tt[ir]) ; ir=ir+1
        r34se=int(tt[ir]) ; ir=ir+1
        r34sw=int(tt[ir]) ; ir=ir+1
        r34nw=int(tt[ir]) ; ir=ir+2

        r50ne=int(tt[ir]) ; ir=ir+1
        r50se=int(tt[ir]) ; ir=ir+1
        r50sw=int(tt[ir]) ; ir=ir+1
        r50nw=int(tt[ir]) ; ir=ir+2

        ir=47
        poci=float(tt[ir]) ; ir=ir+1
        roci=float(tt[ir]) ; ir=ir+2

        rmax=float(tt[ir]) ; ir=ir+2
        reye=float(tt[ir]) ; ir=ir+2
        tcdepth=tt[ir]

    else:
        r34ne=r34se=r34sw=r34nw=-999.0
        r50ne=r50se=r50sw=r50nw=-999.0
        poci=roci=rmax=reye=-999.0
        tcdepth='X'

    r34quad=[r34ne,r34se,r34sw,r34nw]
    r50quad=[r50ne,r50se,r50sw,r50nw]

    if(cqdir > 720.0):
        cqdir=-999.9
        cqspd=-99.9

    btdic=[flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum]
    cqdic=[cqlat,cqlon,cqvmax,cqdir,cqspd,cqpmin]
    bwdic=[bvmax,r34,r50,rmax,reye,poci,roci,tcdepth]
    btc=[blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad]

    return(btc)



def ParseMdeck2Btcs(dtgs,mdcards):

    btcs={}

    for dtg in dtgs:
        mdcard=mdcards[dtg]
        btc=ParseMdeckCard2Btcs(mdcard)
        btcs[dtg]=btc

    return(btcs)



def GetMdeckBts(stmid,dofilt9x=1,verb=0):

##    mdcards=findtc(stmid,dofilt9x)
    mdcards=findMdeckTC(stmid,do9x=dofilt9x)
    if(len(mdcards) == 0):
        print 'WWW(GetMdeckBts): mdcards = []'
        return(None,None)
    else:
        dtgs=mdcards.keys()
        dtgs.sort()
        bts=ParseMdeck2Btcs(dtgs,mdcards)
        return(dtgs,bts)


def findMdeckTC(tstm,do9x=1,verb=0):

    from tcbase import MdeckDir
    
    tt=tstm.split('.')

    if(len(tt) != 2):
        print 'EEE invalid tstm in findMdckTC: ',tstm
        sys.exit()

    tstmid=tt[0].upper()
    yyyy=tt[1]

    mddir="%s/%s"%(MdeckDir,yyyy)
    mdmask="%s/mdeck.*.%s.*.txt"%(mddir,tstmid)
    mdpaths=glob.glob(mdmask)

    omdcards={}

    if(len(mdpaths) > 0):

        mdpath=mdpaths[-1]
        mdcards=open(mdpath).readlines()

        for mdcard in mdcards:
            dtg=mdcard.split()[0]
            omdcards[dtg]=mdcard


    return(omdcards)


def GetMdeckBts(stmid,dofilt9x=1,verb=0):

##    mdcards=findtc(stmid,dofilt9x)
    mdcards=findMdeckTC(stmid,do9x=dofilt9x)
    if(len(mdcards) == 0):
        print 'WWW(GetMdeckBts): mdcards = []'
        return(None,None)
    else:
        dtgs=mdcards.keys()
        dtgs.sort()
        bts=ParseMdeck2Btcs(dtgs,mdcards)
        return(dtgs,bts)



def GetBtcardsLatLonsFromMdeck(stmid,dtg,nhback=48,nhplus=120,verb=0):

    btcards=[]
    btcardsgt0=[]

    lats=[]
    lons=[]
    vmaxs=[]
    pmins=[]

    (btdtgs,btcs)=GetMdeckBts(stmid,dofilt9x=0,verb=verb)

    if(btdtgs == None):
        print 'WWW(tcbase.GetBtcardsLatLonsFromMdeck): no bts for stmid: ',stmid
        return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)


    btdtgs.sort()

    obtdtgs=[]
    obtdtgsgt0=[]
    for btdtg in btdtgs:
        dt=mf.dtgdiff(dtg,btdtg)
        if(dt <= 0 and dt >= -nhback):
            obtdtgs.append(btdtg)
        if(dt >= 0):
            obtdtgsgt0.append(btdtg)


    btcard="N bt: %d"%(len(obtdtgs))
    btcards.append(btcard)

    for dtg in obtdtgs:

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcards.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    btcardgt0="N bt: %d"%(len(obtdtgsgt0))
    btcardsgt0.append(btcardgt0)

    nbt0=0
    # -- 20130703 -- caused gfs2 to crash on plotting in lsdiag
    if(len(obtdtgsgt0) > 0):
        dtg0=obtdtgsgt0[0]

    for dtg in obtdtgsgt0:
        dt=mf.dtgdiff(dtg0,dtg)
        if(dt%12): continue
        dhplus=mf.dtgdiff(dtg0,dtg)
        if(dhplus > nhplus): continue

        nbt0=nbt0+1

        (blat,blon,bvmax,bpmin,bdir,bspd,btdic,cqdic,bwdic,r34quad,r50quad)=btcs[dtg]
        (flgtc,flgind,flgcq,flgwn,tdo,lf,cqlat,cqlon,cqvmax,wlat,wlon,wvmax,tsnum)=btdic

        flgveri=VeriTcFlag(flgtc,flgwn)

        btcard="%s %6.1f %6.1f %3d %2d %6.0f"%(dtg,blat,blon,int(bvmax),flgveri,bpmin)
        btcardsgt0.append(btcard)
        lats.append(blat)
        lons.append(blon)
        vmaxs.append(bvmax)
        pmins.append(bpmin)

    # replace nbt with count from culling out tau12 increment

    btcardsgt0[0]="N bt: %d"%(nbt0)
    return(btcards,btcardsgt0,lats,lons,vmaxs,pmins)


def getmdecktcs(ddir,cdtg,dofilt9x=0,verb=0):

    bdmdeckpath="%s/btops.%s.txt"%(ddir,cdtg)
    try:
        tcs=open(bdmdeckpath).readlines()
    except:
        tcs=[]

    otcs=[]
    if(len(tcs) > 0):
        for tc in tcs:
            stm=tc.split()[1]
            stm3id=stm.split('.')[0]
            if(not(dofilt9x and int(stm3id[0:2]) >= 90)):
                otcs.append(tc)


    return(otcs)



def findtcs(cdtg,dofilt9x=0,srcopt='btops',doLF=1,verb=0):

    from w2local import W2
    w2=W2()
    
    from tcbase import TcCarqDatDir
    if(srcopt == 'btops'):
        yyyy=cdtg[0:4]
        ddir="%s/%s"%(TcCarqDatDir,yyyy)
        tcs=getmdecktcs(ddir,cdtg,dofilt9x)
        return(tcs)

    #-----------------------------------------------------------------
    #
    # if srcopt != btops, then go for dtg in mdecks directly
    #
    #-----------------------------------------------------------------

    #
    # setup land-sea fraction
    #

    if(doLF):
        lf=w2.SetLandFrac()

    stms=[]
    stmcards={}

    yyyy=cdtg[0:4]
    mm=cdtg[4:6]

    yyyym1=int(yyyy)-1
    yyyym1=str(yyyym1)
    yyyyp1=int(yyyy)+1
    yyyyp1=str(yyyyp1)

    (shemoverlap,shyyyy,shyyyyp1)=CurShemOverlap(cdtg)

    tcs=[]
    mdtcs=[]

    doprevyear=0
    if(mm == '01' or mm == '02'): doprevyear=1

    mddir=w2.TcMdecksFinalDir
    mdprefix='MdOps'

    mdmkyyyy="%s/%s/%s.???.*"%(mddir,yyyy,mdprefix)
    mdmkyyyym1="%s/%s/%s.???.*"%(mddir,yyyym1,mdprefix)
    mdmkyyyyp1="%s/%s/%s.???.*"%(mddir,yyyyp1,mdprefix)

    mdp=glob.glob(mdmkyyyy)
    mdpm1=glob.glob(mdmkyyyym1)
    mdpp1=glob.glob(mdmkyyyyp1)

    if(verb):
        print 'MMM mdmkyyyy:   ',mdmkyyyy
        print 'MMM mdmkyyyym1: ',mdmkyyyym1
        print 'MMM mdmkyyyyp1: ',mdmkyyyyp1

        print 'PPPPPPPPPPP doprevyear: ',doprevyear,' shemoverlap ',shemoverlap

    if(doprevyear):

        GrepCdtgMdecks(mdtcs,cdtg,mdpm1)

        if(shemoverlap):
            GrepCdtgMdecks(mdtcs,cdtg,mdpp1)

        GrepCdtgMdecks(mdtcs,cdtg,mdp)

    else:

        if(shemoverlap):
            GrepCdtgMdecks(mdtcs,cdtg,mdpp1)

        GrepCdtgMdecks(mdtcs,cdtg,mdp)

    if(verb):
        for tc in mdtcs:
            print 'tcccccccccccccccccccccccccccccc',tc[:-1]

    ntcs=len(mdtcs)

    # -- remove dups, increas drmin for 9X
    #
    mdtcs=DupChkTcs(mdtcs,drmin=1.5,verb=verb)

    if(ntcs != 0):

        ntcok=0
        for tc in mdtcs:

            tt=tc.split()

            btyear=tt[0]
            btid=tt[1]

            dtg=tt[2]
            stmid="%s.%s"%(btid,btyear)

            vmax=tt[4]
            pmin=tt[5]
            stmnum=int(stmid[0:2])

            doit=1
            if(dofilt9x and stmnum >= 90): doit=0

            if(doit):
                stms.append(stmid)
                stmcards[stmid]=tc
                ntcok=ntcok+1

        if(ntcok == 0):
            tcs=[]
            return(tcs)

        stms=mf.uniq(stms)

        for stm in stms:
            tcs.append(stmcards[stm])

    return(tcs)


def GetOpsRefTrk(dtg,stmid,rtaus=None,override=0,verb=0,btc=None,inputAD=None):

    from w2local import W2
    w2=W2()

    print  'qqqqq====',stmid
    rc=getStmParams(stmid, convert9x=1)
    stm1id=rc[-1]
    astm2id=rc[-2]
    
    stmid=stm1id
    if(rtaus != None):
        taus=rtaus
    else:
        taus=[0,12,24,36,48,60,72,84,96,108,120]
    year=dtg[0:4]

    # --- set up the reftrk path
    #

    refbdir=w2.TcRefTrkDatDir
    refdir="%s/%s"%(refbdir,year)
    mf.ChkDir(refdir,'mk')
    refpath="%s/reftrk.%s.%s.txt"%(refdir,stmid,dtg)

    if(verb): print 'RRR in GetOpsRefTrk refpath: ',refpath,MF.GetPathSiz(refpath)


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- set up the reftrk path and open if there

    # -- always get storm ops adecks and make ad Adeck obj
    #
    snum=stmid[0:2]
    b1id=stmid[2].upper()
    b2id=Basin1toBasin2[b1id].lower()

    if(IsJtwcBasin(b1id)):
        sdir="%s/%s"%(w2.TcAdecksJtwcDir,year)
        (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)
        if(shemoverlap):
            mask=[]
            sdir="%s/%s"%(w2.TcAdecksJtwcDir,cy)
            sdirp1="%s/%s"%(w2.TcAdecksJtwcDir,cyp1)
            mask.append("%s/a%s%s%s.dat"%(sdir,b2id,snum,cy))
            mask.append("%s/a%s%s%s.dat"%(sdirp1,b2id,snum,cyp1))
        else:
            mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)

        oaids=opsaids['jtwc']

    elif(IsNhcBasin(b1id)):
        sdir="%s/%s"%(w2.TcAdecksNhcDir,year)
        mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)
        oaids=opsaids['nhc']

    else:
        print 'EEE(tcbase.GetOpsRefTrk): invalid b1id: ',b1id,'is not jt|nhc'
        sys.exit()

    #from adCL import Adeck
    #from adVM import GetStm2idFromAdeck
    #ad=Adeck(mask)


    # -- if not there get the adecks and make
    #
    if(MF.GetPathSiz(refpath) <= 0 or override):

        # get storm ops adecks and make the ad Adeck obj
        #
        snum=stmid[0:2]
        b1id=stmid[2].upper()
        b2id=Basin1toBasin2[b1id].lower()
        if(IsJtwcBasin(b1id)):
            sdir="%s/%s"%(w2.TcAdecksJtwcDir,year)
            (shemoverlap,cy,cyp1)=CurShemOverlap(dtg)
            if(shemoverlap):
                mask=[]
                sdir="%s/%s"%(w2.TcAdecksJtwcDir,cy)
                sdirp1="%s/%s"%(w2.TcAdecksJtwcDir,cyp1)
                mask.append("%s/a%s%s%s.dat"%(sdir,b2id,snum,cy))
                mask.append("%s/a%s%s%s.dat"%(sdirp1,b2id,snum,cyp1))
            else:
                mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)

            oaids=opsaids['jtwc']

        elif(IsNhcBasin(b1id)):
            sdir="%s/%s"%(w2.TcAdecksNhcDir,year)
            mask="%s/a%s%s%s.dat"%(sdir,b2id,snum,year)
            oaids=opsaids['nhc']

        from tcbase import Adeck,GetStm2idFromAdeck
        ad=Adeck(mask)

        try:
            REF=open(refpath,'w')
        except:
            print 'EEE unable to open reftrk output: ',refpath
            sys.exit()

        # -- check if refcards sufficent...if not, try to regen...
        #
        if(REF != None):
            refcards=open(refpath).readlines()
            if(len(refcards) <= 1):
                REF=None

        refcards=None

    else:
        
        # -- get the reftrk...
        #
        REF=None
        refcards=open(refpath).readlines()


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- parse reftrk if already done
    #

    reflats=[]
    reflons=[]

    if(REF == None and refcards != None):

        reftrk={}

        nr=len(refcards)
        tt=refcards[0].split()

        refdtg=tt[1]
        refstmid=tt[3]
        refaid=tt[5]
        reftau=tt[7]

        if(verb):
            print 'RRR reftrk: ',refpath
            print 'RRR reftrk: ',refdtg,refstmid,refaid,reftau,nr

        for n in range(1,nr):
            tt=refcards[n].split()
            tau=int(tt[0])
            lat=float(tt[1])
            lon=float(tt[2])
            vmax=float(tt[3])
            pmin=float(tt[4])
            reftrk[tau]=(lat,lon,vmax,pmin)
            reflats.append(lat)
            reflons.append(lon)
            if(verb): print 'RRR lat,lon: ',lat,lon

        return(reflats,reflons,refaid,reftau,reftrk)


    #rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
    # -- otherwise make  it
    #

    try:
        REF=open(refpath,'w')
    except:
        print 'EEE unable to open reftrk output: ',refpath
        sys.exit()


    dd=ad.dtgs
    dd.sort()

    nposits=0

    gottau={}
    for tau in taus:
        gottau[tau]=0

    #
    # define a target tau
    #

    ttaus=[72,48,24]
    refaid=None
    reftau=None

    for ttau in ttaus:
        gottau[tau]=0

        for oaid in oaids:
            if(gottau[tau] == 0):
                try:
                    rc=ad.aidtrks[oaid,astm2id][dtg][ttau]
                    if(len(rc) >= 4): 
                        (lat,lon,pmin,vmax)=rc[0:4]
                    
                    #
                    # get the first posit...
                    #
                    gottau[ttau]=1
                    refaid=oaid
                    reftau=ttau
                    if(verb): print 'HHHHH ',ttau,oaid,gottau[ttau]
                    break

                except:
                    if(gottau[tau] == 0):
                        if(verb): print 'NNNN111 no tracks for ',oaid,astm2id,dtg,ttau

        if(gottau[ttau]):
            break

    # -- after loop see what aid is the ref and at what tau
    #

    b1id=stmid[2].lower()

    print 'RRR (refpath):',refpath
    print 'RRR  (reftrk):',dtg,stmid,b1id,refaid,reftau

    #---------------------------------------------------
    # get btcards
    # nhback=48 as the default or only consider previous 48 h of BT

    (btcards,btcardsgt0,btlats,btlons,btvmaxs,btpmins)=GetBtcardsLatLonsFromMdeck(stmid,dtg,verb=0)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 
    # for 9X storms, mdeck might not be there...findtcs and the pull out from btops.dtg.txt
    #

    if(len(btcards) == 0 or int(btcards[0].split()[2]) == 0):
        otcs=findtcs(dtg)
        print 'otcs ',otcs
        for tc in otcs:
            tt=tc.split()
            tstmid=tt[1]
            print 'otc: ',tc,tstmid
            if(stmid == tstmid):
                tvmax=tt[2]
                tpmin=tt[3]
                trlat=float(tt[4])
                trlon=float(tt[5])
                #
                # crossing the prime meridian -- for lant only
                #
                if(trlon <= primeMeridianChk and b1id == 'l'):
                    trlon=trlon+360.0

                reflats.append(trlat)
                reflons.append(trlon)

        print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW -- no mdeck for: ',stmid,' dtg: ',dtg,' using btops.DTG.txt',reflons,reflats

    #
    # write the reftrk data to REF
    #

    rcard="dtg: %s stmid: %s refaid: %s reftau: %s"%(dtg,stmid,refaid,reftau)
    REF.writelines(rcard+'\n')

    reftrk={}

    for btcard in btcards[1:]:
        tt=btcard.split()
        bdtg=tt[0]
        blat=float(tt[1])
        blon=float(tt[2])

        reflats.append(blat)
        reflons.append(blon)

        bvmax=float(tt[3])
        bvflg=tt[4]
        bpmin=float(tt[5])
        btau=mf.dtgdiff(dtg,bdtg)
        if(btau == 0): btau=-1
        reftrk[btau]=(blat,blon,bvmax,bpmin)
        rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f BT"%(btau,blat,blon,bvmax,bpmin)
        if(verb): print 'RRR rcard: ',rcard
        REF.writelines(rcard+'\n')


    nojoy=1
    for tau in taus:
        try:
            rc=ad.aidtrks[oaid,astm2id][dtg][tau]
            if(len(rc) >= 4):
                (lat,lon,vmax,pmin)=rc[0:4]

            #
            # crossing the prime meridian; mod to get madagacar
            #
            if(lon <= primeMeridianChk and b1id == 'l'):
                lon=lon+360.0

            reflats.append(lat)
            reflons.append(lon)
            reftrk[tau]=(lat,lon,vmax,pmin)
            rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,lat,lon,vmax,pmin,refaid)
            if(verb): print 'RRR rcard: ',rcard
            REF.writelines(rcard+'\n')
            nojoy=0

        except:
            None

    # -- no aids use climo motion 285 ; 12 kt
    #
    if(nojoy):

        btaus=reftrk.keys()
        btaus.sort()

        if(btc != None):
            (blat0,blon0,bvmax0,bpmin0)=btc[0:4]
        else:
            if(len(btaus) > 0 and btaus[-1] >= -6):
                (blat0,blon0,bvmax0,bpmin0)=reftrk[btaus[-1]]
            else:
                print 'EEEEEEEEEEEEEEE no bt or forecast track in tcbase.GetOpsRefTrk()'
                sys.exit()

        if(blat0 > 0.0):

            if(abs(blat0) < 25.0):
                clmdir=285
                clmspd=12
            else:
                clmdir=315
                clmspd=6

        else:

            if(abs(blat0) < 25.0):
                clmdir=265
                clmspd=12
            else:
                clmdir=225
                clmspd=6


        nt=len(taus)
        dtau=taus[1]-taus[0]
        refaid='MFCLM'
        for n in range(1,nt):
            if(n == 1):
                reflats.append(blat0)
                reflons.append(blon0)
                tau=taus[0]
                if(bvmax0 == None): bvmax0=-99.
                if(bpmin0 == None): bpmin0=-999.
                reftrk[tau]=(blat0,blon0,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,blat0,blon0,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')

                (rlat,rlon)=rumltlg(clmdir,clmspd,dtau,blat0,blon0)

                reflats.append(rlat)
                reflons.append(rlon)
                tau=taus[1]
                reftrk[tau]=(rlat,rlon,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,rlat,rlon,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')

            else:

                (blat0,blon0,bvmax0,bpmin0)=reftrk[taus[n-1]]
                (rlat,rlon)=rumltlg(clmdir,clmspd,dtau,blat0,blon0)

                reflats.append(rlat)
                reflons.append(rlon)
                tau=taus[n]
                reftrk[tau]=(rlat,rlon,bvmax0,bpmin0)
                rcard="%4i  %5.1f  %6.1f  %3.0f  %6.0f %s"%(tau,rlat,rlon,bvmax0,bpmin0,refaid)
                if(verb): print 'RRR rcard: ',rcard,' CCCCCCCCCClimo'
                REF.writelines(rcard+'\n')




    if(verb): print 'RRR(refpath): ',refpath
    REF.close()

    return(reflats,reflons,refaid,reftau,reftrk)



def getBasinLatLonsPrecise(basin):

    latlons=[]

    if(basin == 'global'):
        lat1=-30.0
        lat2=30.0
        lon1=0.0
        lon2=359.0
        
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'lant'):

        lat1=0.0
        lat2=30.0
        lon1=360.0-100.
        lon2=359.0

        lat1=0.0
        lat2=10.0
        lon2=360.0-10.0
        lon1=360.0-75.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=10.0
        lat2=15.0
        lon2=360.0-10.0
        lon1=360.0-85.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=15.0
        lat2=18.0
        lon2=360.0-10.0
        lon1=360.0-89.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=18.0
        lat2=30.0
        lon2=360.0-10.0
        lon1=360.0-97.0
        latlons.append((lat1,lat2,lon1,lon2))


    elif(basin == 'epac'):

        lat1=0.0
        lat2=10.0
        lon1=180.0
        lon2=360.0-75.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=10.0
        lat2=15.0
        lon1=180.0
        lon2=360.0-85.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=15.0
        lat2=18.0
        lon1=180.0
        lon2=360.0-89.0
        latlons.append((lat1,lat2,lon1,lon2))

        lat1=18.0
        lat2=30.0
        lon1=180.0
        lon2=360.0-97.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'wpac'):

        lat1=0.0
        lat2=30.0
        lon1=100.0
        lon2=180.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'shem'):

        lat1=-30.0
        lat2=0.0
        lon1=35.0
        lon2=360.0-150.0
        latlons.append((lat1,lat2,lon1,lon2))

    elif(basin == 'nio'):

        lat1=0.0
        lat2=30.0
        lon1=40.0
        lon2=100.0
        latlons.append((lat1,lat2,lon1,lon2))

    else:
        print 'EEE invalid basin in getBasinLatLon: ',basin
        sys.exit()

    return(latlons)


def getGentaus(gentau):

    if(gentau == 'all'):
        gentaus=[0,48,72,96,120,144]
        gentaus=[60,132]
        gentaus=[0,60,132]
        # -- d+2 (60) d+3 (84) d+5 (132)
        gentaus=[0,60,84,108,132]
        gentaus=[0,60,84,108,120,144,168]
        # era5
        gentaus=[0,24,48,72,96,120,144,168]

    elif(gentau == 'allgen'):
        gentaus=[72,96,120,144]

    elif(gentau == 'all24h'):
        gentaus=[0,24,48,72,96,120]
        gentaus=[0,24,72,120]

    else:
        gentaus=[]
        tt=gentau.split(',')
        for t in tt:
            try:
                gentaus.append(int(t))
            except:
                print 'WWW invalid tau in gentau: ',gentau

        gentaus=MF.uniq(gentaus)

    return(gentaus)

# -- CCCCCCCCCCCCCCCCCCCC -- wxmap2
#
from sBTcl import MFutils

def setGA(gaclass='gacore',Opts='',Bin='grads',Quiet=1,Window=0,verb=0,doLogger=0):

    if(gaclass == 'gacore'):

        MF.sTimer(tag='load grads gacore')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore')
        

        class W2GaCore(GaCore,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin=Bin, Echo=True, Opts=Opts, Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)
        

        ga=W2GaCore(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    if(gaclass == 'galats'):

        MF.sTimer(tag='load grads gacore - galats')
        from grads import GaCore,GrADSError
        MF.dTimer(tag='load grads gacore - galats')
        

        class W2GaLats(GaCore,GaLatsQ,GrADSError,MFbase):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)

                # -- lats vars
                #
                
                self.dtg=dtg
                self.model=model
                self._cmd=self.cmd2

                self.frequency=frequency

                self.regrid=regrid
                self.remethod=remethod
                self.smth2d=smth2d
                self.doyflip=doyflip
                self.reargs=reargs

                self.area='global'

                self.btau=btau
                self.etau=etau
                self.dtau=dtau

                if(taus == None):
                    self.taus=range(btau,etau+1,dtau)
                else:
                    self.taus=taus


                self("set_lats parmtab %s"%(ptable))
                self("set_lats convention %s"%(outconv))
                self("set_lats calendar %s"%(calendar))
                self("set_lats model %s"%(model))
                self("set_lats center %s"%(center))
                self("set_lats comment %s"%(comment))
                self("set_lats timeoption %s"%(timeoption))
                self("set_lats frequency %s"%(frequency))

                if(self.frequency == 'forecast_hourly'):
                    self("set_lats deltat %d"%(dtau))
                elif(self.frequency == 'forecast_minutes'):
                    self("set_lats deltat %d"%(dtau*60))

                self("set_lats gridtype %s"%(gridtype))

                if(hasattr(ga,'fh')):
                    self.fh=ga.fh
                else:
                    print 'EEE GaLats(Q) needs a fh object (file handle) in the grads.ga object'
                    sys.exit()

                ge.getFileMeta(self)


        ga=W2GaLats(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)



    elif(gaclass == 'ganum'):

        MF.sTimer(tag='load grads gacore-ganum')
        from grads import GaNum,GrADSError
        MF.dTimer(tag='load grads gacore-ganum')


        class W2GaNum(GaNum,W2GaBase,GrADSError):

            Quiet=1

            def __init__ (self, 
                          Bin='grads', Echo=True, Opts='', Port=False, 
                          Strict=False, Quiet=0, RcCheck=None, Verb=0, Window=None,
                          doLogger=doLogger):

                # --- standard gacore init
                #
                self.Bin=Bin
                self.Echo=Echo
                self.Opts=Opts
                self.Port=Port
                self.Strict=False
                self.Quiet=Quiet
                self.RcCheck=RcCheck
                self.Verb=Verb
                self.Window=Window
                self.doLogger=doLogger

                self.initGaCore()

                self.GrADSError=GrADSError

                self._cmd=self.__call__
                self.rl=self.rline
                self.rw=self.rword

                # -- instantiate a GradsEnv object, ge
                #
                self.ge=GradsEnv()
                self.ge._cmd=self.__call__
                self.ge.cmdQ=self.cmdQ

                self.ge._ga=self
                self.ge.rl=self.rline
                self.ge.rw=self.rword

                self.gp=GradsPlot(self,self.ge)



        ga=W2GaNum(Opts=Opts,Bin=Bin,Quiet=Quiet,Window=Window,doLogger=doLogger)
        

    # -- decorate with verb
    ga.verb=verb
    ga.ge.verb=verb

    ga.gxout=gxout(ga)
    ga.set=gxset(ga)
    ga.dvar=gxdefvar(ga)
    ga.get=gxget(ga)
        
    return(ga)


MF=MFutils()

