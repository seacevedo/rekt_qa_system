FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip sudo

RUN useradd -m seacevedo

RUN chown -R seacevedo:seacevedo /home/seacevedo/

COPY --chown=seacevedo . /home/seacevedo/flows/

USER seacevedo

RUN pip3 install --upgrade pip

RUN cd /home/seacevedo/flows/ && pip3 install --no-cache-dir -r requirements.txt

WORKDIR /home/seacevedo/flows


CMD ["python3", "-c", "from prefect.cli import app; app()", "server", "start", "--host", "0.0.0.0"]

