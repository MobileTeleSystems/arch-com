import pandas as pd
from sqlalchemy import create_engine
import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_SCHEME = os.getenv('DB_SCHEME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

engine = create_engine("mysql+pymysql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_HOST+":"+DB_PORT+"/"+DB_SCHEME, echo = True)

conn = engine.connect() 
conn.execute("""CREATE TABLE IF NOT EXISTS `Presentation` 
    (`id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(256) NOT NULL,
    `date` Date  NOT NULL,
    `author_id` INT NULL,
    PRIMARY KEY (`id`),
    KEY `ai` (`author_id`));""")
conn.execute("""DROP TABLE IF EXISTS Author;""")

df = pd.read_json("ExportJson.json")
df.to_sql("Author", con=engine, if_exists = 'replace', index=False)

conn.execute("""ALTER TABLE `Author` ADD  `id` INT PRIMARY KEY AUTO_INCREMENT;""")
conn.execute("""ALTER TABLE Author ADD  birth_year INT NULL;""")
conn.execute("""UPDATE `Author` SET `birth_year` = YEAR(STR_TO_DATE(SUBSTRING(`birth_date`,1,10), '%%Y-%%m-%%d'));""")
conn.execute("""alter table Author drop PRIMARY KEY, add primary key (`id`, `birth_year`);""")

conn.execute("""ALTER TABLE Author PARTITION BY RANGE (birth_year) (
    PARTITION p2011 VALUES LESS THAN (2011),
    PARTITION p2021 VALUES LESS THAN (2021),
    PARTITION p9999 VALUES LESS THAN MAXVALUE
);""")
