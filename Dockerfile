# docker build -t katalog_py .
# docker run -it --rm -p 8080:8080  --mount type=bind,source="$(pwd)"/app,target=/app katalog_py
# docker run -dt -p 8080:8080  --mount type=bind,source="$(pwd)"/app,target=/app --name katalog_py_instance katalog_py

FROM continuumio/anaconda:latest
MAINTAINER hellsurfer
RUN pip install TurboGears2
RUN pip install kajiki
EXPOSE 8080/tcp
VOLUME /app
WORKDIR /app
ENTRYPOINT python ./main.py
