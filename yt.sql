CREATE TABLE yt_file (
	yt_file SERIAL PRIMARY KEY NOT NULL,
	url VARCHAR NOT NULL,
	status VARCHAR NOT NULL DEFAULT 'Queued'
);
