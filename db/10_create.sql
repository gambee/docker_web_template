/* schema.pgsql
 * 
 * Description: This is the Database Schema for PROJECT
 */


/* The following command is commented out, because one database is already
 * created as part of the build process, and the name of this database is
 * determined by the 'POSTGRES_DB' variable defined in the .env file
 */
--CREATE DATABASE dbname;
\c dbname;

CREATE TABLE IF NOT EXISTS Example (
    PKID            serial UNIQUE PRIMARY KEY,
    Data            text
);
