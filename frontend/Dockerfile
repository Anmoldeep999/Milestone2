FROM alpine:3.20


RUN apk add --no-cache lighttpd


COPY index.html /var/www/localhost/htdocs/index.html


RUN sed -i 's#server.document-root = ".*"#server.document-root = "/var/www/localhost/htdocs"#' /etc/lighttpd/lighttpd.conf

EXPOSE 80

CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
