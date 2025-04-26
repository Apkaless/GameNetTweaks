
# Network Optimizer for Online Gaming

## Version: 2.0  
**Author**: Apkaless  
[GitHub](https://github.com/apkaless) | [Instagram](https://instagram.com/apkaless)

---

### **Overview**

This tool is designed to optimize your system for online gaming by improving network performance, CPU and GPU priority, and overall connectivity. It disables certain network throttling features, enhances TCP/IP settings, and modifies registry values to ensure the best possible gaming experience.

### **Key Features**
1. **GPU & CPU Priority Boost**: Sets the priority of GPU and CPU for gaming to optimize performance.
2. **Disable Nagle's Algorithm**: Disables Nagle's Algorithm to reduce latency and improve network responsiveness.
3. **Disable Network Throttling**: Disables Windows' network throttling settings to ensure a smoother gaming experience.
4. **TCP Optimization**: Tweaks TCP settings for better network performance.
5. **Disable Quality of Service (QoS)**: Disables QoS reserved bandwidth to improve the gaming experience.
6. **Network Adapter Optimization**: Optimizes network adapters for maximum performance, including disabling power-saving features and optimizing packet handling.
7. **Eliminate Buffer Bloat**: Disables certain network optimizations that can introduce latency.
8. **Set Private Network**: Ensures your network is set to "Private" to avoid network discovery issues.
9. **DNS Cache Management**: Flushes DNS cache for faster name resolution.
10. **Fast Send Datagram**: Optimizes datagram thresholds to reduce packet delay.
11. **Prioritize Network Interface**: Sets Ethernet interface metric to prioritize gaming traffic.
12. **Set Custom Priority Control**: Customizes Windows' priority control for foreground tasks to enhance gaming performance.

### **Requirements**
- **Platform**: Windows 10 or later
- **Administrator Privileges**: The tool requires administrative privileges to modify system settings and registry values.
- **Dependencies**: 
  - `psutil` for network interface management.
  - `subprocess` for executing system commands.
  - `colorama` for terminal color output.

### **How to Use**
1. Download and extract the tool.
2. Run the tool as Administrator.
3. Follow the on-screen instructions to start the optimization process.
4. Once the tool completes, your system will be optimized for online gaming.

### **Important Notes**
- **Permission**: Ensure the script is run with administrator privileges to make the necessary changes to the system.
- **Backup**: It’s recommended to create a system restore point or backup before running this tool to ensure you can revert changes if needed.
- **Platform**: This tool is specifically designed for Windows users.

### **Commands Used**
- Registry modifications to optimize TCP/IP, network adapters, and gaming performance.
- PowerShell commands to disable specific features that can interfere with network performance (like QoS, buffer bloat, etc.).

### **Disclaimer**
This tool makes changes to your system's network and performance settings. While it aims to improve your online gaming experience, use it at your own risk. The developer is not responsible for any unintended consequences of using this tool. Always ensure you have a backup of your system before making changes.
