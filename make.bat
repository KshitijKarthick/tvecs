@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=documentation
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% .
set I18NSPHINXOPTS=%SPHINXOPTS% .
set SPHINXAPIDOC=sphinx-apidoc
set SPHINXAPIDOCDIR=_dev_docs
set SRC_DIR=tvecs
set SPHINXAPIDOCTESTDIR=_test_docs
set SRC_TEST_DIR=tests
if NOT "%PAPER%" == "" (
	set ALLSPHINXOPTS=-D latex_paper_size=%PAPER% %ALLSPHINXOPTS%
	set I18NSPHINXOPTS=-D latex_paper_size=%PAPER% %I18NSPHINXOPTS%
)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  html       to make standalone HTML files
	echo.  dirhtml    to make HTML files named index.html in directories
	echo.  singlehtml to make a single large HTML file
	echo.  pickle     to make pickle files
	echo.  json       to make JSON files
	echo.  htmlhelp   to make HTML files and a HTML help project
	echo.  qthelp     to make HTML files and a qthelp project
	echo.  devhelp    to make HTML files and a Devhelp project
	echo.  epub       to make an epub
	echo.  epub3      to make an epub3
	echo.  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
	echo.  text       to make text files
	echo.  man        to make manual pages
	echo.  texinfo    to make Texinfo files
	echo.  gettext    to make PO message catalogs
	echo.  changes    to make an overview over all changed/added/deprecated items
	echo.  xml        to make Docutils-native XML files
	echo.  pseudoxml  to make pseudoxml-XML files for display purposes
	echo.  linkcheck  to check all external links for integrity
	echo.  doctest    to run all doctests embedded in the documentation if enabled
	echo.  coverage   to run coverage check of the documentation if enabled
	goto end
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	for /d %%i in (%SPHINXAPIDOCDIR\*) do rmdir /q /s %%i
	del /q /s %SPHINXAPIDOCDIR%\*
	for /d %%i in (%SPHINXAPIDOCTESTDIR\*) do rmdir /q /s %%i
	del /q /s %SPHINXAPIDOCTESTDIR%\*
	goto end
)


REM Check if sphinx-build is available and fallback to Python version if any
%SPHINXBUILD% 1>NUL 2>NUL
if errorlevel 9009 goto sphinx_python
goto sphinx_ok

:sphinx_python

set SPHINXBUILD=python -m sphinx.__init__
%SPHINXBUILD% 2> nul
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

:sphinx_ok


if "%1" == "html" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/html
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/html.
	goto end
)

if "%1" == "dirhtml" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b dirhtml %ALLSPHINXOPTS% %BUILDDIR%/dirhtml
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/dirhtml.
	goto end
)

if "%1" == "singlehtml" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b singlehtml %ALLSPHINXOPTS% %BUILDDIR%/singlehtml
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/singlehtml.
	goto end
)

if "%1" == "pickle" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b pickle %ALLSPHINXOPTS% %BUILDDIR%/pickle
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished; now you can process the pickle files.
	goto end
)

if "%1" == "json" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b json %ALLSPHINXOPTS% %BUILDDIR%/json
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished; now you can process the JSON files.
	goto end
)

if "%1" == "htmlhelp" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b htmlhelp %ALLSPHINXOPTS% %BUILDDIR%/htmlhelp
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished; now you can run HTML Help Workshop with the ^
.hhp project file in %BUILDDIR%/htmlhelp.
	goto end
)

if "%1" == "qthelp" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b qthelp %ALLSPHINXOPTS% %BUILDDIR%/qthelp
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished; now you can run "qcollectiongenerator" with the ^
.qhcp project file in %BUILDDIR%/qthelp, like this:
	echo.^> qcollectiongenerator %BUILDDIR%\qthelp\T-Vecs.qhcp
	echo.To view the help file:
	echo.^> assistant -collectionFile %BUILDDIR%\qthelp\T-Vecs.ghc
	goto end
)

if "%1" == "devhelp" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b devhelp %ALLSPHINXOPTS% %BUILDDIR%/devhelp
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished.
	goto end
)

if "%1" == "epub" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b epub %ALLSPHINXOPTS% %BUILDDIR%/epub
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The epub file is in %BUILDDIR%/epub.
	goto end
)

if "%1" == "epub3" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b epub3 %ALLSPHINXOPTS% %BUILDDIR%/epub3
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The epub3 file is in %BUILDDIR%/epub3.
	goto end
)

if "%1" == "latex" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished; the LaTeX files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "latexpdf" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	cd %BUILDDIR%/latex
	make all-pdf
	cd %~dp0
	echo.
	echo.Build finished; the PDF files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "latexpdfja" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b latex %ALLSPHINXOPTS% %BUILDDIR%/latex
	cd %BUILDDIR%/latex
	make all-pdf-ja
	cd %~dp0
	echo.
	echo.Build finished; the PDF files are in %BUILDDIR%/latex.
	goto end
)

if "%1" == "text" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b text %ALLSPHINXOPTS% %BUILDDIR%/text
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The text files are in %BUILDDIR%/text.
	goto end
)

if "%1" == "man" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b man %ALLSPHINXOPTS% %BUILDDIR%/man
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The manual pages are in %BUILDDIR%/man.
	goto end
)

if "%1" == "texinfo" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b texinfo %ALLSPHINXOPTS% %BUILDDIR%/texinfo
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The Texinfo files are in %BUILDDIR%/texinfo.
	goto end
)

if "%1" == "gettext" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b gettext %I18NSPHINXOPTS% %BUILDDIR%/locale
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The message catalogs are in %BUILDDIR%/locale.
	goto end
)

if "%1" == "changes" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b changes %ALLSPHINXOPTS% %BUILDDIR%/changes
	if errorlevel 1 exit /b 1
	echo.
	echo.The overview file is in %BUILDDIR%/changes.
	goto end
)

if "%1" == "linkcheck" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b linkcheck %ALLSPHINXOPTS% %BUILDDIR%/linkcheck
	if errorlevel 1 exit /b 1
	echo.
	echo.Link check complete; look for any errors in the above output ^
or in %BUILDDIR%/linkcheck/output.txt.
	goto end
)

if "%1" == "doctest" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b doctest %ALLSPHINXOPTS% %BUILDDIR%/doctest
	if errorlevel 1 exit /b 1
	echo.
	echo.Testing of doctests in the sources finished, look at the ^
results in %BUILDDIR%/doctest/output.txt.
	goto end
)

if "%1" == "coverage" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b coverage %ALLSPHINXOPTS% %BUILDDIR%/coverage
	if errorlevel 1 exit /b 1
	echo.
	echo.Testing of coverage in the sources finished, look at the ^
results in %BUILDDIR%/coverage/python.txt.
	goto end
)

if "%1" == "xml" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b xml %ALLSPHINXOPTS% %BUILDDIR%/xml
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The XML files are in %BUILDDIR%/xml.
	goto end
)

if "%1" == "pseudoxml" (
	%SPHINXAPIDOC% -o %SPHINXAPIDOCDIR% %SRC_DIR% .
	%SPHINXAPIDOC% -o %SPHINXAPIDOCTESTDIR% %SRC_TEST_DIR% .
	%SPHINXBUILD% -b pseudoxml %ALLSPHINXOPTS% %BUILDDIR%/pseudoxml
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The pseudo-XML files are in %BUILDDIR%/pseudoxml.
	goto end
)

:end
