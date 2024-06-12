FROM python:3.10

# Create app directory
WORKDIR scoring_system

# Install app dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . ./

CMD [ "pytest", "--cov-report", "term", "--cov=.", "test_scoring.py" ]