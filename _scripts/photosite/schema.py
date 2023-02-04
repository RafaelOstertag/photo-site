def _user_version(db):
    return db.execute("pragma user_version").fetchall()[0][0]


def _version0(db):
    with db:
        db.execute(
            """
        CREATE TABLE photo(
            id INTEGER PRIMARY KEY ASC,
            image_path VARCHAR(1024) NOT NULL UNIQUE,
            image_modified REAL NOT NULL,
            created REAL,
            aperture VARCHAR(32),
            exposure VARCHAR(32),
            iso VARCHAR(32),
            lens VARCHAR(128),
            focal_length VARCHAR(32),
            tags VARCHAR(1024)
        );
        
        PRAGMA user_version=1;
        """
        )

def _version1(db):
    with db:
        db.execute(
            """
        ALTER TABLE photo ADD body_serial VARCHAR(32);
        ALTER TABLE photo ADD lens_serial VARCHAR(32);
        ALTER TABLE photo ADD reindex INTEGER NOT NULL DEFAULT 0;

        UPDATE photo SET reindex = 1;

        CREATE INDEX body_serial_idx ON photo (body_serial);
        CREATE INDEX lens_serial_idx ON photo (lens_serial);
        
        PRAGMA user_version=2;
        """
        )


def _ensure_schema(db):
    if _user_version(db) == 0:
        _version0(db)
    if _user_version(db) == 1:
        _version1(db)
