FROM python:3.9-slim-buster

RUN apt-get update && apt-get upgrade -y

RUN useradd --create-home --uid 9000 nonroot
USER nonroot

WORKDIR /home/nonroot/app
COPY --chown=nonroot:nonroot . .
ENV PATH="/home/nonroot/.local/bin:${PATH}"
RUN python3 -m pip install --user pipenv
RUN pipenv install

EXPOSE 8501
CMD pipenv run streamlit run explorer/all.py
