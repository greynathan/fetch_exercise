FROM python:3.9.2
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8050
ENTRYPOINT ["python"]
CMD [ "app.py" ]