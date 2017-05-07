#####################################################################
#                                                                   #
#                               setup.py                            #
#                     Author: Angelika Kosciolek                    #
#                             20/03/2017                            #
#                                                                   #
#                  Description: Setup file for Py2Exe               #
#                                                                   #
#####################################################################

from distutils.core import setup
import matplotlib
import py2exe

my_data_files = matplotlib.get_py2exe_datafiles()


setup(
    windows=[{"script": "main.py"}],
    options={
             'py2exe': {
                        'excludes': ['_gtkagg', '_tkagg'],
                        'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                         'libgobject-2.0-0.dll',
                                         'oci.dll',
                                         'libgdk_pixbuf-2.0-0.dll',
                                         'QtCore4.dll'
                                         'QtGui4.dll',
                                         'libeay32.dll'
                                         'libmysql.dll',
                                         'phonon4.dll',
                                         'QtCLucene4.dll',
                                         'QtDeclarative4.dll',
                                         'QtDesigner4.dll',
                                         'QtHelp4.dll',
                                         'QtMultimedia4.dll',
                                         'QtNetwork4.dll',
                                         'QtOpenGL4.dll',
                                         'QtScript4.dll',
                                         'QtScriptTools4.dll',
                                         'QtSql4.dll',
                                         'QtSvg4.dll',
                                         'QtTest4.dll',
                                         'QtWebKit4.dll',
                                         'QtXml4.dll',
                                         'QtXmlPatterns4.dll',
                                         'ssleay32.dll'
                                         ],
                        'packages': ['matplotlib', 'pytz'],
                       }
            },
    data_files=my_data_files,
)
