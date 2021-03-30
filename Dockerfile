FROM cccs/assemblyline-v4-service-base:latest

ENV SERVICE_PATH steg_finder.StegFinder

USER root

RUN mkdir -p /usr/share/man/man1
RUN apt update
RUN apt install -y git default-jre-headless
RUN git clone https://github.com/b3dk7/StegExpose.git

USER assemblyline

WORKDIR /opt/al_service
COPY . .

ARG version=4.0.0.dev1
USER root
RUN sed -i -e "s/\$SERVICE_TAG/$version/g" service_manifest.yml

USER assemblyline