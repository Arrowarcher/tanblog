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