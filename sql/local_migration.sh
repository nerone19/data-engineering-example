#!/bin/sh

export DATABASE_URL=$DATABASE_URL
diesel setup && diesel migration run