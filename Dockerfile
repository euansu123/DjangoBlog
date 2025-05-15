FROM ubuntu:20.04
LABEL description="DjangoBlog Dockerfile"
# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# 安装编译工具和依赖
RUN apt-get update && \
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget vim python3-tk tk-dev && \
    mkdir -p /euansu/apps/Python/