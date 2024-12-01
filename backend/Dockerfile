FROM python:3.12

WORKDIR /backend
#ROZBUDIWAĆ CAŁOŚĆ // TO JEST TYLKO ŻEBY COKOLWIEK BYŁO!!!
COPY /requirements.txt ./

RUN pip install -r /requirements.txt

EXPOSE 8000

COPY ./backend .

CMD [ "python3", "http-con.py" ]