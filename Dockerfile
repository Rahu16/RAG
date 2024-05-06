FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

#VOLUME ["/tmp"] ["/tmp"]

# VOLUME ["/slash_tmp"]

ADD requirements.txt .

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

COPY . .
CMD ["python3", "main.py"]