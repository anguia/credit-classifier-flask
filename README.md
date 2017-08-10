# credit-classifier-flask
## 目录及文件说明：
1.	App为整个应用根目录，uwsgi.ini为UWSGI的配置文件；
2.	Credit.py为python web service的文件，实现用户信息录入、数据处理、调用模型服务进行预测以及预测结果展示等功能；
3.	Static目录定义了UI展示的HTML文件；
4.	TF目录主要实现后端模型服务及数据处理等功能；
5.	MODEL目录，为训练模型保存和恢复目录；
6.	Requirements.txt文件，定义了运行环境依赖库；
7.	TF目录下，test.txt, newTest.csv文件，前者为原始用户信用数据。后者为处理后的数据；
8.	TF目录下clientCredit.py实现模型恢复，以及更加输入参数进行信用预测功能；

## 运行环境说明：
1.	基础镜像库为ubuntu16.10
2.	前端运行环境要求：flask, wtforms, nginx, uwsgi, supervisor(使用python开发的c/s进程管理工具，非必须)；
3.	后端Tensorflow环境要求：scipy, numpy, sklearn, tensorflow；
4.	端口说明，容器内采用80端口；
5.	信用分类路由及功能：
a)	/credit: 用户信用数据录入；
b)	/classifier:用户数据处理和展示，并根据用户录入数据进行信用分类预测；
c)	/predict:用户信用预测结果展示，包含两部分，单条记录分类预测。根据最后100条记录对模型的评估；
## 部署说明
1.	部署本地Docker环境；
2.	git clone git@github.com:anguia/credit-classifier-flask.git
3.	cd credit-classifier-flask
4.	构建docker镜像，docker build –t docker-credit-flask .
5.	创建docker实例，docker run –it –p 10081:80 docker-credit-flask
6.	访问应用 http://local:10081/credit
