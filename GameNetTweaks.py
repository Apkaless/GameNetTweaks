import winreg
import socket
from colorama import Fore, init
import os
import time
import psutil
import re
import subprocess
import random
import platform
import ctypes


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
        winreg.SetValueEx(full_key, 'EnableLargeSendOffload', 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(full_key, 'TcpInitialRtt', 0, winreg.REG_DWORD, 3)
        winreg.SetValueEx(full_key, 'Tcp1323Opts', 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(full_key, 'EnableTCPChimney', 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(full_key, 'EnableTCPA', 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(full_key, 'EnableRSS', 0, winreg.REG_DWORD, 1)
        print(f'\n{bold}{cyan}[+] TCP Optimization Successful:\n\n\tTcpTimedWaitDelay Set To -> {pink}30\n\t{cyan}MaxUserPort Set To -> {pink}65534\n\t{cyan}TcpMaxDataRetransmissions Set To -> {pink}5\n\t{cyan}EnableLargeSendOffload Set To -> {pink}0\n')
    except:
        print(f'\n{bold}{red}Error While Optimizing TCP.')
        return False

def DisableQOS():
    sub_key = r'SOFTWARE\Policies\Microsoft\Windows\Psched'
    try:
        main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(main_key, 'NonBestEffortLimit', 0, winreg.REG_DWORD, 0)
        print(f'\t{bold}{cyan}[+] QOS Reserved Bandwidth Set --> {pink} 0')
    except PermissionError:
        print(f'\t{bold}{red}Error While Disabling QoS Reserved Bandwidth')
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
            # Value name, Data Type, Value
            registry_values = [
                ('*WakeOnMagicPacket', 'REG_SZ',0),
                ('*WakeOnPattern', 'REG_SZ',0),
                ('WolShutdownLinkSpeed', 'REG_SZ',2),
                ('TxIntDelay', 'REG_SZ',0),
                ('TxAbsIntDelay', 'REG_SZ',0),
                ('RxIntDelay', 'REG_SZ',0),
                ('RxAbsIntDelay', 'REG_SZ',0),
                ('PowerSavingMode', 'REG_SZ',0),
                ('*LsoV2IPv4', 'REG_SZ',0),
                ('*LsoV2IPv6', 'REG_SZ',0),
                ('*InterruptModeration', 'REG_SZ',0),
                ('*EEE', 'REG_SZ',0),
                ('*TCPChecksumOffloadIPv4', 'REG_SZ', 3),
                ('*TCPChecksumOffloadIPv6', 'REG_SZ',3),
                ('*UDPChecksumOffloadIPv4', 'REG_SZ',3),
                ('*UDPChecksumOffloadIPv6', 'REG_SZ',3),
                ('*ReceiveBuffers', 'REG_SZ', 2048),
                ('*TransmitBuffers', 'REG_SZ', 4096),
                ('*FlowControl', 'REG_SZ', 0),
                ('FlowControlCap', 'REG_SZ', 0),
                ('*InterruptModerationRate', 'REG_SZ', 0),
                ('*AdaptiveInterFrameSpacing', 'REG_SZ', 1),
                ('EnablePMTUDiscovery', 'REG_DWORD', 0)
            ]

            random_times = [0.1, 0.2, 0.3, 0.01]

            for i in range(0, values_count):
                try:
                    if transportName in winreg.EnumValue(full_main_key,i):
                        adapter_name = GetAdapterName(full_sub_key)
                        full_main_key = f'HKEY_LOCAL_MACHINE\\{full_sub_key}'
                        max_speed = GetMaxSpeed(full_main_key)
                        registry_values.append(('*SpeedDuplex', 'REG_SZ', max_speed))
                        for reg_key, dtype, reg_value in registry_values:
                            subprocess.run(fr'reg add {full_main_key} /v {reg_key} /t {dtype} /d {reg_value} /f', shell=True, text=True, stdout=subprocess.PIPE)
                except:
                    pass
        except:
            pass
        
    print(f'{bold}{cyan}[+] {adapter_name}:\n')    
    for value_name, dtype, value_data in registry_values:
        print(f"\t{bold}{cyan}[+] {value_name} Set --> {pink}{value_data}")
        time.sleep(random.choice(random_times))

def set_priority_control():
    sub_key = r'SYSTEM\CurrentControlSet\Control\PriorityControl'
    try:
        full_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0 , winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(full_key, 'Win32PrioritySeparation', 0, winreg.REG_DWORD, 42)
        print(f"\t{bold}{cyan}[+] Win32PrioritySeparation Set To --> {pink}42 {yellow}(Optimize priority for foreground tasks)")
    except PermissionError:
        print(f'\t{bold}{red}[-] Error: Permission Denied to modify PriorityControl settings.')

def EliminateBufferBloat():
    commands = ['PowerShell.exe Set-NetTCPSetting -SettingName internet -AutoTuningLevelLocal disabled', 'PowerShell.exe Set-NetOffloadGlobalSetting -ReceiveSegmentCoalescing disabled',
'PowerShell.exe Set-NetOffloadGlobalSetting -ReceiveSideScaling disabled',
'PowerShell.exe Set-NetOffloadGlobalSetting -Chimney disabled',
'PowerShell.exe Disable-NetAdapterLso -Name *',
'PowerShell.exe Disable-NetAdapterChecksumOffload -Name *', 'PowerShell.exe Set-NetTCPSetting -SettingName Datacenter -AutoTuningLevel Disabled',
'PowerShell.exe ipconfig /flushdns', 'PowerShell.exe Disable-NetAdapterRsc -Name "Ethernet"']
    
    for command in commands:
        try:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
        except:
            print(f'\t{bold}{red}[-] Unable to execute command >> {command}')
            pass

    print(f"\t{bold}{cyan}[+] AutoTuningLevelLocal Internet Set --> {pink}Disabled")
    time.sleep(0.1)
    print(f"\t{bold}{cyan}[+] AutoTuningLevelLocal Datacenter Set --> {pink}Disabled")
    time.sleep(0.2)
    print(f"\t{bold}{cyan}[+] ReceiveSegmentCoalescing Set --> {pink}Disabled")
    time.sleep(0.3)
    print(f"\t{bold}{cyan}[+] ReceiveSideScaling Set --> {pink}Disabled")
    print(f"\t{bold}{cyan}[+] Chimney Set --> {pink}Disabled")
    time.sleep(0.2)
    print(f"\t{bold}{cyan}[+] NetAdapterLso Set --> {pink}Disabled")
    print(f"\t{bold}{cyan}[+] NetAdapterChecksumOffload Set --> {pink}Disabled")
    time.sleep(0.2)
    print(f"\t{bold}{cyan}[+] DNS Cache --> {pink}Flushed")
    time.sleep(0.2)

    return True

def FastSendDatagram():
    sub_key = r'SYSTEM\CurrentControlSet\Services\AFD\Parameters'
    try:
        main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(main_key, 'FastSendDatagramThreshold', 0, winreg.REG_DWORD, 409600)
        print(f"\t{bold}{cyan}[+] FastSendDatagramThreshold Set --> {pink}409600")
    except PermissionError:
        print(f'\t{bold}{red}[-] Error: Unable To Set FastSendDatagramThreshold > Permission Denied.')

def DNSCache():
    sub_key = r'SYSTEM\CurrentControlSet\Services\Dnscache\Parameters'
    try:
        main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(main_key, 'MaxCacheTtl', 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(main_key, 'MaxNegativeCacheTtl', 0, winreg.REG_DWORD, 0)
        print(f"\t{bold}{cyan}[+] MaxCacheTtl Set --> {pink}1\n\t{bold}{cyan}[+] MaxNegativeCacheTtl Set --> {pink}0")
    except PermissionError:
        print(f'\t{bold}{red}[-] Error: Unable To Set DNSCache Values > Permission Denied.')

def PrioritizeInterfaceMetricForGaming():
    try:
        subprocess.run('powershell -Command "Set-NetIPInterface -InterfaceAlias "Ethernet" -InterfaceMetric 1"', shell=True, text=True, stdout=subprocess.PIPE)
        print(f"\t{bold}{cyan}[+] Interface Metric For Ethernet Set --> {pink}1")
    except:
        print(f'\t{bold}{red}[-] Error: Unable To Prioritize "Ethernet" For Online Gaming')

def SetPrivateNetwork():
    try:
        subprocess.run('powershell -Command "Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private"', shell=True, text=True, stdout=subprocess.PIPE)
        print(f"\t{bold}{cyan}[+] Network Category --> {pink}Private")
    except:
        print(f'\t{bold}{red}[-] Error: Unable To Set Network Category to Private')

def GetMacAddress():
    current_ip = GetCurrentIPV4()
    for iface_name, iface_details in psutil.net_if_addrs().items():
        for i in iface_details:
            if i.family == -1:
                mac_address = i.address
            if current_ip in i.address:
                return iface_name, mac_address
    else:
        print(f'\n{bold}{red}[-] Unable to obtain The MAC Address')
        input('\n\n>>>')
        return False

def GetTransName(macAddress):
    trans_command = 'getmac'
    transport_regex = '{.+}'
    try:
        output = subprocess.check_output(trans_command, stderr=subprocess.PIPE, shell=True, text=True)
        results = output.split()
        for i in results:
            currentIndex = results.index(i)
            if macAddress in i:
                NoneCleantransportname = results[currentIndex + 1]
                CleanTransName = re.search(transport_regex, NoneCleantransportname)
                if CleanTransName:
                    return CleanTransName.group()
    except:
        print(f'\n{bold}{red}[-] Unable to obtain The Transport Name')
        input('\n\n>>>')

def GetCurrentIPV4():
    socket.setdefaulttimeout(3)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ipv4Address = s.getsockname()[0]
        return ipv4Address
    except:
        print(f'\n{bold}{red}[-] Unable to obtain The IPv4 Address')
        input('\n\n>>>')


def is_windows():
    return platform.system() == 'Windows'


def is_admin():
    try:
        # Check for admin privileges
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

def main():
    if is_windows():
        if is_admin():
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
            EliminateBufferBloat()
            time.sleep(0.2)
            FastSendDatagram()
            time.sleep(0.2)
            SetPrivateNetwork()
            time.sleep(0.2)
            DNSCache()
            time.sleep(0.2)
            PrioritizeInterfaceMetricForGaming()
            time.sleep(0.3)
            DisableQOS()
            time.sleep(0.2)
            set_priority_control()
            time.sleep(1)
            input('\n.............................................')
        else:
            print(f"\n{bold}{red}The script is not running with administrative privileges\n")
            input('\n.............................................')
    else:
        print(f"\n{bold}{red}The system is not running Windows\n")
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