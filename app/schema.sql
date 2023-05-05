CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    mod INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS manga (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    banner TEXT,
    cover TEXT,
    type TEXT,
    author TEXT,
    release_date DATE,
    status TEXT,
    gender TEXT,
    last_chapter INTEGER DEFAULT 0,
    note DECIMAL DEFAULT 0,
    views INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS chapitre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    numero INTEGER NOT NULL,
    visible BOOLEAN NOT NULL,
    manga_id INTEGER NOT NULL,
    FOREIGN KEY (manga_id) REFERENCES manga (id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    chapter_id INTEGER NOT NULL,
    manga_id,
    date DATE NOT NULL,
    FOREIGN KEY (chapter_id) REFERENCES chapitre (id),
    FOREIGN KEY (manga_id) REFERENCES manga (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS gender (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO gender (name) VALUES
    ('4-koma'),
    ('Action'),
    ('Adulte'),
    ('Amitié'),
    ('Amour'),
    ('Animation'),
    ('Arts Martiaux'),
    ('Aventure'),
    ('Boxe'),
    ('Combat'),
    ('Comédie'),
    ('Crime'),
    ('Cybernétique'),
    ('Démons'),
    ('Doujinshi'),
    ('Drame'),
    ('E-sport'),
    ('Ecchi'),
    ('Espionnage'),
    ('Famille'),
    ('Fantaisie'),
    ('Fantastique'),
    ('Gender Bender'),
    ('Guerre'),
    ('Harcèlement'),
    ('Harem'),
    ('Hentai'),
    ('Historique'),
    ('Horreur'),
    ('Isekaï'),
    ('Jeux vidéo'),
    ('Josei'),
    ('Magical Girls'),
    ('Magie'),
    ('Mature'),
    ('Mecha'),
    ('Monstres'),
    ('Mystère'),
    ('One Shot'),
    ('Organisation secrète'),
    ('Parodie'),
    ('Policier'),
    ('Psychologique'),
    ('Realité Virtuel'),
    ('Réincarnation'),
    ('Returner'),
    ('Romance'),
    ('Science-fiction'),
    ('Seinen'),
    ('Shôjo'),
    ('Shôjo Ai'),
    ('Shonen'),
    ('Shônen Ai'),
    ('Smut'),
    ('Sport'),
    ('Sports'),
    ('Steampunk'),
    ('Super héros'),
    ('Surnaturel'),
    ('Technologie'),
    ('Tournoi'),
    ('Tragédie'),
    ('Tranches de vie'),
    ('Vampires'),
    ('Vie scolaire'),
    ('Virtuel world'),
    ('Webtoons'),
    ('Yaoi'),
    ('Yuri')
WHERE EXISTS (SELECT 1 FROM gender);