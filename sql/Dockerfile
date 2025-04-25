FROM rust:1.78.0 as diesel_base
RUN cargo install diesel_cli \
    --version 2.2.4 \
    --locked \
    --no-default-features \
    --features postgres

ARG MIGRATIONS_FOLDER=migrations
COPY ./${MIGRATIONS_FOLDER} ./migrations

FROM diesel_base as diesel_migrations
COPY local_migration.sh .
RUN chmod +x local_migration.sh
CMD ["./local_migration.sh"]