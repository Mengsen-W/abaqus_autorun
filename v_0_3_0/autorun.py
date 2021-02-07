# -*- coding: utf-8 -*-
""" autorun in abaqus job
@Author: Mengsen.Wang
@Last Modified time: 2021-02-05 09:55:57
"""
import os
import requests
import psutil

META_STR = """
import job
import sys
from odbAccess import *
from visualization import *
from abaqusConstants import *
from abaqus import *

input_file = '{}'
parall_num = {}

job_name = input_file[0:-4]
mdb.JobFromInputFile(name=job_name, inputFileName=input_file,
                     numCpus=parall_num, numDomains=parall_num)
mdb.jobs[job_name].submit()
mdb.jobs[job_name].waitForCompletion()

odb_name = '{{}}.odb'.format(job_name)
step_name = 'Step-2'
set_name = 'RP-1'
outfile_name = '{{}}.txt'.format(job_name)

# get odb name
odb = openOdb(odb_name)
# outfile
f = open(outfile_name, 'w')
myAssembly = odb.rootAssembly
# step name
frameRepository = odb.steps[step_name].frames
# set name
RefPointSet = myAssembly.nodeSets[set_name]
for i in range(len(frameRepository)):
    # [0]--x [1]--y [2]--z
    # extract set_name in directory force
    RForce = frameRepository[i].fieldOutputs['RF']
    RefPointRForce = RForce.getSubset(region=RefPointSet)
    RForceValues = RefPointRForce.values
    RF_x = RForceValues[0].data[0]
    # extract set_name in directory displace
    displacement = frameRepository[i].fieldOutputs['U']
    RefPointDisp = displacement.getSubset(region=RefPointSet)
    DispValue = RefPointDisp.values
    Disp_x = DispValue[0].data[0]
    # write file
    Disp_data = '\\t' + '\\t' + str(Disp_x)
    Force_data = '\\t' + '\\t' + str(RF_x)
    Disp = str(Disp_data)
    RF = str(Force_data)
    f.write(Disp)
    f.write(RF)
    f.write('\\n')
sys.exit(0)
"""


def send_message(title, body=None):
    """send message to wechat interface
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 10:02:49
    """
    key = "SCU78414T0b1a7165fe765d2090c77ae576019f87601be1c76609b"
    url = "https://sc.ftqq.com/{}.send".format(key)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    payload = {"text": "{}".format(title), "desp": "{}".format(body)}
    result = requests.post(url, params=payload, headers=headers)
    return result


def find_inp() -> (str, str, str):
    """ find this directory inp file
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 09:59:20
    """
    os_walk = os.walk(os.getcwd())
    for path, _dir_list, file_list in os_walk:
        for file_name in file_list:
            if file_name.split(".")[-1] == "inp":
                return (path, os.path.join(path, file_name), file_name, file_name[0:-4])
    send_message("find_inp()", "NoFileExistsError")
    return (None, None, None, None)


def cmd_exec(abs_path):
    """cmd execute this is the main logic
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 10:00:37
    """
    error = os.system(
        'cd /d {} && abaqus cae noGUI=temp.py && echo "finish jobs" && echo.'.format(
            abs_path
        )
    )
    if (error >> 8) != 0:
        send_message("cmd_exec_error", str(error >> 8))


def write_py(main_file_name, abs_path):
    """write temp python for called by cmd_exec()
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 10:01:40
    """
    with open("{}\\temp.py".format(abs_path), "w") as temp_python:
        temp_python.write(META_STR.format(
            main_file_name, psutil.cpu_count(False)))


def clean(abs_path):
    """clean temp python
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 10:02:17
    """
    try:
        os.remove("{}\\temp.py".format(abs_path))
    except OSError:
        send_message("clean error", "OSError")


def main():
    """main entry
    @Author: Mengsen Wang
    @Last Modified time: 2021-02-05 10:08:49
    """
    abs_path, abs_file_path, main_file_name, job_name = find_inp()
    print(abs_path, abs_file_path, main_file_name, job_name)
    send_message("{} begin".format(job_name))
    write_py(main_file_name, abs_path)
    print("write temp py")
    cmd_exec(abs_path)
    clean(abs_path)
    send_message("{} finish".format(job_name))


if __name__ == "__main__":
    main()

# send_message("hello world", "Hello server")
# os.system('mkdir {}'.format(main_name))
# os.system('move {} {}'.format(file_name, main_name))
# os.system("echo '%~f0'  | cmd")
# os.system("mkdir test")
# os.system('echo "hello world"')
# @echo off
# setlocal
# set ABA_COMMAND=%~nx0
# set ABA_COMMAND_FULL=%~f0
# "C:\SIMULIA\CAE\2019\win_b64\code\bin\ABQLauncher.exe" %*
# endlocal
