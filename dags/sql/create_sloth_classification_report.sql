CREATE TABLE IF NOT EXISTS sloth_classification_report (
    classification_id SERIAL PRIMARY KEY,
    model_datetime VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    classification_param VARCHAR NOT NULL,
    precision NUMERIC NOT NULL,
    recall NUMERIC NOT NULL,
    f1score NUMERIC NOT NULL,
    support NUMERIC NOT NULL
);