FROM nginx:1.17-alpine 
RUN rm /etc/nginx/conf.d/default.conf 
RUN mkdir /etc/nginx/sites-enabled
#RUN mkdir /var/nginx/cache
COPY nginx.conf /etc/nginx/conf.d 
COPY nginx.conf /etc/nginx/sites-enabled
