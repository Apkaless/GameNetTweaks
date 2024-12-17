import winreg
import socket
from colorama import Fore, init
import os
import time

def banner():
    print(fr'''{cyan}
 ▄▄▄       ██▓███   ██ ▄█▀▄▄▄       ██▓    ▓█████   ██████   ██████ 
▒████▄    ▓██░  ██▒ ██▄█▒▒████▄    ▓██▒    ▓█   ▀ ▒██    ▒ ▒██    ▒ 
▒██  ▀█▄  ▓██░ ██▓▒▓███▄░▒██  ▀█▄  ▒██░    ▒███   ░ ▓██▄   ░ ▓██▄   
░██▄▄▄▄██ ▒██▄█▓▒ ▒▓██ █▄░██▄▄▄▄██ ▒██░    ▒▓█  ▄   ▒   ██▒  ▒   ██▒
 ▓█   ▓██▒▒██▒ ░  ░▒██▒ █▄▓█   ▓██▒░██████▒░▒████▒▒██████▒▒▒██████▒▒
{pink} ▒▒   ▓▒█░▒▓▒░ ░  ░▒ ▒▒ ▓▒▒▒   ▓▒█░░ ▒░▓  ░░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
{pink}  ▒   ▒▒ ░░▒ ░     ░ ░▒ ▒░ ▒   ▒▒ ░░ ░ ▒  ░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░
{pink}  ░   ▒   ░░       ░ ░░ ░  ░   ▒     ░ ░      ░   ░  ░  ░  ░  ░  ░  
{pink}      ░  ░         ░  ░        ░  ░    ░  ░   ░  ░      ░        ░

                        {green}Hi {pink}[{os.getlogin()}{pink}]

                        {cyan}Welcome To {pink}Networking Tweaks For Online Gaming

                        {cyan}Visit My Profiles At: 
                        {cyan}Github: {pink}github.com/apkaless
                        {cyan}Instagram: {pink}instagram.com/apkaless
                        {cyan}Credits To {pink}Apkaless
''')
    
def SetGPUCPUPriority(gp: int, cp: int):
    Games_subKey = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games'
    try:
        Games_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Games_subKey, access=winreg.KEY_ALL_ACCESS)
    except:
        print(f'\n{red}[-] Error: Permission Denied. Please Open As Admin.')
        return False
    try:
        winreg.SetValueEx(Games_reg, 'GPU Priority', 0, winreg.REG_DWORD, gp)
        winreg.SetValueEx(Games_reg, 'Priority', 0, winreg.REG_DWORD, cp)
        print(f'{green}\n[+] GPU & CPU\'s Priority Has Been Set For Gaming')
        return True
    except:
        print(f'\n{red}[-] Error: Cannot Set Data')
        return False
    
def DisableNaglesAlg(ipv4):
    active_interface_subkey = r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'

    try:
        interfaces = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, active_interface_subkey, 0, winreg.KEY_ALL_ACCESS)
    except:
        print(f'\n{red}Error: Can\'t Disable Nagle\'s Algorithm')
        return False
    total_interfaces = winreg.QueryInfoKey(interfaces)[0]

    for i in range(0, total_interfaces):
        interface = winreg.EnumKey(interfaces, i)
        current_interface_path = f'{active_interface_subkey}\\{interface}'
        current_interface_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, current_interface_path, 0 , winreg.KEY_ALL_ACCESS)
        values_count = winreg.QueryInfoKey(current_interface_key)[1]
        for i in range(0, values_count):
            vname, vdata, vtype = winreg.EnumValue(current_interface_key, i)
            if vdata == ipv4:
                try:
                    winreg.SetValueEx(current_interface_key, 'TcpAckFrequency', 0, winreg.REG_DWORD, 1)
                    winreg.SetValueEx(current_interface_key, 'TCPNoDelay', 0, winreg.REG_DWORD, 1)
                    print(f"\n{green}[+] Nagle's Algorithm {pink}Disabled")
                    return True
                except:
                    print(f'\n{red}Error: Can\'t Disable Nagle\'s Algorithm')
                    return False
        else:
            print(f'\n{red}[-] Error: No Active Interface Detected.')
        return True

def DisableNetworkThrottling():
    sub_key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile'
    full_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    try:

        winreg.SetValueEx(full_key, 'NetworkThrottlingIndex', 0, winreg.REG_DWORD, 0xffffffff)
        winreg.SetValueEx(full_key, 'SystemResponsiveness', 0, winreg.REG_DWORD, 0)
        print(f'\n{green}[+] Network Throttling Has Been {pink}Disabled')
    except:
        print(f'\n{red}Error While Disabling Network Throttling.')
        return False

def TcpOptimization():
    sub_key = r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters'
    full_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    try:

        winreg.SetValueEx(full_key, 'TcpTimedWaitDelay', 0, winreg.REG_DWORD, 30)
        winreg.SetValueEx(full_key, 'MaxUserPort', 0, winreg.REG_DWORD, 65534)
        winreg.SetValueEx(full_key, 'TcpMaxDataRetransmissions', 0, winreg.REG_DWORD, 5)
        print(f'\n{green}[+] TCP Optimization Successful:\n\n\tTcpTimedWaitDelay Set To -> 30\n\tMaxUserPort Set To -> 65534\n\tTcpMaxDataRetransmissions Set To -> 5')
    except:
        print(f'\n{red}Error While Optimizing TCP.')
        return False
    
def GetCurrentIPV4():
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ipv4Address = s.getsockname()[0]
    return ipv4Address


def main():
    input(f'{green}..............................[HIT ENTER TO START THE PROCESS]..............................')
    time.sleep(1)
    SetGPUCPUPriority(8, 6)
    time.sleep(0.1)
    DisableNaglesAlg(GetCurrentIPV4())
    time.sleep(0.3)
    DisableNetworkThrottling()
    time.sleep(0.6)
    TcpOptimization()
    time.sleep(0.9)

    input('\n.............................................')

if __name__ == '__main__':
    init(convert=True)
    green = Fore.GREEN
    red = Fore.RED
    cyan = Fore.CYAN
    pink = Fore.LIGHTMAGENTA_EX
    banner()
    main()
