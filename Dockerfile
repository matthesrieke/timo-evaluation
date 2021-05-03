FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

RUN python -m ipykernel install --user

ADD ./jupyter/Timo-Evaluation.ipynb /home/jovyan/allprojects.ipynb
ADD ./jupyter/Timo-Leistungsnachweis.ipynb /home/jovyan/performance_record.ipynb

# ENV STATIC_URL /static
# ENV STATIC_PATH /var/www/app/static

COPY ./server /app/
# COPY uwsgi.ini /server/
# COPY app/__init__.py /server/app/
# COPY app/views.py /server/app/
