FROM python:3.10

# Create directories and copy over
RUN mkdir /project
WORKDIR /project
COPY ./requirements.txt ./
COPY fcfb/. /fcfb/
RUN mkdir /fcfb/graphics/scorebugs

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev
RUN pip install -r requirements.txt
ADD fcfb/main/porygon_bot.py /

# Run
CMD [ "python", "/fcfb/main/porygon_bot.py" ]