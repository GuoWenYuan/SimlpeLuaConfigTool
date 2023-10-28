@echo on
cd /d %~dp0
REM "begin export table   export dir : ExprotData" 
CALL "BuildConfig/BuildConfig.exe"
PAUSE