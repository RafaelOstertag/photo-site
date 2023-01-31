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


def _ensure_schema(db):
    if _user_version(db) == 0:
        _version0(db)
