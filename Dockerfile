FROM node:15 AS webpack

WORKDIR /usr/src/app/frontend

COPY frontend/package.json .
COPY frontend/package-lock.json .
RUN npm ci

COPY frontend/.babelrc .
COPY frontend/webpack.config.js .
COPY frontend/src src
RUN npm run dev


FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY --from=webpack /usr/src/app/frontend/static frontend/static
COPY . .

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn -b 0.0.0.0:5003 radiodns.wsgi" ]