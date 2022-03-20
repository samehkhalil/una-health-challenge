# Una Health Code Challenge

## Assumptions

Due to the nature of the challenge, I Have made some assumptions, in a real world scenario, access to product owner and other teams is available to clear out each assumption.

- The main value to record in a reading, csv file data rows, is "Glukosewert-Verlauf mg/dL" / Glucose Value, if non existant in a record, it will be discarded.
- data in date time field has no timezone data, timezones are ignored by setting USE_TZ to False

## Improvements

Due the time constraints some improvements could be added to the codebase

- More Testing
- Post endpoint would accept a file and load it to database instead of reading sample files.
- Remove unused Django apps, static files, messages...etc

## Running the app

- Clone the repo
- Run with docker compose

```
docker compose up
```

- Visit /api/v1/prepopulate/ with A POST to populate the data

- Run tests

```
python manage.py test
```
