import winreg
import socket
from colorama import Fore, init
import os
import time
import psutil
import re
import subprocess
import random



def banner():

    print(rf"""{bold}{cyan}
      ___ ___  __   __   __   __  ___  ___  __  
|\ | |__   |  |__) /  \ /  \ /__`  |  |__  |__) 
| \| |___  |  |__) \__/ \__/ .__/  |  |___ |  \ 
                                                
{yellow}╔═════════════════════════════════════════════════════════════════════╗
║ {cyan}Welcome, {os.getlogin()}!{yellow}                                                     ║
║ This tool is designed to {pink}boost your network{yellow} for online gaming and   ║
║ enhance your {pink}connectivity experience.{yellow}                               ║
╚═════════════════════════════════════════════════════════════════════╝
{cyan}➤ {cyan}Github: {pink}github.com/apkaless
{cyan}➤ {cyan}Instagram: {pink}instagram.com/apkaless
{cyan}➤ {cyan}Credits: {pink}Apkaless
{reset}""")




    
def SetGPUCPUPriority(gp: int, cp: int):
    Games_subKey = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games'
    try:
        Games_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Games_subKey, access=winreg.KEY_ALL_ACCESS)
    except:
        print(f'\n{bold}{red}[-] Error: Permission Denied. Please Open As Admin.')
        return False
    try:
        winreg.SetValueEx(Games_reg, 'GPU Priority', 0, winreg.REG_DWORD, gp)
        winreg.SetValueEx(Games_reg, 'Priority', 0, winreg.REG_DWORD, cp)
        print(f'{bold}{cyan}\n[+] GPU & CPU\'s Priority Has Been Set For {pink}Gaming')
        return True
    except:
        print(f'\n{bold}{red}[-] Error: Cannot Set Data')
        return False
    
def DisableNaglesAlg(ipv4):
    active_interface_subkey = r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces'
    try:
        interfaces = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, active_interface_subkey, 0, winreg.KEY_ALL_ACCESS)
    except:
        print(f'\n{bold}{red}Error: Can\'t Disable Nagle\'s Algorithm')
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
                    print(f"\n{bold}{cyan}[+] Nagle's Algorithm {pink}Disabled")
                    return True
                except:
                    print(f'\n{bold}{red}Error: Can\'t Disable Nagle\'s Algorithm')
                    return False
    else:
        print(f'\n{bold}{red}[-] Error: No Active Interface Detected.')

    return True

def DisableNetworkThrottling():
    sub_key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile'
    full_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    try:

        winreg.SetValueEx(full_key, 'NetworkThrottlingIndex', 0, winreg.REG_DWORD, 0xffffffff)
        winreg.SetValueEx(full_key, 'SystemResponsiveness', 0, winreg.REG_DWORD, 0)
        print(f'\n{bold}{cyan}[+] Network Throttling Has Been {pink}Disabled')
    except:
        print(f'\n{bold}{red}Error While Disabling Network Throttling.')
        return False

def TcpOptimization():
    sub_key = r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters'
    full_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    try:

        winreg.SetValueEx(full_key, 'TcpTimedWaitDelay', 0, winreg.REG_DWORD, 30)
        winreg.SetValueEx(full_key, 'MaxUserPort', 0, winreg.REG_DWORD, 65534)
        winreg.SetValueEx(full_key, 'TcpMaxDataRetransmissions', 0, winreg.REG_DWORD, 5)
        print(f'\n{bold}{cyan}[+] TCP Optimization Successful:\n\n\tTcpTimedWaitDelay Set To -> {pink}30\n\t{cyan}MaxUserPort Set To -> {pink}65534\n\t{cyan}TcpMaxDataRetransmissions Set To -> {pink}5\n')
    except:
        print(f'\n{bold}{red}Error While Optimizing TCP.')
        return False

def GetAdapterName(subkey):
    main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey, 0, winreg.KEY_ALL_ACCESS)
    values_count = winreg.QueryInfoKey(main_key)[1]
    for i in range(0, values_count):
        vname, vdata, vtype = winreg.EnumValue(main_key, i)
        if 'DriverDesc' in vname:
            return vdata

def GetMaxSpeed(full_key):
    res = subprocess.check_output(fr'reg query {full_key}\Ndi\params\*SpeedDuplex\enum', shell=True)
    decoded_res = res.decode().strip()
    key = re.search(r'HKEY_LOCAL_MACHINE\\.+', decoded_res).group()
    clean_res = decoded_res.strip(key)
    final_res = clean_res.strip()
    string_numbers = re.findall(r'\d+', final_res)
    int_numbers = list(map(int, string_numbers))
    int_numbers.sort()
    return int_numbers[-1]

def OptimizeActiveAdapter(transportName):
    sub_key = r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}'
    main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    sub_keys_count = winreg.QueryInfoKey(main_key)[0]
    for i in range(0, sub_keys_count):
        full_sub_key = f'{sub_key}\\{winreg.EnumKey(main_key, i)}'
        try:
            full_main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, full_sub_key, 0, winreg.KEY_ALL_ACCESS)
            values_count = winreg.QueryInfoKey(full_main_key)[1]
            registry_values = [
                ('*WakeOnMagicPacket', 0),
                ('*WakeOnPattern', 0),
                ('WolShutdownLinkSpeed', 2),
                ('TxIntDelay', 0),
                ('TxAbsIntDelay', 0),
                ('RxIntDelay', 0),
                ('RxAbsIntDelay', 0),
                ('PowerSavingMode', 0),
                ('*LsoV2IPv4', 0),
                ('*LsoV2IPv6', 0),
                ('*InterruptModeration', 0),
                ('*FlowControl', 3),
                ('*EEE', 0),
                ('*SpeedDuplex', 2500),
                ('*TCPChecksumOffloadIPv4', 3),
                ('*TCPChecksumOffloadIPv6', 3),
                ('*UDPChecksumOffloadIPv4', 3),
                ('*UDPChecksumOffloadIPv6', 3),
                ('AdvancedEEE', 0)
            ]
            random_times = [0.1, 0.2, 0.3, 0.01]

            for i in range(0, values_count):
                try:
                    if transportName in winreg.EnumValue(full_main_key,i):
                        adapter_name = GetAdapterName(full_sub_key)
                        full_main_key = f'HKEY_LOCAL_MACHINE\\{full_sub_key}'
                        max_speed = GetMaxSpeed(full_main_key)
                        subprocess.run(fr'reg add {full_main_key} /v AdvancedEEE /t REG_SZ /d 0 /f && reg add {full_main_key} /v *EEE /t REG_SZ /d 0 /f && reg add {full_main_key} /v *FlowControl /t REG_SZ /d 3 /f && reg add {full_main_key} /v *InterruptModeration /t REG_SZ /d 0 /f && reg add {full_main_key} /v *LsoV2IPv6 /t REG_SZ /d 0 /f && reg add {full_main_key} /v *LsoV2IPv4 /t REG_SZ /d 0 /f && reg add {full_main_key} /v PowerSavingMode /t REG_SZ /d 0 /f && reg add {full_main_key} /v RxAbsIntDelay /t REG_SZ /d 0 /f && reg add {full_main_key} /v RxIntDelay /t REG_SZ /d 0 /f && reg add {full_main_key} /v TxAbsIntDelay /t REG_SZ /d 0 /f && reg add {full_main_key} /v TxIntDelay /t REG_SZ /d 0 /f && reg add {full_main_key} /v *WakeOnPattern /t REG_SZ /d 0 /f && reg add {full_main_key} /v *WakeOnMagicPacket /t REG_SZ /d 0 /f && reg add {full_main_key} /v *SpeedDuplex /t REG_SZ /d {max_speed} /f && reg add {full_main_key} /v *TCPChecksumOffloadIPv4 /t REG_SZ /d 3 /f && reg add {full_main_key} /v *TCPChecksumOffloadIPv6 /t REG_SZ /d 3 /f && reg add {full_main_key} /v *UDPChecksumOffloadIPv4 /t REG_SZ /d 3 /f && reg add {full_main_key} /v *UDPChecksumOffloadIPv6 /t REG_SZ /d 3 /f && reg add {full_main_key} /v WolShutdownLinkSpeed /t REG_SZ /d 2 /f', shell=True, text=True, stdout=subprocess.PIPE)
                except:
                    pass

        except:
            pass
        
    print(f'{bold}{cyan}[+] {adapter_name}:\n')    
    for value_name, value_data in registry_values:
        print(f"\t{bold}{cyan}[+] {value_name} Set --> {pink}{value_data}")
        time.sleep(random.choice(random_times))

def GetMacAddress():
    current_ip = GetCurrentIPV4()
    for iface_name, iface_details in psutil.net_if_addrs().items():
        for i in iface_details:
            if i.family == -1:
                mac_address = i.address
            if current_ip in i.address:
                return iface_name, mac_address
    else:
        return False

def GetTransName(macAddress):
    trans_command = 'getmac'
    transport_regex = '{.+}'
    output = subprocess.check_output(trans_command, stderr=subprocess.PIPE, shell=True, text=True)
    results = output.split()
    for i in results:
        currentIndex = results.index(i)
        if macAddress in i:
            NoneCleantransportname = results[currentIndex + 1]
            CleanTransName = re.search(transport_regex, NoneCleantransportname)
            if CleanTransName:
                return CleanTransName.group()

def GetCurrentIPV4():
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ipv4Address = s.getsockname()[0]
    return ipv4Address


def main():
    input(f"{bold}{yellow}........................[ PRESS ENTER TO LAUNCH THE TOOL ]........................{reset}")
    time.sleep(1)
    SetGPUCPUPriority(8, 6)
    time.sleep(0.1)
    DisableNaglesAlg(GetCurrentIPV4())
    time.sleep(0.3)
    DisableNetworkThrottling()
    time.sleep(0.6)
    TcpOptimization()
    time.sleep(0.9)
    OptimizeActiveAdapter(GetTransName(GetMacAddress()[1]))
    time.sleep(0.5)
    input('\n.............................................')

if __name__ == '__main__':
    init(convert=True)
    red = Fore.RED
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    pink = '\033[95m'
    bold = '\033[1m'
    reset = '\033[0m'
    banner()
    main()