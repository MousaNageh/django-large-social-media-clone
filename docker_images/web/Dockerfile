FROM python:3.12-alpine3.18

ENV SECRET_KEY='django-insecure-0(xjts_lck0lixxi5&*s5-5jwid-ab@nup5=^#$)2n-yz31sd6'

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --update --no-cache \
    postgresql-client \
    libmagic \
    libpng-dev \
    jpeg-dev \
    libwebp-dev \
    lcms2-dev \
    freetype-dev \
    libimagequant-dev \
    geos-dev \
    gdal-dev \
    bash && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    gcc musl-dev \
    python3-dev \
    libffi-dev \
    postgresql \
    ca-certificates \
    build-base  \
    postgresql-dev \
    zlib \
    zlib-dev \
    libpq-dev \
    libpq \
    coreutils \
    dpkg-dev dpkg \
    make \
    openssl-dev \
    linux-headers && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    apk del .tmp-build-deps

ENV PATH="/py/bin:$PATH"

COPY . /app

EXPOSE 6060
