-- Создайте базу данных, если она ещё не создана
CREATE DATABASE ugc;

-- Подключитесь к вашей базе данных
\c ugc

-- Создание таблицы users
CREATE TABLE users (
    id UUID PRIMARY KEY
);

-- Создание таблицы ratings
CREATE TABLE ratings (
    user_id UUID REFERENCES users(id),
    item_id UUID,
    rating INTEGER,
    PRIMARY KEY (user_id, item_id)
);

-- Создание таблицы likes
CREATE TABLE likes (
    user_id UUID REFERENCES users(id),
    item_id UUID,
    PRIMARY KEY (user_id, item_id)
);

-- Создание таблицы bookmarks
CREATE TABLE bookmarks (
    user_id UUID REFERENCES users(id),
    item_id UUID,
    PRIMARY KEY (user_id, item_id)
);
