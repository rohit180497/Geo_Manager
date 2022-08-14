from matplotlib import offsetbox
from questionary import password


@echo off

set /p service = 'Enter Service: '
set /p user = 'Enter username/ID'

set "psCommand = powershell -command "$pword = read-host 'Enter Password' -AsSecureString ; ^
    $BSTR  = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($pword); ^
        [System.Runtime.InteropServices.Marshal]:: PtrToStringAuto($BSTR)""
for /f "usebaclq delims=" %%p in ('&psCommand') do set password= %%password

python password_manager.py %service% %user% %password%