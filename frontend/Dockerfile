FROM nginx:alpine

RUN printf 'server {\n    listen 3000;\n    location / {\n        root /usr/share/nginx/html;\n        index index.html;\n    }\n}\n' > /etc/nginx/conf.d/default.conf

COPY . /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
