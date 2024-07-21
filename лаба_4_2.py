#!/usr/bin/env python3

import subprocess
import re
import time
from datetime import datetime, timedelta
PCAP_FILE = "/etc/capture.pcap"
BLOCKED_IPS_FILE = '/etc/blocked_ips.txt'

# Конфигурация
BLOCK_TIME = 120  # Время блокировки в секундах (1 час)
BLOCK_MULTIPLIER = 2  # Множитель для увеличения срока блокировки
RECHECK_TIME = 7200  # Время повторной проверки в секундах (2 часа)
TCP_THRESHOLD = 100  # Пороговое количество TCP пакетов от одного IP за 2 минуты


# Функция для выполнения команд
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')


# Функция для сбора пакетов
def collect_packets():
    print("Сбор пакетов...")
    command = "tcpdump -c 1000 -w /etc/capture.pcap"
    run_command(command)


# Функция для анализа пакетов на сканирование портов
def detect_port_scans():
    print("Анализ пакетов на сканирование портов...")
    command = "tcpdump -r /etc/capture.pcap | grep 'Flags \[S\]'"
    output, _ = run_command(command)
    suspicious_ips = set()
    for line in output.split('\n'):
        match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)\.', line)
        if match:
            ip = match.group(1)
            suspicious_ips.add(ip)
    return suspicious_ips


# Функция для анализа TCP пакетов
def detect_tcp_flood():
    print("Анализ TCP пакетов...")
    command = "tcpdump -r /etc/capture.pcap 'tcp[tcpflags] & tcp-syn != 0'"
    output, _ = run_command(command)
    ip_count = {}
    for line in output.split('\n'):
        match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)\.', line)
        if match:
            ip = match.group(1)
            if ip in ip_count:
                ip_count[ip] += 1
            else:
                ip_count[ip] = 1

    suspicious_ips = {ip for ip, count in ip_count.items() if count >= TCP_THRESHOLD}
    command = f"tcpdump -nn -r {PCAP_FILE} | grep 'Flags \[S\]'"
    ip_ports = {}
    for line in output.split('\n'):
        match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)\.(\d+) > \d+\.\d+\.\d+\.\d+\.(\d+)', line)
        if match:
            ip = match.group(1)
            port = match.group(3)
            if ip in ip_ports:
                ip_ports[ip].add(port)
            else:
                ip_ports[ip] = {port}

    suspicious_ips += {ip for ip, ports in ip_ports.items() if len(ports) > TCP_THRESHOLD}

    def extract_ports_from_pcap(pcap_file):
        command = f"tcpdump -nn -r {pcap_file} 'tcp'"
        output, _ = run_command(command)
        ip_ports = {}
        for line in output.split('\n'):
            match = re.search(r'IP (\d+\.\d+\.\d+\.\d+)\.\d+ > (\d+\.\d+\.\d+\.\d+)\.(\d+)', line)
            if match:
                src_ip = match.group(1)
                dst_port = match.group(3)
                if src_ip not in ip_ports:
                    ip_ports[src_ip] = set()
                ip_ports[src_ip].add(dst_port)
        return ip_ports
    portsss = extract_ports_from_pcap(PCAP_FILE)
    with open('/etc/blocked_ip.txt', 'a') as f:
        for i in portsss:
            f.write(f"{i}n")
    return suspicious_ips


# # Функция для блокировки IP адресов
# def block_ip(ip, duration):
#     print(f"Блокировка IP {ip} на {duration} секунд")
#     unblock_time = datetime.now() + timedelta(seconds=duration)
#     command_check = f"sudo iptables -C INPUT -s {ip} -j DROP"
#     result, _ = run_command(command_check)
#     if "iptables: Bad rule" in result:
#         command = f"sudo iptables -A INPUT -s {ip} -j DROP"
#         run_command(command)
#         with open('/etc/blocked_ip.txt', 'a+') as f:
#             # Проверяем, есть ли уже такой IP в файле
#             if ip not in f.read():
#                 f.write(f"{ip}\t{unblock_time}\n")
#     return unblock_time
#
#
# Функция для разблокировки IP адресов
def unblock_ip():
    print("Разблокировка IP адресов...")
    with open('/etc/blocked_ip.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        ip, unblock_time_str = line.strip().split('\t')
        unblock_time = datetime.strptime(unblock_time_str, "%Y-%m-%d %H:%M:%S")
        with open('/etc/info.txt', 'w') as f:
            f.write(unblock_time)
        if datetime.now() > unblock_time:
            command = f"sudo iptables -D INPUT -s {ip} -j DROP"
            run_command(command)
            lines.remove(line)
    # Перезаписываем файл без разблокированных IP адресов
    with open('/etc/blocked_ip.txt', 'w') as f:
        f.writelines(lines)

def block_ip(ip, duration):
    print(f"Блокировка IP {ip} на {duration} секунд")
    unblock_time = datetime.now() + timedelta(seconds=duration)
    command = f"sudo iptables -A INPUT -s {ip} -j DROP"
    run_command(command)
    with open('/etc/blocked_ip.txt', 'a') as f:
        f.write(f"{ip}\t{unblock_time}\n")
    return unblock_time




# Основная функция
def main():
    # Сбор пакетов
    unblock_ip()
    collect_packets()

    # Анализ пакетов
    port_scan_ips = detect_port_scans()
    tcp_flood_ips = detect_tcp_flood()

    # Список для отслеживания заблокированных IP и времени разблокировки
    blocked_ips = {}

    def is_ip_blocked(ip):
        result = subprocess.run(["sudo", "iptables", "-L", "INPUT", "-v", "-n"], capture_output=True, text=True)
        return ip in result.stdout
    # Блокировка IP адресов
    for ip in port_scan_ips.union(tcp_flood_ips):
        if ip in blocked_ips:
            unblock_time, current_duration = blocked_ips[ip]
            if datetime.now() > unblock_time:
                # Увеличение срока блокировки при повторном нарушении
                new_duration = current_duration * BLOCK_MULTIPLIER
                unblock_time = block_ip(ip, new_duration)
                blocked_ips[ip] = (unblock_time, new_duration)
            else:
                print(f"IP {ip} уже заблокирован до {unblock_time}")
        elif not is_ip_blocked(ip):
            unblock_time = block_ip(ip, BLOCK_TIME)
            blocked_ips[ip] = (unblock_time, BLOCK_TIME)
    unblock_ip()



# Запуск основной функции
if __name__ == "__main__":
    main()
