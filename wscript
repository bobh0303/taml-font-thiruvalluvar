#!/usr/bin/python
# this is a smith configuration file

# thiruvalluvar

# command line options
opts = preprocess_args(
    {'opt' : '-l'}, # build fonts from legacy for inclusion into final fonts
    {'opt' : '-p'}, # do not run psfix on the final fonts
    {'opt' : '-s'}  # only build a single font
    )

import os2

# set the default output folders
out='results'

# locations of files needed for some tasks
DOCDIR = ['documentation', 'web']
STANDARDS='tests/reference'

# set meta-information
script='taml'
APPNAME='nlci-' + script

DESC_SHORT='Tamil Unicode font with OT and Graphite support'
DESC_NAME='NLCI-' + script
DEBPKG='fonts-nlci-' + script
getufoinfo('source/ThiruValluvar-Regular.ufo')

# set test parameters
TESTSTRING=u'\u0c15'
#ftmlTest('tools/FTMLcreateList.xsl')
ftmlTest('tools/ftml-padauk.xsl')
testCommand('sile', cmd='${SILE} -o "${TGT}" "${SRC[0].abspath()}" -f "${SRC[1]}"', extracmds=['sile'], shapers=0, supports=['.sil'], ext='.pdf')

# set fonts to build
faces = ('ThiruValluvar', 'Auvaiyar', 'Vaigai')
facesLegacy = ('THIR', 'AUVA', 'VAIG')
styles = ('-R', '-B', '-I', '-BI')
stylesName = ('Regular', 'Bold', 'Italic', 'Bold Italic')
stylesLegacy = ('', 'BD', 'I', 'BI')

if '-s' in opts:
    faces = (faces[0],)
    facesLegacy = (facesLegacy[0],)
    styles = (styles[0],)
    stylesName = (stylesName[0],)
    stylesLegacy = (stylesLegacy[0],)

# set build parameters
fontbase = 'source/'
archive = fontbase + 'archive/'
generated = 'generated/'
tag = script.upper()

panose = [2, 0, 0, 3]
codePageRange = [0, 29]
unicodeRange = [0, 1, 2, 3, 4, 5, 6, 7, 15, 20, 29, 31, 32, 33, 35, 38, 39, 40, 45, 57, 60, 62, 67, 69, 91]
hackos2 = os2.hackos2(panose, codePageRange, unicodeRange)

if '-l' in opts:
    for f, fLegacy in zip(faces, facesLegacy):
        for (s, sn, sLegacy) in zip(styles, stylesName, stylesLegacy):
            gentium = '../../../../latn/fonts/gentium_local/basic/1.102/zip/unhinted/2048/GenBkBas' + s.replace('-', '') + '.ttf'
            charis = '../../../../latn/fonts/charis_local/5.000/zip/unhinted/2048/CharisSIL' + s + '.ttf'
            extra = '../' + archive + 'VAIG' + sLegacy + '.ttf'
            missing_face = fLegacy
            if missing_face == 'AUVA':
                missing_face = 'VAIG' # used to be THIR
            missing = '../' + archive + missing_face + sLegacy + '.ttf'
            font(target = process('ufo/' + f + '-' + sn.replace(' ', '') + '.ttf',
                    cmd(hackos2 + ' ${DEP} ${TGT}'),
                    name(f, lang='en-US', subfamily=(sn))
                    ),
                source = legacy(f + s + '.ttf',
                                source = archive + 'unhinted/' + fLegacy + sLegacy + '.ttf',
                                xml = fontbase + 'thiruvalluvar_unicode.xml',
                                params = '-f ' + charis + ' -f ' + extra + ' -f ' + missing,
                                noap = '')
                )

psfix = 'cp' if '-p' in opts else 'psfix'

# create('master.sfd', cmd("../tools/ffaddapstotaml ${SRC} ${TGT}", ["source/master_src.sfd"]))
if '-l' in opts:
    faces = list()
for f in faces:
    p = package(
        appname = APPNAME + '-' + f.lower(),
        version = VERSION,
        docdir = DOCDIR # 'documentation'
    )
    for (s, sn) in zip(styles, stylesName):
        snf = '-' + sn.replace(' ', '')
        fontfilename = tag + f + snf
        if f == 'ThiruValluvar':
            ot = f + s
        else:
            ot = 'additional_faces'
        font(target = process(fontfilename + '.ttf',
                #cmd(hackos2 + ' ${DEP} ${TGT}'),
                name(tag + ' ' + f, lang='en-US', subfamily=(sn))
                ),
            source = fontbase + f + snf + '.ufo',
            # source = fontbase + f + snf + '.sfd',
            # sfd_master = 'master.sfd',
            # opentype = internal(),
            # sfd_master = 'source/master_src.sfd',
            # opentype = fea(fontbase + 'master_src.fea', no_make = True),
            opentype = fea(fontbase + 'master.fea', no_make = True),
            # opentype = fea(fontbase + ot + '.fea', no_make = True),
            graphite = gdl(generated + f + snf + '.gdl',
                master = fontbase + 'master.gdl',
                make_params = '-l last -p 1',
                params =  '-e ' + f + snf + '_gdlerr.txt'
                ),
            #classes = fontbase + 'thiruvalluvar_classes.xml',
            ap = generated + f + snf + '.xml',
            version = VERSION,
            woff = woff('woff/' + fontfilename + '.woff', params = '-v ' + VERSION + ' -m ../' + fontbase + f + '-WOFF-metadata.xml'),
            script = 'taml',
            # extra_srcs = ['tools/ffaddapstotaml'],
            package = p,
            fret = fret(params = '')
        )
