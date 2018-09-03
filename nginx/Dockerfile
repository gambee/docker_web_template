FROM nginx:1.13.10
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY PROJECT.conf /etc/nginx/conf.d/
