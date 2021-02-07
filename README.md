# abaqus_autorun

## 0.1.0

包含两个文件，先在`windows terminal`中运行`autorun.bat`开始计算，而后在`abaqus command`运行`abaqus cae noGUI=odb_to_data.py`的到结果

## 0.2.0

计算部分和提取数据全部由`python`脚本运行。打包成为`.exe`可执行文件，直接在`.inp`文件夹双击运行即可

## 0.3.0

增加了`Server酱`接口，方便在运行时提示完成，提高程序容错率

## 0.4.0

增加了流水线运行，对于一组分析只需要运行一次，程序会自动进入流水线



## TODO

1. 增加线程池，固定运行数量
2. 增加多文件的自动处理功能
3. 增加更多参数接口
4. 增加GUI界面
5. 改写`c++`