SELECT table_name AS "Table", round(((data_length + index_length) / 1024 / 1024), 2) as sizeMB FROM information_schema.TABLES WHERE table_schema = "okmis_dev" ORDER BY sizeMB DESC;
