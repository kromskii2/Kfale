import os
from ftplib import FTP
import configparser

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    folder_path = config['DEFAULT']['folder_path']
    return folder_path

def write_config(folder_path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'folder_path': folder_path}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def read_ftp_config():
    config = configparser.ConfigParser()
    config.read('ftp.ini')
    ftp_info = {
        'host': config['DEFAULT']['host'],
        'username': config['DEFAULT']['username'],
        'password': config['DEFAULT']['password']
    }
    return ftp_info

def write_ftp_config(host, username, password):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'host': host, 'username': username, 'password': password}
    with open('ftp.ini', 'w') as configfile:
        config.write(configfile)

def upload_file_ftp(file_path, ftp_info):
    with FTP(ftp_info['host']) as ftp:
        ftp.login(ftp_info['username'], ftp_info['password'])
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {os.path.basename(file_path)}', file)

def main():
    folder_path = input("Введите путь к папке для взаимодействия со скриптом: ")
    write_config(folder_path)

    host = input("Введите IP адрес FTP сервера: ")
    username = input("Введите логин для FTP сервера: ")
    password = input("Введите пароль для FTP сервера: ")
    write_ftp_config(host, username, password)

    folder_path = read_config()
    ftp_info = read_ftp_config()

    while True:
        file_name = input("Введите имя файла для копирования на FTP сервер (или 'exit' для выхода): ")
        if file_name.lower() == 'exit':
            break

        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            upload_file_ftp(file_path, ftp_info)
            print("Файл успешно загружен на FTP сервер.")
            # После успешной загрузки файла на FTP сервер можно удалить оригинальный файл.
            os.remove(file_path)
            print("Оригинальный файл удален.")
        else:
            print("Файл не найден.")

if __name__ == "__main__":
    main()
