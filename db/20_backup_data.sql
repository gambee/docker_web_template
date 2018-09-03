/* import backup data, and reset counters for the pkid sequences */

\c dbname;

-- example
\copy example from '/docker-entrypoint-initdb.d/backups/example.csv' with (format csv);
-- select so that the output os the setval function is logged in docker-compose logs db
select setval('example_pkid_seq', (select max(pkid) from example), true)
    as example_pkid_after_csv;
