@echo off
set num=0
For /r %%i in (*.dat) do (
set /a num+=1
echo %%i
call echo �� %%num%% ���ļ�����ɹ�
ren "%%i" "%%~ni.pcm")
echo �� %num%���ļ�������ɹ�
pause>nul