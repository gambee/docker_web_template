FROM postgres:10.3

# PROJECT
# Database Container

# use build args in the docker-compose.yml file if behind proxy,
# must add proxies to the docker-compose file as well as the various
# Dockerfiles themselves, to resolve issues with configuring apt-get
ARG arg_APT_PROXY=''
RUN printf ''${arg_APT_PROXY:+'Acquire::http::Proxy "http://example-proxy.com:123";\nAcquire::https::Proxy "http://example-proxy.com.com:456";'} >> /etc/apt/apt.conf.d/70debconf

RUN apt-get update

# because debugging postgres with sed and no pager is just unnecessary
RUN apt-get install -y vim less

COPY . /docker-entrypoint-initdb.d

# because 
ENV PAGER="less -#.1 --chop-long-lines"
