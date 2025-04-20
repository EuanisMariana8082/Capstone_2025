@echo off
setlocal

set "fasconcat_dir=C:\Users\Rushe\Desktop\capstone 2025\FASconCAT"
set "fasconcat_script=FASconCAT-G_v1.06.1.pl"

echo Current directory:
cd

echo Files in current directory:
dir

cd %fasconcat_dir%

echo Current directory:
cd

echo Files in current directory:
dir

echo Processing file: cleaned_supermatrix.fas
perl %fasconcat_script% < input_commands.txt

endlocal
echo Done!
pause







