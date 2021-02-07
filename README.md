# abaqus_autorun

## 0.1.0

包含两个文件，先在`windows terminal`中运行`autorun.bat`开始计算，而后在`abaqus command`运行`abaqus cae noGUI=odb_to_data.py`的到结果

## 0.2.0

计算部分和提取数据全部由`python`脚本运行。打包成为`.exe`可执行文件，直接在`.inp`文件夹双击运行即可

## 0.3.0

增加了`Server酱`接口，方便在运行时提示完成，提高程序容错率