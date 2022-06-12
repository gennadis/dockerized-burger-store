##### BUILDING STAGE #####
FROM python:3.9-alpine as build

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add `pillow` and `psycopg2` dependencies
RUN apk --no-cache add \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


##### RELEASE STAGE #####
FROM python:3.9-alpine

RUN mkdir -p /home/burger
RUN addgroup -S burger && adduser -S burger -G burger

ENV HOME=/home/burger
ENV APP_HOME=/home/burger/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

RUN apk --no-cache add libpq libjpeg
COPY --from=build /usr/src/app/wheels /wheels
COPY --from=build /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh

COPY . $APP_HOME

RUN chown -R burger:burger $APP_HOME
USER burger

ENTRYPOINT ["/home/burger/web/entrypoint.sh"]
