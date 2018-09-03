from sqlalchemy.dialects.postgresql import TEXT, TIMESTAMP, INTEGER, BIGINT
from sqlalchemy.dialects.postgresql import REAL, TSVECTOR
from sqlalchemy import create_engine, Table, Column, ForeignKey, func
from sqlalchemy.schema import MetaData
import datetime
import re


def connect(user, passwd):
    # Establish a connection with the postgres database (we do this a lot)
    # format takes 6 args: (dilect+driver, user, passwd, host, port, database)
    postgres_url = '{}://{}:{}@{}:{}/{}'
    url = postgres_url.format('postgresql',
                              user,
                              passwd,
                              'db',
                              '5432',
                              'dbname')

    engine = create_engine(url)
    conn = engine.connect()
    # metadata needed at runtime to build ORM tables
    metadata = MetaData(bind=engine)
    return (conn, metadata)


def upsert(conn, table, records, uniqcol):
    # Implements SQL Upsert (because no native support exists in postgres)
    # This logic chooses between UPDATE and INSERT depending on the existence
    # of the records in question.
    # Arguments:
    #   table - sqlalchemy 'Table()' object
    #   records - list of dicts (or dict like) repesentations of rows to upsert
    #   uniqcol - string/key to upsert on (UPDATE where ... exists? etc.)

    existing = {  # query for existing records
                    record[uniqcol]
                    for record in conn.execute(
                            table.select().where(
                                table.c[uniqcol].in_({
                                            r[uniqcol]
                                            for r in records
                                        })))
                }
    updates = [  # Build a list of records that are UPDATEs
                record
                for record in records
                if record[uniqcol] in existing
              ]
    # The remaining records are new, and must be INSERTed
    inserts = [  # Build a list of records that are INSERTs
                record
                for record in records
                if record[uniqcol] not in existing
              ]

    # execute the INSERTions
    if(len(inserts) > 0):
        conn.execute(table.insert(), inserts)
    # execute the UPDATEs
    # (NOTE: must be done individually due to the uniqcol in the where clause)
    for record in updates:
        key = record[uniqcol]  # save the uniqcol to UPDATE on
        del record[uniqcol]  # then delete it from dict, (or postgres whines)
        conn.execute(table.update().where(table.c[uniqcol] == key), record)


class PROJECT_Tables:
    # This is a wrapper class object that encapsulates all of the ORM
    # information and access for the tables in the postgres database.
    # All interractions between python and postgresql should happen
    # via this class interface (unless you want to reinvent the wheel,
    # and all of the debugging and errors that come along with that).
    def __init__(self, user, passwd):
        (self.conn, self.metadata) = connect(user, passwd)
        # sql execution function (save here for conciseness)
        self.execute = self.conn.execute

        # Build the actual ORM table objects
        # NOTE: this is done via these functions becuase the metadata is
        # needed at runtime, and the ORM definitions can become quite long.
        # This makes it easier to read the class interface definition. See
        # below for the ORM defintion functions.

        self.example_table = mktab_example(self.metadata)

        # NOTE: if you want to be able to refer to tables like
        # PROJECT_Tables.member (or any table name), then you must add it
        # to the below list comprehension, so that it will be added to the
        # __getitem__ method
        self.tbls = dict([  # This is used by __getitem__
                            (x.name, x)
                            for x in [self.member_table, self.activity_table]
                        ])

    def __getitem__(self, key):
        # this allows us to reference tables by their 'name'
        return self.tbls[key] if key in self.tbls else None


def mktab_member(metadata):
        return Table(
            'example',
            metadata,
            Column('pkid', INTEGER,  primary_key=True),
            Column('data', TEXT))
