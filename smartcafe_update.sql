USE cafe_system;

UPDATE locations
SET name='Мамыр', address='Мамыр 7, 8Б'
WHERE id=1;

UPDATE locations
SET name='Розыбакиев', address='Розыбакиева 133'
WHERE id=2;

UPDATE locations
SET name='Абылайхана', address='Абылайхана 24'
WHERE id=3;

INSERT IGNORE INTO users (username, password, role)
VALUES ('guest', 'guest', 'guest');

ALTER TABLE recipes
ADD COLUMN IF NOT EXISTS output_quantity DECIMAL(10,3) DEFAULT 1;

ALTER TABLE recipes
ADD COLUMN IF NOT EXISTS output_unit VARCHAR(50) DEFAULT 'порция';
