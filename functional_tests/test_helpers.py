import os
import shutil
import subprocess
import psutil


def create_and_set_working_dir(new_dir):
    if os.path.exists(new_dir):
        shutil.rmtree(new_dir)
    os.makedirs(new_dir)
    os.chdir(new_dir)


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return ''.join(iter(p.stdout.readline, b''))


def stop_running_wiremocks():
    for proc in psutil.process_iter():
        try:
            pcmd = proc.cmdline()
            if pcmd[2] and pcmd[2].find("wiremock") >= 0:
                proc.terminate()
        except:
            pass


def count_running_wiremocks():
    count = 0
    for proc in psutil.process_iter():
        try:
            pcmd = proc.cmdline()
            if pcmd[2] and pcmd[2].find("wiremock") >= 0:
                count += 1
        except:
            pass
    return count


def print_file(path):
    with open(path, 'r') as log_file:
        for line in log_file:
            print(line)


def make_service_dir(api, version):
    api_dir = os.path.join('services', api, version)
    os.makedirs(api_dir)

def assert_equal(expected, actual):
    if not expected == actual:
        raise AssertionError('Expected result:\n {}\n Not equal to actual: \n{}\n'.format(expected, actual))

