# 第9天学生项目：机器学习零基础数据准备

## 运行方法

```bash
python -m pip install -r requirements.txt
python validate_day09_environment.py
jupyter lab
```

打开`notebooks/day09_ml_preparation_student.ipynb`。Notebook已经提供完整处理骨架，你只需完成少量关键填空、运行检查点并撰写解释。

## 学生信息

- 姓名：袁艳
- 学号：24040083
- 班级：信计2班

## 用自己的话回答

- 什么是特征，什么是标签：特征是模型用来做判断的依据或信息，标签是我们希望模型预测的答案，在这个任务中，标签是 Churn（是否流失），0表示未流失，1表示流失。
- 为什么要保留测试集：因为测试集可以检验模型，检验模型的普遍适用性，从而测试模型是否有效。
- 为什么83%准确率仍可能没有用：因为它的流失召回率为0，
