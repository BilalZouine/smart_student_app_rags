CREATE EXTENSION IF NOT EXISTS vector;
-- (Re)créer la table documents en 1536 dimensions
DROP TABLE IF EXISTS documents CASCADE;
CREATE TABLE documents (
id SERIAL PRIMARY KEY,
source TEXT,
chunk TEXT,
modality TEXT, -- "text" ou "image"
embedding VECTOR(1536) -- dim = text-embedding-3-small
);

