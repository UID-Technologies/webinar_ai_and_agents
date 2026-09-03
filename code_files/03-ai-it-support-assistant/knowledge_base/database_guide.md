# Production Database Guide

The Order API connects to the production MySQL database.

Production database configuration:

Host: mysql.internal
Port: 3306
Database: orders

Applications running in production must use:

DB_HOST=mysql.internal
DB_PORT=3306
