这个项目是一个前后端不分离的blog项目

blog样式见：https://www.zmrenwu.com/
此blog代码也是学习上面教程写出来的。

我把它用来制作docker镜像学习使用，需要的自取，或非docker使用

# 使用docker部署项目

该项目的已经经过预准备：
- 划分settings
- 使用nginx+gunicorn成功访问该项目
    - nginx配置 
    ```
    server {
    charset utf-8;
    listen 80;
    server_name 127.0.0.1:80;
    # 代理静态文件
    location /static {
        alias /....../projects/tanblog/static;
    }
    # 博客代理主程序
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8080;
    }
    }
    ```
    - gunicorn启动命令，启动主程序
    `gunicorn tanblog.wsgi:application -w 2 -k gthread -b 0.0.0.0:8080`

`注：该项目settings里的数据库请修改成自己可用的`

---

- 配置Dockerfile

从0制作一个完整的tanblog镜像

```Dockerfile
# 基础镜像
FROM centos:centos7.5.1804
#ENV 设置环境变量
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

#RUN 执行以下命令
RUN curl -so /etc/yum.repos.d/Centos-7.repo http://mirrors.aliyun.com/repo/Centos-7.repo && rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
RUN yum install -y  python36 python3-devel gcc pcre-devel zlib-devel make net-tools nginx mariadb-devel

WORKDIR /app

COPY . /app

COPY ./k8s/production/nginx/tanblog.conf /etc/nginx/conf.d/

RUN pip3 install -r requirements.txt

RUN chmod +x run.sh

RUN rm -rf ~/.cache/pip
#EXPOSE 映射端口
EXPOSE 80

#容器启动时执行命令
CMD ["./run.sh"]

```
>EXPOSE 指令是声明运行时容器提供服务端口，这只是一个声明，在运行时并不会因为这个声明应用就会开启这个端口的服务。在 Dockerfile 中写入这样的声明有两个好处，一个是帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射；另一个用处则是在运行时使用随机端口映射时，也就是 docker run -P时，会自动随机映射 EXPOSE 的端口。


tanblog.conf

```nginx
server {
    listen 80;
    server_name  127.0.0.1:80;

    location /static {
        alias /app/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:8080;
    }
}
```

run.sh内容

```sh
#!/bin/sh
# default.conf会干扰80端口的配置，因此移除
mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak
# 启动nginx
nginx
# 执行迁移
python3 manage.py migrate
# 收集静态文件
python3 manage.py collectstatic --noinput
# 启动django服务
gunicorn tanblog.wsgi:application -w 2 -k gthread -b 0.0.0.0:8080 --chdir=/app
```

- 打包镜像
```sh
docker build -t tanblog:v1.0 -f k8s/production/Dockerfile .
# 等待打包完成，之后可以查看镜像
docker images
```
- 创建镜像容器并启动
```sh
docker run -itd --name tanblog2 -p 8080:80  tanblog:v1.0
# -it是以交互模式运行 -d是后台运行
# --name 容器的取名
# -p 主机端口:容器端口   容器端口映射出来 
#  tanblog:v1.0是制定的镜像
```

- 进入容器
```sh
docker exec -it tanblog bash
以伪终端交互模式进入容器
```

- 外部查看容器logs检查容器运行情况
```
docker logs 容器名
```

