##### BUILDING STAGE #####
FROM node:18 as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
COPY bundles-src ./bundles-src

RUN npm ci --include=dev
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"


##### RELEASE STAGE #####
FROM node:18-alpine

WORKDIR /home/burger/web

COPY --from=build /usr/src/app/bundles ./bundles
COPY --from=build /usr/src/app/node_modules/ ./node_modules
