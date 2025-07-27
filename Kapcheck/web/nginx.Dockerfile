# nginx.Dockerfile
FROM nginx:alpine

# Копировать кастомный конфиг внутрь образа (если не используешь volume)
# COPY ./nginx.conf /etc/nginx/conf.d/default.conf
