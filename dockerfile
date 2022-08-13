FROM python:3.9.2
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 5150
ENTRYPOINT ["python"]
CMD [ "app.py" ]