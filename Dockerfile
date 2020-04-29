FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
<<<<<<< HEAD
COPY ./ /code/
=======
COPY ./ /code/
>>>>>>> parent of b637295... Changed Docker's files
