@echo off
:: setlocal enabledelayedexpansion 
:: enableextensions

::a.txt 2>&1


:: 2 - two bodies (rectangular and arch) in mutual contact
:: 3 - '''' nothing '''
:: 4 - two squers (two pieces) in mutual contact
:: 5 - one beam (one piece) - time-harmonic 
:: 6 - one beam (one piece) - quasi-static 
:: 7 - one beam (two pieces) - mortar - quasi-static 
:: 8 - two boxes in mutual contact
:: 9 - two curved boxes in mutual contact

set benchmark=1


set elm_nx1=4
set elm_ny1=4
set elm_nz1=8

set sub_Nx1=4
set sub_Ny1=2
set sub_Nz1=1

set elm_nx2=5
set elm_ny2=5
set elm_nz2=5 

set sub_Nx2=1
set sub_Ny2=1
set sub_Nz2=2
::
:: set "DEVENV_WAS_CALLED=0"
:: 
:: force setting for smallest possible mesh (circle 2  elem, square 1 elem)

set SOLVERS=2
::         -1  - only *.vtu and *.nma files are generated 
::  	    0  - launch ddsolv with '1' mpi process
::  	    1  - launch ddsolv with '1' mpi process + pardiso 
::  	    2  - launch ddsolv with 'n' mpi processes (n = # subdomains)
::  	    3  - launch ddsolv with 'n' mpi processes + pardiso 
::  	    4  - launch pardiso only
::::
:: set path to "python.exe"
set PYTHON_EXE="C:\Users\mar440\AppData\Local\Continuum\Anaconda2\python.exe" 

:: set path to "numea_driver.exe"
:: set NUMEA_EXE="c:\Build_NUMEA\Src\Release\numea_driver.exe" 
set NUMEA_EXE="c:\Build_NUMEA_dev_am\Src\Release\numea_driver.exe" 

:: set name of "*.nma" file (solved by ddsolv)
set NMA_FILE="input"%benchmark%".nma" 

:: path to evironment variables setup file (for numea etc...)
set PATH_TO_DEVENV_BAT_FILE="C:\devenv\win64\devenv_win64_v0_0.bat"

:: set blablafile (true or false)
set blablafile="true"

:: set dumpfileCSRmatrix (true or false)
set dumpfileCSRmatrix="false"

:: set dumpfile (true or false)
set dumpfile="true"

:: set FETI (1 or 2)
set FETI="2"

:: set iterative solver tolerance 
set eps_iter="1e-4"

::+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
::+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
::+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
::+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
::::
:: set small case
:::: 
::


set /A nDOF=((%elm_nx1%*%sub_Nx1%+1)*(%elm_ny1%*%sub_Ny1%+1)*(%elm_nz1%*%sub_Nz1%+1)+(%elm_nx2%*%sub_Nx2%+1)*(%elm_ny2%*%sub_Ny2%+1)*(%elm_nz2%*%sub_Nz2%+1))*3 



set /A nSub=%sub_Nx1%*%sub_Ny1%*%sub_Nz1% + %sub_Nx2%*%sub_Ny2%*%sub_Nz2%

@echo number of subdomanis: %nSub% 
@echo number of DOFs:       %nDOF% 

:: generated vtu file (according to var "sub_Nphi", "sub_Nradial, ...)
set vtuFile=mesh.vtu
set meshTableFiles="*.dat" 
set currentDir=%cd%
set workingDirectory=%~dp0numea_solution
IF NOT EXIST %workingDirectory% (mkdir  %workingDirectory% )
::::
set meshGeneratorPath=%~dp0__python__
set meshGeneratorFilePy=create_vtu_for_numea.py 
set modifNumeaFilePy=modifNumeaFile.py
::::
:: if "devenv_win64_v0_0.bat" is called first time, this *.bat file must be launched again
IF "%DEVENV_WAS_CALLED%" EQU "0" (
@ECHO "devenv is being setup, call 'runNumea...' again" 
call %PATH_TO_DEVENV_BAT_FILE% 
) ELSE (
@echo "devenv ... was already setup"
)
::::
:: setup mpi_size
set /A mpi_size=%sub_Nx1%*%sub_Ny1%*%sub_Nz1% + %sub_Nx2%*%sub_Ny2%*%sub_Nz2%  
::::
:: generatin new '*.vtu' file
cd /d %meshGeneratorPath% 
%PYTHON_EXE% %meshGeneratorFilePy% benchmark %benchmark% Nx1 %sub_Nx1% Ny1 %sub_Ny1% Nz1 %sub_Nz1% nx1 %elm_nx1% ny1 %elm_ny1% nz1 %elm_nz1% Nx2 %sub_Nx2% Ny2 %sub_Ny2% Nz2 %sub_Nz2% nx2 %elm_nx2% ny2 %elm_ny2% nz2 %elm_nz2% 


::::
:: copy vtu to working directory
copy /y %meshGeneratorPath%\%vtuFile%  %workingDirectory%
copy /y %meshGeneratorPath%\%meshTableFiles%  %workingDirectory%
::::
cd /d %workingDirectory% 
:: copy nma file to working directory
::copy /y "..\"%NMA_DDSOLV_FILE% .
copy /y "..\"%NMA_FILE% .
::IF EXIST "..\"%NMA_PARDISO_FILE% (copy /y "..\"%NMA_PARDISO_FILE% .)

IF %SOLVERS% LSS 2 (set mpi_size=1)

@echo "mpi_size="%mpi_size% 


IF %SOLVERS% EQU -1 (
set _ddsolv_or_pardiso="ddsolv" 
%PYTHON_EXE% %meshGeneratorPath%\%modifNumeaFilePy% NMA_FILE %NMA_FILE%  ddsolv_or_pardiso %_ddsolv_or_pardiso% blablafile %blablafile% dumpfile %dumpfile% FETI %FETI% eps_iter %eps_iter% dumpfileCSRmatrix %dumpfileCSRmatrix% 
@echo " only *.nma and *.vtu files are generated (without NUMEA)"
EXIT /b
) ELSE (
@echo " NUMEA IS LAUNCHING ..."
)





::::
@echo %mpi_size%
set USE_PARDISO=0
IF %SOLVERS% EQU 1 (set USE_PARDISO=1)
IF %SOLVERS% EQU 3 (set USE_PARDISO=1)
IF %SOLVERS% EQU 4 (set USE_PARDISO=1)

IF %USE_PARDISO% EQU 1 ( 
set _ddsolv_or_pardiso="pardiso" 
%PYTHON_EXE% %meshGeneratorPath%\%modifNumeaFilePy% NMA_FILE %NMA_FILE%  ddsolv_or_pardiso %_ddsolv_or_pardiso% blablafile %blablafile% dumpfile %dumpfile% FETI %FETI% eps_iter %eps_iter% dumpfileCSRmatrix %dumpfileCSRmatrix%
%NUMEA_EXE%  %NMA_FILE% 1>&2
) 

::set _ddsolv_or_pardiso="ddsolv" 
::%PYTHON_EXE% %meshGeneratorPath%\%modifNumeaFilePy% NMA_FILE %NMA_FILE%  ddsolv_or_pardiso %_ddsolv_or_pardiso% blablafile %blablafile% dumpfile %dumpfile% FETI %FETI% eps_iter %eps_iter% dumpfileCSRmatrix %dumpfileCSRmatrix%
::%NUMEA_EXE%  %NMA_FILE% 1>&2


::IF %SOLVERS% LSS 4  (
set _ddsolv_or_pardiso="ddsolv" 
%PYTHON_EXE% %meshGeneratorPath%\%modifNumeaFilePy% NMA_FILE %NMA_FILE%  ddsolv_or_pardiso %_ddsolv_or_pardiso% blablafile %blablafile% dumpfile %dumpfile% FETI %FETI% eps_iter %eps_iter% dumpfileCSRmatrix %dumpfileCSRmatrix%
mpiexec.smpd -n %mpi_size% %NUMEA_EXE%  %NMA_FILE% 1>&2
)

:: go back to original directory
cd /d %currentDir% 
::::
