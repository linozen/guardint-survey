FROM python:3.9-slim-buster

RUN apt-get update && apt-get upgrade -y

RUN useradd --create-home --uid 9000 nonroot
USER nonroot

WORKDIR /home/nonroot/app
COPY --chown=nonroot:nonroot . .
RUN python3 -m pip install --user -r requirements.txt
ENV PATH="/home/nonroot/.local/bin:${PATH}"

EXPOSE 8501
CMD streamlit run app.py
