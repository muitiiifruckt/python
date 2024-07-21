#!/usr/bin/env python3

import subprocess
from datetime import datetime

# Функция для выполнения команд
def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')

# Функция для разблокировки IP адресов
def unblock_ip(ip):
    print(f"Разблокировка IP {ip}")
    command = f"sudo iptables -D INPUT -s {ip} -j DROP"
    run_command(command)

# Чтение и обновление файла /etc/blocked_ip.txt
def update_blocked_ips(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_time = datetime.now()
    updated_lines = []

    for line in lines:
        ip, unblock_time_str = line.strip().split('\t')
        unblock_time = datetime.strptime(unblock_time_str, '%Y-%m-%d %H:%M:%S.%f')

        if current_time >= unblock_time:
            # Время разблокировки прошло, разблокируем IP
            unblock_ip(ip)
        else:
            # Время разблокировки не прошло, оставляем запись в файле
            updated_lines.append(line)

    # Обновление файла
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

# Путь к файлу с заблокированными IP
file_path = '/etc/blocked_ip.txt'

# Обновление списка заблокированных IP
update_blocked_ips(file_path)
