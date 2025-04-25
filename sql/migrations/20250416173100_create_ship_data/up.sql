CREATE TABLE ships (
    device_id VARCHAR NOT NULL,
    datetime TIMESTAMP NOT NULL,
    address_ip VARCHAR NOT NULL,
    address_port INTEGER NOT NULL,
    original_message_id VARCHAR NOT NULL,
    CONSTRAINT ships_pk PRIMARY KEY (device_id, original_message_id),
    raw_message JSONB NOT NULL
);

CREATE INDEX idx_ship_datetime ON ships USING BTREE (datetime);
CREATE INDEX idx_ship_device_id ON ships USING BTREE (device_id);
CREATE INDEX idx_ship_original_message_id ON ships USING BTREE (original_message_id);
