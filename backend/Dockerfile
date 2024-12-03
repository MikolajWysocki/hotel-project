FROM python:3.12

WORKDIR /backend
#ROZBUDIWAĆ CAŁOŚĆ // TO JEST TYLKO ŻEBY COKOLWIEK BYŁO!!!
COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 9000

CMD [ "python3", "http-con.py" ]