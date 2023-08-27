FROM python:3.11.4-bookworm

WORKDIR /app

COPY app/ /app

RUN pip3 install dash
RUN pip3 install pandas
RUN pip3 install dash_bootstrap_components
RUN pip3 install scikit-learn
RUN pip3 install xgboost

EXPOSE 8050

CMD ["python", "main.py"]
