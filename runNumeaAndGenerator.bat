@echo off
setlocal enabledelayedexpansion 
setlocal enableextensions



set BENCHMARK=7
REM ####     1 - one body (arch) - quasi-static problem
REM ####     2 - two bodies (rectangular and arch) in mutual contact - quasi-static problem
REM ####     3 - two squares (two pieces) in mutual contact - quasi-static problem
REM ####     4 - one beam (one piece) - time-harmonic problem
REM ####     5 - one beam (one piece) - time-harmonic problem (different BC as in 4)
REM ####     6 - one beam (one piece) - quasi-static problem
REM ####     7 - one beam (two pieces) - mortar - quasi-static problem
REM ####     8 - two boxes in mutual contact - quasi-static problem
REM ####     9 - two curved boxes in mutual contact - quasi-static problem


set SOLVERS=2
REM ####    -1  - files *.vtu and *.nma are generated only (numea is not launched)
REM ####     0  - launch ddsolv with '1' mpi process
REM ####     1  - launch ddsolv with '1' mpi process + pardiso 
REM ####     2  - launch ddsolv with 'n' mpi processes (n = # subdomains)
REM ####     3  - launch ddsolv with 'n' mpi processes + pardiso 
REM ####     4  - launch pardiso only


set elm_nx1=6
set elm_ny1=6
set elm_nz1=3

set sub_Nx1=1
set sub_Ny1=2
set sub_Nz1=1

set elm_nx2=7
set elm_ny2=7
set elm_nz2=6 

set sub_Nx2=1
set sub_Ny2=1
set sub_Nz2=2

REM ####     set "DEVENV_WAS_CALLED=0"

REM ####     set path to "python.exe"
set PYTHON_EXE="C:\Users\mar440\AppData\Local\Continuum\Anaconda2\python.exe" 

REM ####     set path to "numea_driver.exe"
set NUMEA_EXE="c:\Build_NUMEA_dev_am\Src\Release\numea_driver.exe" 

REM ####     path to evironment variables setup file (for numea etc...)
set PATH_TO_DEVENV_BAT_FILE="C:\devenv\win64\devenv_win64_v0_0.bat"

REM ####     set blablafile (true or false)
set blablafile="true"

REM ####     set dumpfileCSRmatrix (true or false)
set dumpfileCSRmatrix="true"

REM ####     set dumpfile (true or false)
set dumpfile="false"

REM ####     set FETI (1 or 2)
set FETI="2"

REM ####     set iterative solver tolerance 
set eps_iter="1e-6"

REM ####    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
REM ####    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
REM ####    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
REM ####    +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
REM


REM ####     set name of "*.nma" file (solved by ddsolv)
set NMA_FILE="input"!BENCHMARK!".nma" 


rem IF %BENCHMARK%==4 (
rem @ECHO "  For BENCHMARK == 4 nothing to do.                   "
rem @ECHO "  set another benchmar (number from 1,2,4,5,6,7,8,9)  "
rem EXIT /b
rem )

REM MPI is called according to exact number of subdomains

REM 1 domain in 2D
IF !BENCHMARK!==1 (
set sub_Nz1=1
set sub_Nx2=0
set sub_Ny2=0
set sub_Nz2=0
)

REM 2 domains in 2D
IF !BENCHMARK!==2 (
set sub_Nz1=1
)

REM 2 domains in 2D
IF !BENCHMARK!==3 (
set sub_Nz1=1
)

REM 1 domain in 3D
IF !BENCHMARK!==4 (
set sub_Nx2=0
set sub_Ny2=0
set sub_Nz2=0
)

REM 1 domain in 3D
IF !BENCHMARK!==5 (
set sub_Nx2=0
set sub_Ny2=0
set sub_Nz2=0
)

REM 1 domain in 3D
IF !BENCHMARK!==6 (
set sub_Nx2=0
set sub_Ny2=0
set sub_Nz2=0
)

REM BENCHMARKS = 8, 9 are two 3-dim domains (no need to correct number of MPI processes)



REM >output.txt 2>&1  ( 
REM >output.txt ( 

set /A nnd1_1=!elm_nx1!*!sub_Nx1!+1
set /A nnd1_2=!elm_ny1!*!sub_Ny1!+1
set /A nnd1_3=!elm_nz1!*!sub_Nz1!+1 
set /A nnd1=!nnd1_1!*!nnd1_2!*!nnd1_3!
set /A nnd2_1=!elm_nx1!*!sub_Nx1!+1
set /A nnd2_2=!elm_ny1!*!sub_Ny1!+1
set /A nnd2_3=!elm_nz1!*!sub_Nz1!+1
set /A nnd2=!nnd2_1!*!nnd2_2!*!nnd2_3!
set /A nnd=!nnd1! + !nnd2! 

set /A nSub=!sub_Nx1!*!sub_Ny1!*!sub_Nz1! + !sub_Nx2!*!sub_Ny2!*!sub_Nz2!
REM ####      
@echo number of subdomanis: !nSub! 
@echo number of nodes:      !nnd! 
REM ####      
REM ####     generated vtu file (according to var "sub_Nphi", "sub_Nradial, ...)
set vtuFile=mesh.vtu
set meshTableFiles="*.dat" 
set currentDir=!cd!
set workingDirectory=%~dp0numea_solution
IF NOT EXIST !workingDirectory! (mkdir  !workingDirectory! )
REM ####    REM ####    
set meshGeneratorPath=%~dp0__python__
set meshGeneratorFilePy=create_vtu_for_numea.py 
set modifNumeaFilePy=modifNumeaFile.py
REM ####    REM ####    
REM ####     if "devenv_win64_v0_0.bat" is called first time, this *.bat file must be launched again
IF "!DEVENV_WAS_CALLED!"=="" ( 
set DEVENV_WAS_CALLED=0
)
IF "!DEVENV_WAS_CALLED!" EQU "0" (
@ECHO "     ... devenv is being setup ..." 
call !PATH_TO_DEVENV_BAT_FILE! 
) ELSE (
@echo "devenv ... was already setup"
)

REM ####     setup mpi_size
set /A mpi_size=!sub_Nx1!*!sub_Ny1!*!sub_Nz1! + !sub_Nx2!*!sub_Ny2!*!sub_Nz2!  

REM ####     generatin new '*.vtu' file
cd /d !meshGeneratorPath! 
!PYTHON_EXE! !meshGeneratorFilePy! BENCHMARK !BENCHMARK! Nx1 !sub_Nx1! Ny1 !sub_Ny1! Nz1 !sub_Nz1! nx1 !elm_nx1! ny1 !elm_ny1! nz1 !elm_nz1! Nx2 !sub_Nx2! Ny2 !sub_Ny2! Nz2 !sub_Nz2! nx2 !elm_nx2! ny2 !elm_ny2! nz2 !elm_nz2! 

REM ####     copy vtu to working directory
copy /y !meshGeneratorPath!\!vtuFile!  !workingDirectory!
copy /y !meshGeneratorPath!\!meshTableFiles!  !workingDirectory!

cd /d !workingDirectory! 
REM ####     copy nma file to working directory
copy /y "..\"!NMA_FILE! .




IF !SOLVERS! EQU -1 (
!PYTHON_EXE! !meshGeneratorPath!\!modifNumeaFilePy! NMA_FILE !NMA_FILE!  Solver "gen_solver_ddsolv" blablafile !blablafile! dumpfile !dumpfile! FETI !FETI! eps_iter !eps_iter! dumpfileCSRmatrix !dumpfileCSRmatrix!
@echo " only *.nma and *.vtu files are generated (without NUMEA)"
cd /d !currentDir! 
EXIT /b
) ELSE (
@echo " NUMEA IS LAUNCHING ..."
)


IF !SOLVERS! LSS 2 (set mpi_size=1)
@echo "mpi_size="!mpi_size! 


@echo !mpi_size!
set USE_PARDISO=0
IF !SOLVERS! EQU 1 (set /A USE_PARDISO=1)
IF !SOLVERS! EQU 3 (set /A USE_PARDISO=1)
IF !SOLVERS! EQU 4 (set /A USE_PARDISO=1)


@echo "USE_PARDISO="!USE_PARDISO!


set /A nnd1_1=!elm_nx1!*!sub_Nx1!+1

IF !USE_PARDISO! EQU 1 ( 
!PYTHON_EXE! !meshGeneratorPath!\!modifNumeaFilePy! NMA_FILE !NMA_FILE!  Solver "gen_solver_pardiso" blablafile !blablafile! dumpfile !dumpfile! FETI !FETI! eps_iter !eps_iter! dumpfileCSRmatrix !dumpfileCSRmatrix!
!NUMEA_EXE!  !NMA_FILE! 
if !SOLVERS! NEQ 4 (
timeout 2
)
) 



IF !SOLVERS! LSS 4  (
!PYTHON_EXE! !meshGeneratorPath!\!modifNumeaFilePy! NMA_FILE !NMA_FILE!  Solver "gen_solver_ddsolv" blablafile !blablafile! dumpfile !dumpfile! FETI !FETI! eps_iter !eps_iter! dumpfileCSRmatrix !dumpfileCSRmatrix!
mpiexec.smpd -n !mpi_size! !NUMEA_EXE!  !NMA_FILE! )

REM ####     go back to original directory
cd /d !currentDir! 
REM ####  
REM )
