DROP TABLE IF EXISTS article;
DROP TYPE IF EXISTS ARTICLE_TYPE;
DROP TABLE IF EXISTS tag_product;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS site_user;

CREATE TYPE ARTICLE_TYPE AS ENUM ('ABOUT', 'CONTACT');

CREATE TABLE article(
   id SERIAL PRIMARY KEY,
   text TEXT,
   type ARTICLE_TYPE,
   date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
   last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'));

INSERT INTO article(id, text, type) VALUES
(1, 'this is about', 'ABOUT'),
(2, 'this is contact', 'CONTACT');

CREATE TABLE category(
   id SERIAL PRIMARY KEY,
   name VARCHAR(32) NOT NULL,
   icon VARCHAR(32),
   deleted BOOLEAN NOT NULL DEFAULT FALSE,
   date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
   last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'));

INSERT INTO category(id, name, icon) VALUES
(1, 'Kitchenware', 'account_balance'),
(2, 'Furniture', 'dashboard'),
(3, 'Light', 'attach_money');

CREATE TABLE tag(
   id SERIAL PRIMARY KEY,
   name VARCHAR(32) NOT NULL,
   deleted BOOLEAN NOT NULL DEFAULT FALSE,
   date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
   last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'));

INSERT INTO tag(id, name) VALUES
(1, 'OLD'),
(2, 'NEW'),
(3, 'FROM AUSTRALIA'),
(4, 'FROM AMERICA'),
(5, 'FROM CHINA');

CREATE TABLE product(
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    category_id INTEGER REFERENCES category(id));

INSERT INTO product(id, name, category_id) VALUES
(1, 'kitchenware1', 1),
(2, 'kitchenware2', 1),
(3, 'kitchenware3', 1),
(4, 'kitchenware4', 1),
(5, 'kitchenware5', 1),
(6, 'light1', 3),
(7, 'light2', 3),
(8, 'light3', 3),
(9, 'light4', 3),
(10, 'light5', 3),
(11, 'furniture1', 2),
(12, 'furniture2', 2),
(13, 'furniture3', 2),
(14, 'furniture4', 2),
(15, 'furniture5', 2);

CREATE TABLE tag_product(
    product_id INTEGER REFERENCES product(id),
    tag_id INTEGER REFERENCES tag(id),
    PRIMARY KEY (product_id, tag_id));

INSERT INTO tag_product(product_id, tag_id) VALUES
(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),
(9,2),(10,2),(11,2),(12,2),(13,2),(14,2),(15,2),
(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),
(8,4),(9,4),(10,4),(11,4),(12,5),(13,5),(14,5),(15,5);
