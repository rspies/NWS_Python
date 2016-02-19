#_calculate_basin_nlcd_summary.py
#Cody Moser
#cody.moser@amec.com
#AMEC
#Description: calculates basin % land classification
#from .xls files output from ArcGIS Model Builder

#import script modules
import glob
import os
import re

import numpy
import csv

####################################################################
#USER INPUT SECTION
####################################################################
#ENTER RFC
RFC = 'MBRFC'
#FOLDER PATH OF NLCD .xls DATA FILES
csv_folderPath = r'P:\\NWS\\GIS\\MBRFC\\Land Use\\data_files\\'
#FOLDER PATH OF BASIN SUMMARYNLCD .xls DATA FILES (!Must be different than csv_FolderPath!)
output_folderPath = r'P:\\NWS\\GIS\\MBRFC\\Land Use\\'
####################################################################
#END USER INPUT SECTION
####################################################################

print 'Script is Running...'

nlcd_file = open(output_folderPath + '_' + RFC + '_MT_Detailed_NLCD_Summary.csv', 'w')
nlcd_file.write('Basin,' + '%0,' + '%1,' + '%2,' + '%3,' + '%4,' + '%5,' + '%6,' + '%7,' + '%8,' + '%9,' + '%10,' + '%11,' + '%12,' + '%13,' + '%14,' + '%15,' + '%16,' + '%17,' + '%18,' + '%19,' + '%20,' + '%21,' + '%22,' + '%23,' + '%24,' + '%25,' + '%26,' + '%27,' + '%28,' + '%29,' + '%30,' + '%31,' + '%32,' + '%33,' + '%34,' + '%35,' + '%36,' + '%37,' + '%38,' + '%39,' + '%40,' + '%41,' + '%42,' + '%43,' + '%44,' + '%45,' + '%46,' + '%47,' + '%48,' + '%49,' + '%50,' + '%51,' + '%52,' + '%53,' + '%54,' + '%55,' + '%56,' + '%57,' + '%58,' + '%59,' + '%60,' + '%61,' + '%62,' + '%63,' + '%64,' + '%65,' + '%66,' + '%67,' + '%68,' + '%69,' + '%70,' + '%71,' + '%72,' + '%73,' + '%74,' + '%75,' + '%76,' + '%77,' + '%78,' + '%79,' + '%80,' + '%81,' + '%82,' + '%83,' + '%84,' + '%85,' + '%86,' + '%87,' + '%88,' + '%89,' + '%90,' + '%91,' + '%92,' + '%93,' + '%94,' + '%95,' + '%96,' + '%97,' + '%98,' + '%99,' + '%100,' + '%101,' + '%102,' + '%103,' + '%104,' + '%105,' + '%106,' + '%107,' + '%108,' + '%109,' + '%110,' + '%111,' + '%112,' + '%113,' + '%114,' + '%115,' + '%116,' + '%117,' + '%118,' + '%119,' + '%120,' + '%121,' + '%122,' + '%123,' + '%124,' + '%125,' + '%126,' + '%127,' + '%128,' + '%129,' + '%130,' + '%131,' + '%132,' + '%133,' + '%134,' + '%135,' + '%136,' + '%137,' + '%138,' + '%139,' + '%140,' + '%141,' + '%142,' + '%143,' + '%144,' + '%145,' + '%146,' + '%147,' + '%148,' + '%149,' + '%150,' + '%151,' + '%152,' + '%153,' + '%154,' + '%155,' + '%156,' + '%157,' + '%158,' + '%159,' + '%160,' + '%161,' + '%162,' + '%163,' + '%164,' + '%165,' + '%166,' + '%167,' + '%168,' + '%169,' + '%170,' + '%171,' + '%172,' + '%173,' + '%174,' + '%175,' + '%176,' + '%177,' + '%178,' + '%179,' + '%180,' + '%181,' + '%182,' + '%183,' + '%184,' + '%185,' + '%186,' + '%187,' + '%188,' + '%189,' + '%190,' + '%191,' + '%192,' + '%193,' + '%194,' + '%195,' + '%196,' + '%197,' + '%198,' + '%199,' + '%200,' + '%201,' + '%202,' + '%203,' + '%204,' + '%205,' + '%206,' + '%207,' + '%208,' + '%209,' + '%210,' + '%211,' + '%212,' + '%213,' + '%214,' + '%215,' + '%216,' + '%217,' + '%218,' + '%219,' + '%220,' + '%221,' + '%222,' + '%223,' + '%224,' + '%225,' + '%226,' + '%227,' + '%228,' + '%229,' + '%230,' + '%231,' + '%232,' + '%233,' + '%234,' + '%235,' + '%236,' + '%237,' + '%238,' + '%239,' + '%240,' + '%241,' + '%242,' + '%243,' + '%244,' + '%245,' + '%246,' + '%247,' + '%248,' + '%249,' + '%250,' + '%251,' + '%252,' + '%253,' + '%254,' + '%255,' +'\n')

#loop through NLCD .xls files in folderPath
for filename in glob.glob(os.path.join(csv_folderPath, "*.csv")):
    #print filename

    #Define output file name
    name = str(os.path.basename(filename)[:])
    name = name.replace('_MT_Detailed_NLCD.csv', '')
    #print name

    txt_file = open(filename, 'r')

    #csv_file = open(r'P:\\NWS\\GIS\\NERFC\\APriori\\temp.csv', 'w')
    csv_file = open(output_folderPath + 'temp.csv', 'w')
    
    grid = []
    
    for line in txt_file:
        #print line
        csv_file.write(line)

    csv_file.close()
    txt_file.close()

    csv_file = open(output_folderPath + 'temp.csv')
    
    data_file = csv.reader(csv_file, delimiter = ',')
    data_file.next()

    _0=[]
    _1=[]
    _2=[]
    _3=[]
    _4=[]
    _5=[]
    _6=[]
    _7=[]
    _8=[]
    _9=[]
    _10=[]
    _11=[]
    _12=[]
    _13=[]
    _14=[]
    _15=[]
    _16=[]
    _17=[]
    _18=[]
    _19=[]
    _20=[]
    _21=[]
    _22=[]
    _23=[]
    _24=[]
    _25=[]
    _26=[]
    _27=[]
    _28=[]
    _29=[]
    _30=[]
    _31=[]
    _32=[]
    _33=[]
    _34=[]
    _35=[]
    _36=[]
    _37=[]
    _38=[]
    _39=[]
    _40=[]
    _41=[]
    _42=[]
    _43=[]
    _44=[]
    _45=[]
    _46=[]
    _47=[]
    _48=[]
    _49=[]
    _50=[]
    _51=[]
    _52=[]
    _53=[]
    _54=[]
    _55=[]
    _56=[]
    _57=[]
    _58=[]
    _59=[]
    _60=[]
    _61=[]
    _62=[]
    _63=[]
    _64=[]
    _65=[]
    _66=[]
    _67=[]
    _68=[]
    _69=[]
    _70=[]
    _71=[]
    _72=[]
    _73=[]
    _74=[]
    _75=[]
    _76=[]
    _77=[]
    _78=[]
    _79=[]
    _80=[]
    _81=[]
    _82=[]
    _83=[]
    _84=[]
    _85=[]
    _86=[]
    _87=[]
    _88=[]
    _89=[]
    _90=[]
    _91=[]
    _92=[]
    _93=[]
    _94=[]
    _95=[]
    _96=[]
    _97=[]
    _98=[]
    _99=[]
    _100=[]
    _101=[]
    _102=[]
    _103=[]
    _104=[]
    _105=[]
    _106=[]
    _107=[]
    _108=[]
    _109=[]
    _110=[]
    _111=[]
    _112=[]
    _113=[]
    _114=[]
    _115=[]
    _116=[]
    _117=[]
    _118=[]
    _119=[]
    _120=[]
    _121=[]
    _122=[]
    _123=[]
    _124=[]
    _125=[]
    _126=[]
    _127=[]
    _128=[]
    _129=[]
    _130=[]
    _131=[]
    _132=[]
    _133=[]
    _134=[]
    _135=[]
    _136=[]
    _137=[]
    _138=[]
    _139=[]
    _140=[]
    _141=[]
    _142=[]
    _143=[]
    _144=[]
    _145=[]
    _146=[]
    _147=[]
    _148=[]
    _149=[]
    _150=[]
    _151=[]
    _152=[]
    _153=[]
    _154=[]
    _155=[]
    _156=[]
    _157=[]
    _158=[]
    _159=[]
    _160=[]
    _161=[]
    _162=[]
    _163=[]
    _164=[]
    _165=[]
    _166=[]
    _167=[]
    _168=[]
    _169=[]
    _170=[]
    _171=[]
    _172=[]
    _173=[]
    _174=[]
    _175=[]
    _176=[]
    _177=[]
    _178=[]
    _179=[]
    _180=[]
    _181=[]
    _182=[]
    _183=[]
    _184=[]
    _185=[]
    _186=[]
    _187=[]
    _188=[]
    _189=[]
    _190=[]
    _191=[]
    _192=[]
    _193=[]
    _194=[]
    _195=[]
    _196=[]
    _197=[]
    _198=[]
    _199=[]
    _200=[]
    _201=[]
    _202=[]
    _203=[]
    _204=[]
    _205=[]
    _206=[]
    _207=[]
    _208=[]
    _209=[]
    _210=[]
    _211=[]
    _212=[]
    _213=[]
    _214=[]
    _215=[]
    _216=[]
    _217=[]
    _218=[]
    _219=[]
    _220=[]
    _221=[]
    _222=[]
    _223=[]
    _224=[]
    _225=[]
    _226=[]
    _227=[]
    _228=[]
    _229=[]
    _230=[]
    _231=[]
    _232=[]
    _233=[]
    _234=[]
    _235=[]
    _236=[]
    _237=[]
    _238=[]
    _239=[]
    _240=[]
    _241=[]
    _242=[]
    _243=[]
    _244=[]
    _245=[]
    _246=[]
    _247=[]
    _248=[]
    _249=[]
    _250=[]
    _251=[]
    _252=[]
    _253=[]
    _254=[]
    _255=[]




    Count = []

    #GET THE RASTER GRID COUNT OF EACH LAND CLASSIFICATION
    for row in data_file:
        Value = str(row[1])
        count = float(row[2])
        if Value == '0':
            _0.append(count)
            Count.append(count)
        if Value == '1':
            _1.append(count)
            Count.append(count)
        if Value == '2':
            _2.append(count)
            Count.append(count)
        if Value == '3':
            _3.append(count)
            Count.append(count)
        if Value == '4':
            _4.append(count)
            Count.append(count)
        if Value == '5':
            _5.append(count)
            Count.append(count)
        if Value == '6':
            _6.append(count)
            Count.append(count)
        if Value == '7':
            _7.append(count)
            Count.append(count)
        if Value == '8':
            _8.append(count)
            Count.append(count)
        if Value == '9':
            _9.append(count)
            Count.append(count)
        if Value == '10':
            _10.append(count)
            Count.append(count)
        if Value == '11':
            _11.append(count)
            Count.append(count)
        if Value == '12':
            _12.append(count)
            Count.append(count)
        if Value == '13':
            _13.append(count)
            Count.append(count)
        if Value == '14':
            _14.append(count)
            Count.append(count)
        if Value == '15':
            _15.append(count)
            Count.append(count)
        if Value == '16':
            _16.append(count)
            Count.append(count)
        if Value == '17':
            _17.append(count)
            Count.append(count)
        if Value == '18':
            _18.append(count)
            Count.append(count)
        if Value == '19':
            _19.append(count)
            Count.append(count)
        if Value == '20':
            _20.append(count)
            Count.append(count)
        if Value == '21':
            _21.append(count)
            Count.append(count)
        if Value == '22':
            _22.append(count)
            Count.append(count)
        if Value == '23':
            _23.append(count)
            Count.append(count)
        if Value == '24':
            _24.append(count)
            Count.append(count)
        if Value == '25':
            _25.append(count)
            Count.append(count)
        if Value == '26':
            _26.append(count)
            Count.append(count)
        if Value == '27':
            _27.append(count)
            Count.append(count)
        if Value == '28':
            _28.append(count)
            Count.append(count)
        if Value == '29':
            _29.append(count)
            Count.append(count)
        if Value == '30':
            _30.append(count)
            Count.append(count)
        if Value == '31':
            _31.append(count)
            Count.append(count)
        if Value == '32':
            _32.append(count)
            Count.append(count)
        if Value == '33':
            _33.append(count)
            Count.append(count)
        if Value == '34':
            _34.append(count)
            Count.append(count)
        if Value == '35':
            _35.append(count)
            Count.append(count)
        if Value == '36':
            _36.append(count)
            Count.append(count)
        if Value == '37':
            _37.append(count)
            Count.append(count)
        if Value == '38':
            _38.append(count)
            Count.append(count)
        if Value == '39':
            _39.append(count)
            Count.append(count)
        if Value == '40':
            _40.append(count)
            Count.append(count)
        if Value == '41':
            _41.append(count)
            Count.append(count)
        if Value == '42':
            _42.append(count)
            Count.append(count)
        if Value == '43':
            _43.append(count)
            Count.append(count)
        if Value == '44':
            _44.append(count)
            Count.append(count)
        if Value == '45':
            _45.append(count)
            Count.append(count)
        if Value == '46':
            _46.append(count)
            Count.append(count)
        if Value == '47':
            _47.append(count)
            Count.append(count)
        if Value == '48':
            _48.append(count)
            Count.append(count)
        if Value == '49':
            _49.append(count)
            Count.append(count)
        if Value == '50':
            _50.append(count)
            Count.append(count)
        if Value == '51':
            _51.append(count)
            Count.append(count)
        if Value == '52':
            _52.append(count)
            Count.append(count)
        if Value == '53':
            _53.append(count)
            Count.append(count)
        if Value == '54':
            _54.append(count)
            Count.append(count)
        if Value == '55':
            _55.append(count)
            Count.append(count)
        if Value == '56':
            _56.append(count)
            Count.append(count)
        if Value == '57':
            _57.append(count)
            Count.append(count)
        if Value == '58':
            _58.append(count)
            Count.append(count)
        if Value == '59':
            _59.append(count)
            Count.append(count)
        if Value == '60':
            _60.append(count)
            Count.append(count)
        if Value == '61':
            _61.append(count)
            Count.append(count)
        if Value == '62':
            _62.append(count)
            Count.append(count)
        if Value == '63':
            _63.append(count)
            Count.append(count)
        if Value == '64':
            _64.append(count)
            Count.append(count)
        if Value == '65':
            _65.append(count)
            Count.append(count)
        if Value == '66':
            _66.append(count)
            Count.append(count)
        if Value == '67':
            _67.append(count)
            Count.append(count)
        if Value == '68':
            _68.append(count)
            Count.append(count)
        if Value == '69':
            _69.append(count)
            Count.append(count)
        if Value == '70':
            _70.append(count)
            Count.append(count)
        if Value == '71':
            _71.append(count)
            Count.append(count)
        if Value == '72':
            _72.append(count)
            Count.append(count)
        if Value == '73':
            _73.append(count)
            Count.append(count)
        if Value == '74':
            _74.append(count)
            Count.append(count)
        if Value == '75':
            _75.append(count)
            Count.append(count)
        if Value == '76':
            _76.append(count)
            Count.append(count)
        if Value == '77':
            _77.append(count)
            Count.append(count)
        if Value == '78':
            _78.append(count)
            Count.append(count)
        if Value == '79':
            _79.append(count)
            Count.append(count)
        if Value == '80':
            _80.append(count)
            Count.append(count)
        if Value == '81':
            _81.append(count)
            Count.append(count)
        if Value == '82':
            _82.append(count)
            Count.append(count)
        if Value == '83':
            _83.append(count)
            Count.append(count)
        if Value == '84':
            _84.append(count)
            Count.append(count)
        if Value == '85':
            _85.append(count)
            Count.append(count)
        if Value == '86':
            _86.append(count)
            Count.append(count)
        if Value == '87':
            _87.append(count)
            Count.append(count)
        if Value == '88':
            _88.append(count)
            Count.append(count)
        if Value == '89':
            _89.append(count)
            Count.append(count)
        if Value == '90':
            _90.append(count)
            Count.append(count)
        if Value == '91':
            _91.append(count)
            Count.append(count)
        if Value == '92':
            _92.append(count)
            Count.append(count)
        if Value == '93':
            _93.append(count)
            Count.append(count)
        if Value == '94':
            _94.append(count)
            Count.append(count)
        if Value == '95':
            _95.append(count)
            Count.append(count)
        if Value == '96':
            _96.append(count)
            Count.append(count)
        if Value == '97':
            _97.append(count)
            Count.append(count)
        if Value == '98':
            _98.append(count)
            Count.append(count)
        if Value == '99':
            _99.append(count)
            Count.append(count)
        if Value == '100':
            _100.append(count)
            Count.append(count)
        if Value == '101':
            _101.append(count)
            Count.append(count)
        if Value == '102':
            _102.append(count)
            Count.append(count)
        if Value == '103':
            _103.append(count)
            Count.append(count)
        if Value == '104':
            _104.append(count)
            Count.append(count)
        if Value == '105':
            _105.append(count)
            Count.append(count)
        if Value == '106':
            _106.append(count)
            Count.append(count)
        if Value == '107':
            _107.append(count)
            Count.append(count)
        if Value == '108':
            _108.append(count)
            Count.append(count)
        if Value == '109':
            _109.append(count)
            Count.append(count)
        if Value == '110':
            _110.append(count)
            Count.append(count)
        if Value == '111':
            _111.append(count)
            Count.append(count)
        if Value == '112':
            _112.append(count)
            Count.append(count)
        if Value == '113':
            _113.append(count)
            Count.append(count)
        if Value == '114':
            _114.append(count)
            Count.append(count)
        if Value == '115':
            _115.append(count)
            Count.append(count)
        if Value == '116':
            _116.append(count)
            Count.append(count)
        if Value == '117':
            _117.append(count)
            Count.append(count)
        if Value == '118':
            _118.append(count)
            Count.append(count)
        if Value == '119':
            _119.append(count)
            Count.append(count)
        if Value == '120':
            _120.append(count)
            Count.append(count)
        if Value == '121':
            _121.append(count)
            Count.append(count)
        if Value == '122':
            _122.append(count)
            Count.append(count)
        if Value == '123':
            _123.append(count)
            Count.append(count)
        if Value == '124':
            _124.append(count)
            Count.append(count)
        if Value == '125':
            _125.append(count)
            Count.append(count)
        if Value == '126':
            _126.append(count)
            Count.append(count)
        if Value == '127':
            _127.append(count)
            Count.append(count)
        if Value == '128':
            _128.append(count)
            Count.append(count)
        if Value == '129':
            _129.append(count)
            Count.append(count)
        if Value == '130':
            _130.append(count)
            Count.append(count)
        if Value == '131':
            _131.append(count)
            Count.append(count)
        if Value == '132':
            _132.append(count)
            Count.append(count)
        if Value == '133':
            _133.append(count)
            Count.append(count)
        if Value == '134':
            _134.append(count)
            Count.append(count)
        if Value == '135':
            _135.append(count)
            Count.append(count)
        if Value == '136':
            _136.append(count)
            Count.append(count)
        if Value == '137':
            _137.append(count)
            Count.append(count)
        if Value == '138':
            _138.append(count)
            Count.append(count)
        if Value == '139':
            _139.append(count)
            Count.append(count)
        if Value == '140':
            _140.append(count)
            Count.append(count)
        if Value == '141':
            _141.append(count)
            Count.append(count)
        if Value == '142':
            _142.append(count)
            Count.append(count)
        if Value == '143':
            _143.append(count)
            Count.append(count)
        if Value == '144':
            _144.append(count)
            Count.append(count)
        if Value == '145':
            _145.append(count)
            Count.append(count)
        if Value == '146':
            _146.append(count)
            Count.append(count)
        if Value == '147':
            _147.append(count)
            Count.append(count)
        if Value == '148':
            _148.append(count)
            Count.append(count)
        if Value == '149':
            _149.append(count)
            Count.append(count)
        if Value == '150':
            _150.append(count)
            Count.append(count)
        if Value == '151':
            _151.append(count)
            Count.append(count)
        if Value == '152':
            _152.append(count)
            Count.append(count)
        if Value == '153':
            _153.append(count)
            Count.append(count)
        if Value == '154':
            _154.append(count)
            Count.append(count)
        if Value == '155':
            _155.append(count)
            Count.append(count)
        if Value == '156':
            _156.append(count)
            Count.append(count)
        if Value == '157':
            _157.append(count)
            Count.append(count)
        if Value == '158':
            _158.append(count)
            Count.append(count)
        if Value == '159':
            _159.append(count)
            Count.append(count)
        if Value == '160':
            _160.append(count)
            Count.append(count)
        if Value == '161':
            _161.append(count)
            Count.append(count)
        if Value == '162':
            _162.append(count)
            Count.append(count)
        if Value == '163':
            _163.append(count)
            Count.append(count)
        if Value == '164':
            _164.append(count)
            Count.append(count)
        if Value == '165':
            _165.append(count)
            Count.append(count)
        if Value == '166':
            _166.append(count)
            Count.append(count)
        if Value == '167':
            _167.append(count)
            Count.append(count)
        if Value == '168':
            _168.append(count)
            Count.append(count)
        if Value == '169':
            _169.append(count)
            Count.append(count)
        if Value == '170':
            _170.append(count)
            Count.append(count)
        if Value == '171':
            _171.append(count)
            Count.append(count)
        if Value == '172':
            _172.append(count)
            Count.append(count)
        if Value == '173':
            _173.append(count)
            Count.append(count)
        if Value == '174':
            _174.append(count)
            Count.append(count)
        if Value == '175':
            _175.append(count)
            Count.append(count)
        if Value == '176':
            _176.append(count)
            Count.append(count)
        if Value == '177':
            _177.append(count)
            Count.append(count)
        if Value == '178':
            _178.append(count)
            Count.append(count)
        if Value == '179':
            _179.append(count)
            Count.append(count)
        if Value == '180':
            _180.append(count)
            Count.append(count)
        if Value == '181':
            _181.append(count)
            Count.append(count)
        if Value == '182':
            _182.append(count)
            Count.append(count)
        if Value == '183':
            _183.append(count)
            Count.append(count)
        if Value == '184':
            _184.append(count)
            Count.append(count)
        if Value == '185':
            _185.append(count)
            Count.append(count)
        if Value == '186':
            _186.append(count)
            Count.append(count)
        if Value == '187':
            _187.append(count)
            Count.append(count)
        if Value == '188':
            _188.append(count)
            Count.append(count)
        if Value == '189':
            _189.append(count)
            Count.append(count)
        if Value == '190':
            _190.append(count)
            Count.append(count)
        if Value == '191':
            _191.append(count)
            Count.append(count)
        if Value == '192':
            _192.append(count)
            Count.append(count)
        if Value == '193':
            _193.append(count)
            Count.append(count)
        if Value == '194':
            _194.append(count)
            Count.append(count)
        if Value == '195':
            _195.append(count)
            Count.append(count)
        if Value == '196':
            _196.append(count)
            Count.append(count)
        if Value == '197':
            _197.append(count)
            Count.append(count)
        if Value == '198':
            _198.append(count)
            Count.append(count)
        if Value == '199':
            _199.append(count)
            Count.append(count)
        if Value == '200':
            _200.append(count)
            Count.append(count)
        if Value == '201':
            _201.append(count)
            Count.append(count)
        if Value == '202':
            _202.append(count)
            Count.append(count)
        if Value == '203':
            _203.append(count)
            Count.append(count)
        if Value == '204':
            _204.append(count)
            Count.append(count)
        if Value == '205':
            _205.append(count)
            Count.append(count)
        if Value == '206':
            _206.append(count)
            Count.append(count)
        if Value == '207':
            _207.append(count)
            Count.append(count)
        if Value == '208':
            _208.append(count)
            Count.append(count)
        if Value == '209':
            _209.append(count)
            Count.append(count)
        if Value == '210':
            _210.append(count)
            Count.append(count)
        if Value == '211':
            _211.append(count)
            Count.append(count)
        if Value == '212':
            _212.append(count)
            Count.append(count)
        if Value == '213':
            _213.append(count)
            Count.append(count)
        if Value == '214':
            _214.append(count)
            Count.append(count)
        if Value == '215':
            _215.append(count)
            Count.append(count)
        if Value == '216':
            _216.append(count)
            Count.append(count)
        if Value == '217':
            _217.append(count)
            Count.append(count)
        if Value == '218':
            _218.append(count)
            Count.append(count)
        if Value == '219':
            _219.append(count)
            Count.append(count)
        if Value == '220':
            _220.append(count)
            Count.append(count)
        if Value == '221':
            _221.append(count)
            Count.append(count)
        if Value == '222':
            _222.append(count)
            Count.append(count)
        if Value == '223':
            _223.append(count)
            Count.append(count)
        if Value == '224':
            _224.append(count)
            Count.append(count)
        if Value == '225':
            _225.append(count)
            Count.append(count)
        if Value == '226':
            _226.append(count)
            Count.append(count)
        if Value == '227':
            _227.append(count)
            Count.append(count)
        if Value == '228':
            _228.append(count)
            Count.append(count)
        if Value == '229':
            _229.append(count)
            Count.append(count)
        if Value == '230':
            _230.append(count)
            Count.append(count)
        if Value == '231':
            _231.append(count)
            Count.append(count)
        if Value == '232':
            _232.append(count)
            Count.append(count)
        if Value == '233':
            _233.append(count)
            Count.append(count)
        if Value == '234':
            _234.append(count)
            Count.append(count)
        if Value == '235':
            _235.append(count)
            Count.append(count)
        if Value == '236':
            _236.append(count)
            Count.append(count)
        if Value == '237':
            _237.append(count)
            Count.append(count)
        if Value == '238':
            _238.append(count)
            Count.append(count)
        if Value == '239':
            _239.append(count)
            Count.append(count)
        if Value == '240':
            _240.append(count)
            Count.append(count)
        if Value == '241':
            _241.append(count)
            Count.append(count)
        if Value == '242':
            _242.append(count)
            Count.append(count)
        if Value == '243':
            _243.append(count)
            Count.append(count)
        if Value == '244':
            _244.append(count)
            Count.append(count)
        if Value == '245':
            _245.append(count)
            Count.append(count)
        if Value == '246':
            _246.append(count)
            Count.append(count)
        if Value == '247':
            _247.append(count)
            Count.append(count)
        if Value == '248':
            _248.append(count)
            Count.append(count)
        if Value == '249':
            _249.append(count)
            Count.append(count)
        if Value == '250':
            _250.append(count)
            Count.append(count)
        if Value == '251':
            _251.append(count)
            Count.append(count)
        if Value == '252':
            _252.append(count)
            Count.append(count)
        if Value == '253':
            _253.append(count)
            Count.append(count)
        if Value == '254':
            _254.append(count)
            Count.append(count)
        if Value == '255':
            _255.append(count)
            Count.append(count)






    #SUM THE NLCD GRID COUNTS
    _0sum = numpy.sum(_0)
    _1sum = numpy.sum(_1)
    _2sum = numpy.sum(_2)
    _3sum = numpy.sum(_3)
    _4sum = numpy.sum(_4)
    _5sum = numpy.sum(_5)
    _6sum = numpy.sum(_6)
    _7sum = numpy.sum(_7)
    _8sum = numpy.sum(_8)
    _9sum = numpy.sum(_9)
    _10sum = numpy.sum(_10)
    _11sum = numpy.sum(_11)
    _12sum = numpy.sum(_12)
    _13sum = numpy.sum(_13)
    _14sum = numpy.sum(_14)
    _15sum = numpy.sum(_15)
    _16sum = numpy.sum(_16)
    _17sum = numpy.sum(_17)
    _18sum = numpy.sum(_18)
    _19sum = numpy.sum(_19)
    _20sum = numpy.sum(_20)
    _21sum = numpy.sum(_21)
    _22sum = numpy.sum(_22)
    _23sum = numpy.sum(_23)
    _24sum = numpy.sum(_24)
    _25sum = numpy.sum(_25)
    _26sum = numpy.sum(_26)
    _27sum = numpy.sum(_27)
    _28sum = numpy.sum(_28)
    _29sum = numpy.sum(_29)
    _30sum = numpy.sum(_30)
    _31sum = numpy.sum(_31)
    _32sum = numpy.sum(_32)
    _33sum = numpy.sum(_33)
    _34sum = numpy.sum(_34)
    _35sum = numpy.sum(_35)
    _36sum = numpy.sum(_36)
    _37sum = numpy.sum(_37)
    _38sum = numpy.sum(_38)
    _39sum = numpy.sum(_39)
    _40sum = numpy.sum(_40)
    _41sum = numpy.sum(_41)
    _42sum = numpy.sum(_42)
    _43sum = numpy.sum(_43)
    _44sum = numpy.sum(_44)
    _45sum = numpy.sum(_45)
    _46sum = numpy.sum(_46)
    _47sum = numpy.sum(_47)
    _48sum = numpy.sum(_48)
    _49sum = numpy.sum(_49)
    _50sum = numpy.sum(_50)
    _51sum = numpy.sum(_51)
    _52sum = numpy.sum(_52)
    _53sum = numpy.sum(_53)
    _54sum = numpy.sum(_54)
    _55sum = numpy.sum(_55)
    _56sum = numpy.sum(_56)
    _57sum = numpy.sum(_57)
    _58sum = numpy.sum(_58)
    _59sum = numpy.sum(_59)
    _60sum = numpy.sum(_60)
    _61sum = numpy.sum(_61)
    _62sum = numpy.sum(_62)
    _63sum = numpy.sum(_63)
    _64sum = numpy.sum(_64)
    _65sum = numpy.sum(_65)
    _66sum = numpy.sum(_66)
    _67sum = numpy.sum(_67)
    _68sum = numpy.sum(_68)
    _69sum = numpy.sum(_69)
    _70sum = numpy.sum(_70)
    _71sum = numpy.sum(_71)
    _72sum = numpy.sum(_72)
    _73sum = numpy.sum(_73)
    _74sum = numpy.sum(_74)
    _75sum = numpy.sum(_75)
    _76sum = numpy.sum(_76)
    _77sum = numpy.sum(_77)
    _78sum = numpy.sum(_78)
    _79sum = numpy.sum(_79)
    _80sum = numpy.sum(_80)
    _81sum = numpy.sum(_81)
    _82sum = numpy.sum(_82)
    _83sum = numpy.sum(_83)
    _84sum = numpy.sum(_84)
    _85sum = numpy.sum(_85)
    _86sum = numpy.sum(_86)
    _87sum = numpy.sum(_87)
    _88sum = numpy.sum(_88)
    _89sum = numpy.sum(_89)
    _90sum = numpy.sum(_90)
    _91sum = numpy.sum(_91)
    _92sum = numpy.sum(_92)
    _93sum = numpy.sum(_93)
    _94sum = numpy.sum(_94)
    _95sum = numpy.sum(_95)
    _96sum = numpy.sum(_96)
    _97sum = numpy.sum(_97)
    _98sum = numpy.sum(_98)
    _99sum = numpy.sum(_99)
    _100sum = numpy.sum(_100)
    _101sum = numpy.sum(_101)
    _102sum = numpy.sum(_102)
    _103sum = numpy.sum(_103)
    _104sum = numpy.sum(_104)
    _105sum = numpy.sum(_105)
    _106sum = numpy.sum(_106)
    _107sum = numpy.sum(_107)
    _108sum = numpy.sum(_108)
    _109sum = numpy.sum(_109)
    _110sum = numpy.sum(_110)
    _111sum = numpy.sum(_111)
    _112sum = numpy.sum(_112)
    _113sum = numpy.sum(_113)
    _114sum = numpy.sum(_114)
    _115sum = numpy.sum(_115)
    _116sum = numpy.sum(_116)
    _117sum = numpy.sum(_117)
    _118sum = numpy.sum(_118)
    _119sum = numpy.sum(_119)
    _120sum = numpy.sum(_120)
    _121sum = numpy.sum(_121)
    _122sum = numpy.sum(_122)
    _123sum = numpy.sum(_123)
    _124sum = numpy.sum(_124)
    _125sum = numpy.sum(_125)
    _126sum = numpy.sum(_126)
    _127sum = numpy.sum(_127)
    _128sum = numpy.sum(_128)
    _129sum = numpy.sum(_129)
    _130sum = numpy.sum(_130)
    _131sum = numpy.sum(_131)
    _132sum = numpy.sum(_132)
    _133sum = numpy.sum(_133)
    _134sum = numpy.sum(_134)
    _135sum = numpy.sum(_135)
    _136sum = numpy.sum(_136)
    _137sum = numpy.sum(_137)
    _138sum = numpy.sum(_138)
    _139sum = numpy.sum(_139)
    _140sum = numpy.sum(_140)
    _141sum = numpy.sum(_141)
    _142sum = numpy.sum(_142)
    _143sum = numpy.sum(_143)
    _144sum = numpy.sum(_144)
    _145sum = numpy.sum(_145)
    _146sum = numpy.sum(_146)
    _147sum = numpy.sum(_147)
    _148sum = numpy.sum(_148)
    _149sum = numpy.sum(_149)
    _150sum = numpy.sum(_150)
    _151sum = numpy.sum(_151)
    _152sum = numpy.sum(_152)
    _153sum = numpy.sum(_153)
    _154sum = numpy.sum(_154)
    _155sum = numpy.sum(_155)
    _156sum = numpy.sum(_156)
    _157sum = numpy.sum(_157)
    _158sum = numpy.sum(_158)
    _159sum = numpy.sum(_159)
    _160sum = numpy.sum(_160)
    _161sum = numpy.sum(_161)
    _162sum = numpy.sum(_162)
    _163sum = numpy.sum(_163)
    _164sum = numpy.sum(_164)
    _165sum = numpy.sum(_165)
    _166sum = numpy.sum(_166)
    _167sum = numpy.sum(_167)
    _168sum = numpy.sum(_168)
    _169sum = numpy.sum(_169)
    _170sum = numpy.sum(_170)
    _171sum = numpy.sum(_171)
    _172sum = numpy.sum(_172)
    _173sum = numpy.sum(_173)
    _174sum = numpy.sum(_174)
    _175sum = numpy.sum(_175)
    _176sum = numpy.sum(_176)
    _177sum = numpy.sum(_177)
    _178sum = numpy.sum(_178)
    _179sum = numpy.sum(_179)
    _180sum = numpy.sum(_180)
    _181sum = numpy.sum(_181)
    _182sum = numpy.sum(_182)
    _183sum = numpy.sum(_183)
    _184sum = numpy.sum(_184)
    _185sum = numpy.sum(_185)
    _186sum = numpy.sum(_186)
    _187sum = numpy.sum(_187)
    _188sum = numpy.sum(_188)
    _189sum = numpy.sum(_189)
    _190sum = numpy.sum(_190)
    _191sum = numpy.sum(_191)
    _192sum = numpy.sum(_192)
    _193sum = numpy.sum(_193)
    _194sum = numpy.sum(_194)
    _195sum = numpy.sum(_195)
    _196sum = numpy.sum(_196)
    _197sum = numpy.sum(_197)
    _198sum = numpy.sum(_198)
    _199sum = numpy.sum(_199)
    _200sum = numpy.sum(_200)
    _201sum = numpy.sum(_201)
    _202sum = numpy.sum(_202)
    _203sum = numpy.sum(_203)
    _204sum = numpy.sum(_204)
    _205sum = numpy.sum(_205)
    _206sum = numpy.sum(_206)
    _207sum = numpy.sum(_207)
    _208sum = numpy.sum(_208)
    _209sum = numpy.sum(_209)
    _210sum = numpy.sum(_210)
    _211sum = numpy.sum(_211)
    _212sum = numpy.sum(_212)
    _213sum = numpy.sum(_213)
    _214sum = numpy.sum(_214)
    _215sum = numpy.sum(_215)
    _216sum = numpy.sum(_216)
    _217sum = numpy.sum(_217)
    _218sum = numpy.sum(_218)
    _219sum = numpy.sum(_219)
    _220sum = numpy.sum(_220)
    _221sum = numpy.sum(_221)
    _222sum = numpy.sum(_222)
    _223sum = numpy.sum(_223)
    _224sum = numpy.sum(_224)
    _225sum = numpy.sum(_225)
    _226sum = numpy.sum(_226)
    _227sum = numpy.sum(_227)
    _228sum = numpy.sum(_228)
    _229sum = numpy.sum(_229)
    _230sum = numpy.sum(_230)
    _231sum = numpy.sum(_231)
    _232sum = numpy.sum(_232)
    _233sum = numpy.sum(_233)
    _234sum = numpy.sum(_234)
    _235sum = numpy.sum(_235)
    _236sum = numpy.sum(_236)
    _237sum = numpy.sum(_237)
    _238sum = numpy.sum(_238)
    _239sum = numpy.sum(_239)
    _240sum = numpy.sum(_240)
    _241sum = numpy.sum(_241)
    _242sum = numpy.sum(_242)
    _243sum = numpy.sum(_243)
    _244sum = numpy.sum(_244)
    _245sum = numpy.sum(_245)
    _246sum = numpy.sum(_246)
    _247sum = numpy.sum(_247)
    _248sum = numpy.sum(_248)
    _249sum = numpy.sum(_249)
    _250sum = numpy.sum(_250)
    _251sum = numpy.sum(_251)
    _252sum = numpy.sum(_252)
    _253sum = numpy.sum(_253)
    _254sum = numpy.sum(_254)
    _255sum = numpy.sum(_255)






    
    Count_sum = numpy.sum(Count)

    #CALCULATE PERCENT OF EACH NLCD
    _0percent = float(_0sum/Count_sum*100)
    _1percent = float(_1sum/Count_sum*100)
    _2percent = float(_2sum/Count_sum*100)
    _3percent = float(_3sum/Count_sum*100)
    _4percent = float(_4sum/Count_sum*100)
    _5percent = float(_5sum/Count_sum*100)
    _6percent = float(_6sum/Count_sum*100)
    _7percent = float(_7sum/Count_sum*100)
    _8percent = float(_8sum/Count_sum*100)
    _9percent = float(_9sum/Count_sum*100)
    _10percent = float(_10sum/Count_sum*100)
    _11percent = float(_11sum/Count_sum*100)
    _12percent = float(_12sum/Count_sum*100)
    _13percent = float(_13sum/Count_sum*100)
    _14percent = float(_14sum/Count_sum*100)
    _15percent = float(_15sum/Count_sum*100)
    _16percent = float(_16sum/Count_sum*100)
    _17percent = float(_17sum/Count_sum*100)
    _18percent = float(_18sum/Count_sum*100)
    _19percent = float(_19sum/Count_sum*100)
    _20percent = float(_20sum/Count_sum*100)
    _21percent = float(_21sum/Count_sum*100)
    _22percent = float(_22sum/Count_sum*100)
    _23percent = float(_23sum/Count_sum*100)
    _24percent = float(_24sum/Count_sum*100)
    _25percent = float(_25sum/Count_sum*100)
    _26percent = float(_26sum/Count_sum*100)
    _27percent = float(_27sum/Count_sum*100)
    _28percent = float(_28sum/Count_sum*100)
    _29percent = float(_29sum/Count_sum*100)
    _30percent = float(_30sum/Count_sum*100)
    _31percent = float(_31sum/Count_sum*100)
    _32percent = float(_32sum/Count_sum*100)
    _33percent = float(_33sum/Count_sum*100)
    _34percent = float(_34sum/Count_sum*100)
    _35percent = float(_35sum/Count_sum*100)
    _36percent = float(_36sum/Count_sum*100)
    _37percent = float(_37sum/Count_sum*100)
    _38percent = float(_38sum/Count_sum*100)
    _39percent = float(_39sum/Count_sum*100)
    _40percent = float(_40sum/Count_sum*100)
    _41percent = float(_41sum/Count_sum*100)
    _42percent = float(_42sum/Count_sum*100)
    _43percent = float(_43sum/Count_sum*100)
    _44percent = float(_44sum/Count_sum*100)
    _45percent = float(_45sum/Count_sum*100)
    _46percent = float(_46sum/Count_sum*100)
    _47percent = float(_47sum/Count_sum*100)
    _48percent = float(_48sum/Count_sum*100)
    _49percent = float(_49sum/Count_sum*100)
    _50percent = float(_50sum/Count_sum*100)
    _51percent = float(_51sum/Count_sum*100)
    _52percent = float(_52sum/Count_sum*100)
    _53percent = float(_53sum/Count_sum*100)
    _54percent = float(_54sum/Count_sum*100)
    _55percent = float(_55sum/Count_sum*100)
    _56percent = float(_56sum/Count_sum*100)
    _57percent = float(_57sum/Count_sum*100)
    _58percent = float(_58sum/Count_sum*100)
    _59percent = float(_59sum/Count_sum*100)
    _60percent = float(_60sum/Count_sum*100)
    _61percent = float(_61sum/Count_sum*100)
    _62percent = float(_62sum/Count_sum*100)
    _63percent = float(_63sum/Count_sum*100)
    _64percent = float(_64sum/Count_sum*100)
    _65percent = float(_65sum/Count_sum*100)
    _66percent = float(_66sum/Count_sum*100)
    _67percent = float(_67sum/Count_sum*100)
    _68percent = float(_68sum/Count_sum*100)
    _69percent = float(_69sum/Count_sum*100)
    _70percent = float(_70sum/Count_sum*100)
    _71percent = float(_71sum/Count_sum*100)
    _72percent = float(_72sum/Count_sum*100)
    _73percent = float(_73sum/Count_sum*100)
    _74percent = float(_74sum/Count_sum*100)
    _75percent = float(_75sum/Count_sum*100)
    _76percent = float(_76sum/Count_sum*100)
    _77percent = float(_77sum/Count_sum*100)
    _78percent = float(_78sum/Count_sum*100)
    _79percent = float(_79sum/Count_sum*100)
    _80percent = float(_80sum/Count_sum*100)
    _81percent = float(_81sum/Count_sum*100)
    _82percent = float(_82sum/Count_sum*100)
    _83percent = float(_83sum/Count_sum*100)
    _84percent = float(_84sum/Count_sum*100)
    _85percent = float(_85sum/Count_sum*100)
    _86percent = float(_86sum/Count_sum*100)
    _87percent = float(_87sum/Count_sum*100)
    _88percent = float(_88sum/Count_sum*100)
    _89percent = float(_89sum/Count_sum*100)
    _90percent = float(_90sum/Count_sum*100)
    _91percent = float(_91sum/Count_sum*100)
    _92percent = float(_92sum/Count_sum*100)
    _93percent = float(_93sum/Count_sum*100)
    _94percent = float(_94sum/Count_sum*100)
    _95percent = float(_95sum/Count_sum*100)
    _96percent = float(_96sum/Count_sum*100)
    _97percent = float(_97sum/Count_sum*100)
    _98percent = float(_98sum/Count_sum*100)
    _99percent = float(_99sum/Count_sum*100)
    _100percent = float(_100sum/Count_sum*100)
    _101percent = float(_101sum/Count_sum*100)
    _102percent = float(_102sum/Count_sum*100)
    _103percent = float(_103sum/Count_sum*100)
    _104percent = float(_104sum/Count_sum*100)
    _105percent = float(_105sum/Count_sum*100)
    _106percent = float(_106sum/Count_sum*100)
    _107percent = float(_107sum/Count_sum*100)
    _108percent = float(_108sum/Count_sum*100)
    _109percent = float(_109sum/Count_sum*100)
    _110percent = float(_110sum/Count_sum*100)
    _111percent = float(_111sum/Count_sum*100)
    _112percent = float(_112sum/Count_sum*100)
    _113percent = float(_113sum/Count_sum*100)
    _114percent = float(_114sum/Count_sum*100)
    _115percent = float(_115sum/Count_sum*100)
    _116percent = float(_116sum/Count_sum*100)
    _117percent = float(_117sum/Count_sum*100)
    _118percent = float(_118sum/Count_sum*100)
    _119percent = float(_119sum/Count_sum*100)
    _120percent = float(_120sum/Count_sum*100)
    _121percent = float(_121sum/Count_sum*100)
    _122percent = float(_122sum/Count_sum*100)
    _123percent = float(_123sum/Count_sum*100)
    _124percent = float(_124sum/Count_sum*100)
    _125percent = float(_125sum/Count_sum*100)
    _126percent = float(_126sum/Count_sum*100)
    _127percent = float(_127sum/Count_sum*100)
    _128percent = float(_128sum/Count_sum*100)
    _129percent = float(_129sum/Count_sum*100)
    _130percent = float(_130sum/Count_sum*100)
    _131percent = float(_131sum/Count_sum*100)
    _132percent = float(_132sum/Count_sum*100)
    _133percent = float(_133sum/Count_sum*100)
    _134percent = float(_134sum/Count_sum*100)
    _135percent = float(_135sum/Count_sum*100)
    _136percent = float(_136sum/Count_sum*100)
    _137percent = float(_137sum/Count_sum*100)
    _138percent = float(_138sum/Count_sum*100)
    _139percent = float(_139sum/Count_sum*100)
    _140percent = float(_140sum/Count_sum*100)
    _141percent = float(_141sum/Count_sum*100)
    _142percent = float(_142sum/Count_sum*100)
    _143percent = float(_143sum/Count_sum*100)
    _144percent = float(_144sum/Count_sum*100)
    _145percent = float(_145sum/Count_sum*100)
    _146percent = float(_146sum/Count_sum*100)
    _147percent = float(_147sum/Count_sum*100)
    _148percent = float(_148sum/Count_sum*100)
    _149percent = float(_149sum/Count_sum*100)
    _150percent = float(_150sum/Count_sum*100)
    _151percent = float(_151sum/Count_sum*100)
    _152percent = float(_152sum/Count_sum*100)
    _153percent = float(_153sum/Count_sum*100)
    _154percent = float(_154sum/Count_sum*100)
    _155percent = float(_155sum/Count_sum*100)
    _156percent = float(_156sum/Count_sum*100)
    _157percent = float(_157sum/Count_sum*100)
    _158percent = float(_158sum/Count_sum*100)
    _159percent = float(_159sum/Count_sum*100)
    _160percent = float(_160sum/Count_sum*100)
    _161percent = float(_161sum/Count_sum*100)
    _162percent = float(_162sum/Count_sum*100)
    _163percent = float(_163sum/Count_sum*100)
    _164percent = float(_164sum/Count_sum*100)
    _165percent = float(_165sum/Count_sum*100)
    _166percent = float(_166sum/Count_sum*100)
    _167percent = float(_167sum/Count_sum*100)
    _168percent = float(_168sum/Count_sum*100)
    _169percent = float(_169sum/Count_sum*100)
    _170percent = float(_170sum/Count_sum*100)
    _171percent = float(_171sum/Count_sum*100)
    _172percent = float(_172sum/Count_sum*100)
    _173percent = float(_173sum/Count_sum*100)
    _174percent = float(_174sum/Count_sum*100)
    _175percent = float(_175sum/Count_sum*100)
    _176percent = float(_176sum/Count_sum*100)
    _177percent = float(_177sum/Count_sum*100)
    _178percent = float(_178sum/Count_sum*100)
    _179percent = float(_179sum/Count_sum*100)
    _180percent = float(_180sum/Count_sum*100)
    _181percent = float(_181sum/Count_sum*100)
    _182percent = float(_182sum/Count_sum*100)
    _183percent = float(_183sum/Count_sum*100)
    _184percent = float(_184sum/Count_sum*100)
    _185percent = float(_185sum/Count_sum*100)
    _186percent = float(_186sum/Count_sum*100)
    _187percent = float(_187sum/Count_sum*100)
    _188percent = float(_188sum/Count_sum*100)
    _189percent = float(_189sum/Count_sum*100)
    _190percent = float(_190sum/Count_sum*100)
    _191percent = float(_191sum/Count_sum*100)
    _192percent = float(_192sum/Count_sum*100)
    _193percent = float(_193sum/Count_sum*100)
    _194percent = float(_194sum/Count_sum*100)
    _195percent = float(_195sum/Count_sum*100)
    _196percent = float(_196sum/Count_sum*100)
    _197percent = float(_197sum/Count_sum*100)
    _198percent = float(_198sum/Count_sum*100)
    _199percent = float(_199sum/Count_sum*100)
    _200percent = float(_200sum/Count_sum*100)
    _201percent = float(_201sum/Count_sum*100)
    _202percent = float(_202sum/Count_sum*100)
    _203percent = float(_203sum/Count_sum*100)
    _204percent = float(_204sum/Count_sum*100)
    _205percent = float(_205sum/Count_sum*100)
    _206percent = float(_206sum/Count_sum*100)
    _207percent = float(_207sum/Count_sum*100)
    _208percent = float(_208sum/Count_sum*100)
    _209percent = float(_209sum/Count_sum*100)
    _210percent = float(_210sum/Count_sum*100)
    _211percent = float(_211sum/Count_sum*100)
    _212percent = float(_212sum/Count_sum*100)
    _213percent = float(_213sum/Count_sum*100)
    _214percent = float(_214sum/Count_sum*100)
    _215percent = float(_215sum/Count_sum*100)
    _216percent = float(_216sum/Count_sum*100)
    _217percent = float(_217sum/Count_sum*100)
    _218percent = float(_218sum/Count_sum*100)
    _219percent = float(_219sum/Count_sum*100)
    _220percent = float(_220sum/Count_sum*100)
    _221percent = float(_221sum/Count_sum*100)
    _222percent = float(_222sum/Count_sum*100)
    _223percent = float(_223sum/Count_sum*100)
    _224percent = float(_224sum/Count_sum*100)
    _225percent = float(_225sum/Count_sum*100)
    _226percent = float(_226sum/Count_sum*100)
    _227percent = float(_227sum/Count_sum*100)
    _228percent = float(_228sum/Count_sum*100)
    _229percent = float(_229sum/Count_sum*100)
    _230percent = float(_230sum/Count_sum*100)
    _231percent = float(_231sum/Count_sum*100)
    _232percent = float(_232sum/Count_sum*100)
    _233percent = float(_233sum/Count_sum*100)
    _234percent = float(_234sum/Count_sum*100)
    _235percent = float(_235sum/Count_sum*100)
    _236percent = float(_236sum/Count_sum*100)
    _237percent = float(_237sum/Count_sum*100)
    _238percent = float(_238sum/Count_sum*100)
    _239percent = float(_239sum/Count_sum*100)
    _240percent = float(_240sum/Count_sum*100)
    _241percent = float(_241sum/Count_sum*100)
    _242percent = float(_242sum/Count_sum*100)
    _243percent = float(_243sum/Count_sum*100)
    _244percent = float(_244sum/Count_sum*100)
    _245percent = float(_245sum/Count_sum*100)
    _246percent = float(_246sum/Count_sum*100)
    _247percent = float(_247sum/Count_sum*100)
    _248percent = float(_248sum/Count_sum*100)
    _249percent = float(_249sum/Count_sum*100)
    _250percent = float(_250sum/Count_sum*100)
    _251percent = float(_251sum/Count_sum*100)
    _252percent = float(_252sum/Count_sum*100)
    _253percent = float(_253sum/Count_sum*100)
    _254percent = float(_254sum/Count_sum*100)
    _255percent = float(_255sum/Count_sum*100)




    #WRITE THE DATA TO THE RFC SUMMARY CSV FILE
    nlcd_file.write(name + ',' + str(_0percent) + ',' + str(_1percent) + ',' + str(_2percent) + ',' + str(_3percent) + ',' + str(_4percent) + ',' + str(_5percent) + ',' + str(_6percent) + ',' + str(_7percent) + ',' + str(_8percent) + ',' + str(_9percent) + ',' + str(_10percent) + ',' + str(_11percent) + ',' + str(_12percent) + ',' + str(_13percent) + ',' + str(_14percent) + ',' + str(_15percent) + ',' + str(_16percent) + ',' + str(_17percent) + ',' + str(_18percent) + ',' + str(_19percent) + ',' + str(_20percent) + ',' + str(_21percent) + ',' + str(_22percent) + ',' + str(_23percent) + ',' + str(_24percent) + ',' + str(_25percent) + ',' + str(_26percent) + ',' + str(_27percent) + ',' + str(_28percent) + ',' + str(_29percent) + ',' + str(_30percent) + ',' + str(_31percent) + ',' + str(_32percent) + ',' + str(_33percent) + ',' + str(_34percent) + ',' + str(_35percent) + ',' + str(_36percent) + ',' + str(_37percent) + ',' + str(_38percent) + ',' + str(_39percent) + ',' + str(_40percent) + ',' + str(_41percent) + ',' + str(_42percent) + ',' + str(_43percent) + ',' + str(_44percent) + ',' + str(_45percent) + ',' + str(_46percent) + ',' + str(_47percent) + ',' + str(_48percent) + ',' + str(_49percent) + ',' + str(_50percent) + ',' + str(_51percent) + ',' + str(_52percent) + ',' + str(_53percent) + ',' + str(_54percent) + ',' + str(_55percent) + ',' + str(_56percent) + ',' + str(_57percent) + ',' + str(_58percent) + ',' + str(_59percent) + ',' + str(_60percent) + ',' + str(_61percent) + ',' + str(_62percent) + ',' + str(_63percent) + ',' + str(_64percent) + ',' + str(_65percent) + ',' + str(_66percent) + ',' + str(_67percent) + ',' + str(_68percent) + ',' + str(_69percent) + ',' + str(_70percent) + ',' + str(_71percent) + ',' + str(_72percent) + ',' + str(_73percent) + ',' + str(_74percent) + ',' + str(_75percent) + ',' + str(_76percent) + ',' + str(_77percent) + ',' + str(_78percent) + ',' + str(_79percent) + ',' + str(_80percent) + ',' + str(_81percent) + ',' + str(_82percent) + ',' + str(_83percent) + ',' + str(_84percent) + ',' + str(_85percent) + ',' + str(_86percent) + ',' + str(_87percent) + ',' + str(_88percent) + ',' + str(_89percent) + ',' + str(_90percent) + ',' + str(_91percent) + ',' + str(_92percent) + ',' + str(_93percent) + ',' + str(_94percent) + ',' + str(_95percent) + ',' + str(_96percent) + ',' + str(_97percent) + ',' + str(_98percent) + ',' + str(_99percent) + ',' + str(_100percent) + ',' + str(_101percent) + ',' + str(_102percent) + ',' + str(_103percent) + ',' + str(_104percent) + ',' + str(_105percent) + ',' + str(_106percent) + ',' + str(_107percent) + ',' + str(_108percent) + ',' + str(_109percent) + ',' + str(_110percent) + ',' + str(_111percent) + ',' + str(_112percent) + ',' + str(_113percent) + ',' + str(_114percent) + ',' + str(_115percent) + ',' + str(_116percent) + ',' + str(_117percent) + ',' + str(_118percent) + ',' + str(_119percent) + ',' + str(_120percent) + ',' + str(_121percent) + ',' + str(_122percent) + ',' + str(_123percent) + ',' + str(_124percent) + ',' + str(_125percent) + ',' + str(_126percent) + ',' + str(_127percent) + ',' + str(_128percent) + ',' + str(_129percent) + ',' + str(_130percent) + ',' + str(_131percent) + ',' + str(_132percent) + ',' + str(_133percent) + ',' + str(_134percent) + ',' + str(_135percent) + ',' + str(_136percent) + ',' + str(_137percent) + ',' + str(_138percent) + ',' + str(_139percent) + ',' + str(_140percent) + ',' + str(_141percent) + ',' + str(_142percent) + ',' + str(_143percent) + ',' + str(_144percent) + ',' + str(_145percent) + ',' + str(_146percent) + ',' + str(_147percent) + ',' + str(_148percent) + ',' + str(_149percent) + ',' + str(_150percent) + ',' + str(_151percent) + ',' + str(_152percent) + ',' + str(_153percent) + ',' + str(_154percent) + ',' + str(_155percent) + ',' + str(_156percent) + ',' + str(_157percent) + ',' + str(_158percent) + ',' + str(_159percent) + ',' + str(_160percent) + ',' + str(_161percent) + ',' + str(_162percent) + ',' + str(_163percent) + ',' + str(_164percent) + ',' + str(_165percent) + ',' + str(_166percent) + ',' + str(_167percent) + ',' + str(_168percent) + ',' + str(_169percent) + ',' + str(_170percent) + ',' + str(_171percent) + ',' + str(_172percent) + ',' + str(_173percent) + ',' + str(_174percent) + ',' + str(_175percent) + ',' + str(_176percent) + ',' + str(_177percent) + ',' + str(_178percent) + ',' + str(_179percent) + ',' + str(_180percent) + ',' + str(_181percent) + ',' + str(_182percent) + ',' + str(_183percent) + ',' + str(_184percent) + ',' + str(_185percent) + ',' + str(_186percent) + ',' + str(_187percent) + ',' + str(_188percent) + ',' + str(_189percent) + ',' + str(_190percent) + ',' + str(_191percent) + ',' + str(_192percent) + ',' + str(_193percent) + ',' + str(_194percent) + ',' + str(_195percent) + ',' + str(_196percent) + ',' + str(_197percent) + ',' + str(_198percent) + ',' + str(_199percent) + ',' + str(_200percent) + ',' + str(_201percent) + ',' + str(_202percent) + ',' + str(_203percent) + ',' + str(_204percent) + ',' + str(_205percent) + ',' + str(_206percent) + ',' + str(_207percent) + ',' + str(_208percent) + ',' + str(_209percent) + ',' + str(_210percent) + ',' + str(_211percent) + ',' + str(_212percent) + ',' + str(_213percent) + ',' + str(_214percent) + ',' + str(_215percent) + ',' + str(_216percent) + ',' + str(_217percent) + ',' + str(_218percent) + ',' + str(_219percent) + ',' + str(_220percent) + ',' + str(_221percent) + ',' + str(_222percent) + ',' + str(_223percent) + ',' + str(_224percent) + ',' + str(_225percent) + ',' + str(_226percent) + ',' + str(_227percent) + ',' + str(_228percent) + ',' + str(_229percent) + ',' + str(_230percent) + ',' + str(_231percent) + ',' + str(_232percent) + ',' + str(_233percent) + ',' + str(_234percent) + ',' + str(_235percent) + ',' + str(_236percent) + ',' + str(_237percent) + ',' + str(_238percent) + ',' + str(_239percent) + ',' + str(_240percent) + ',' + str(_241percent) + ',' + str(_242percent) + ',' + str(_243percent) + ',' + str(_244percent) + ',' + str(_245percent) + ',' + str(_246percent) + ',' + str(_247percent) + ',' + str(_248percent) + ',' + str(_249percent) + ',' + str(_250percent) + ',' + str(_251percent) + ',' + str(_252percent) + ',' + str(_253percent) + ',' + str(_254percent) + ',' + str(_255percent) + ',' + '\n')

    csv_file.close()  
nlcd_file.close()

#csv_file.close()
os.remove(output_folderPath + 'temp.csv')

print 'Script Complete'
print 'nlcd Summary File is', nlcd_file
raw_input('Press Enter to continue...')
