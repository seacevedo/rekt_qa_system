FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip sudo

RUN useradd -m seacevedo

RUN chown -R seacevedo:seacevedo /home/seacevedo/

COPY --chown=seacevedo . /home/seacevedo/app/

USER seacevedo

RUN pip3 install --upgrade pip

RUN cd /home/seacevedo/app/ && pip3 install -r requirements.txt

WORKDIR /home/seacevedo/app

EXPOSE 8501

CMD ["streamlit", "run", "/home/seacevedo/app/app.py"]
