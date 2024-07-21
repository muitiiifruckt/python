import subprocess
import time
import wmi
from collections import defaultdict
from scapy.all import sniff, rdpcap, IP, TCP

# Константы для блокировки
BLOCK_DURATION = 3600  # X часов в секундах (например, 1 час)
RECHECK_DURATION = 7200  # Y часов в секундах (например, 2 часа)
SCAN_THRESHOLD = 100  # Минимальное количество пакетов для блокировки
PACKET_CAPTURE_COUNT = 1000  # Количество пакетов для захвата

# Словарь для хранения времени блокировки IP адресов
blocked_ips = defaultdict(int)


def capture_packets():
    capture_file = "capture.pcap"
    tcpdump_command = ['npcap', '-c', str(PACKET_CAPTURE_COUNT), '-w', capture_file]
    try:
        print(f"Capturing {PACKET_CAPTURE_COUNT} packets...")
        subprocess.run(tcpdump_command, check=True)
        print("Packet capture complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error during packet capture: {e}")
    return capture_file


def analyze_packets(capture_file):
    suspicious_ips = defaultdict(int)
    packets = rdpcap(capture_file)
    for packet in packets:
        if IP in packet and TCP in packet:
            ip_src = packet[IP].src
            if packet[TCP].flags == 'S':  # SYN flag indicates TCP connection initiation
                suspicious_ips[ip_src] += 1
    return suspicious_ips


def detect_port_scanning(capture_file):
    try:
        result = subprocess.run(['nmap', '-sV', '-O', '-oX', '-', capture_file], capture_output=True, text=True)
        scanned_ips = [line.split()[4] for line in result.stdout.split('\n') if "Host" in line]
        return scanned_ips
    except subprocess.CalledProcessError as e:
        print(f"Error during nmap scan: {e}")
        return []


def block_ip(ip, duration):
    wmi_service = wmi.WMI(namespace='root\\StandardCimv2')
    firewall_rule = wmi_service.MSFT_NetFirewallRule.create(
        DisplayName=f"BlockIP_{ip}",
        Direction=1,  # Inbound
        Action=2,  # Block
        LocalAddress='Any',
        RemoteAddress=ip,
        Enabled=True,
        Profile=1  # Public profile
    )
    blocked_ips[ip] = time.time() + duration
    print(f"Blocked IP {ip} for {duration // 3600} hours.")


def unblock_ip(ip):
    wmi_service = wmi.WMI(namespace='root\\StandardCimv2')
    rules = wmi_service.MSFT_NetFirewallRule(RemoteAddress=ip)
    for rule in rules:
        rule.Delete_()
    if ip in blocked_ips:
        del blocked_ips[ip]
    print(f"Unblocked IP {ip}.")


def main():
    capture_file = capture_packets()
    suspicious_ips = analyze_packets(capture_file)
    scanned_ips = detect_port_scanning(capture_file)

    current_time = time.time()

    # Обработка IP адресов, заподозренных в сканировании портов или отправке большого количества пакетов
    for ip, count in suspicious_ips.items():
        if count >= SCAN_THRESHOLD:
            if ip in blocked_ips and current_time < blocked_ips[ip]:
                new_duration = 2 * (blocked_ips[ip] - current_time)
                block_ip(ip, new_duration)
            else:
                block_ip(ip, BLOCK_DURATION)

    for ip in scanned_ips:
        if ip in blocked_ips and current_time < blocked_ips[ip]:
            new_duration = 2 * (blocked_ips[ip] - current_time)
            block_ip(ip, new_duration)
        else:
            block_ip(ip, BLOCK_DURATION)

    # Разблокировка IP адресов по истечении времени блокировки
    for ip in list(blocked_ips):
        if current_time >= blocked_ips[ip]:
            unblock_ip(ip)


if __name__ == "__main__":
    main()
