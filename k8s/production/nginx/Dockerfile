FROM nginx:1.17.1

# 替换为国内源
# RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
# COPY ./compose/production/nginx/sources.list /etc/apt/
# RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx
# 更新系统并安装 certbot 用于配置 https 证书
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/tanblog.conf /etc/nginx/conf.d/tanblog.conf