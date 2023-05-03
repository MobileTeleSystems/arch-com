--create database archdb;
-- use archdb; 
-- show tables;


-- CREATE TABLE IF NOT EXISTS `Presentation` 
--     (`id` INT NOT NULL AUTO_INCREMENT,
--     `title` VARCHAR(256) NOT NULL,
--     `date` Date  NOT NULL,
--     `author_id` INT NULL,
--     PRIMARY KEY (`id`),
--     KEY `ai` (`author_id`));


-- ALTER TABLE `Author` ADD  `id` INT PRIMARY KEY  AUTO_INCREMENT;


describe Author;
select count(*) from Author;
select * from Author where id=10;
explain select * from Author where id=10;
explain select * from Author where first_name='Josh';
show index from Author;
create index first_name using btree on Author(first_name);
show index from Author;
explain select * from Author where first_name='Josh';
explain extended select * from Author where first_name like 'Jo%';
--insert into Author (first_name,last_name,email,title) values ('Иван','Иванов','ivanov@yandex.ru','господин');
--SELECT LAST_INSERT_ID();
--select * from Author where id=LAST_INSERT_ID();
--delete from Author where id= 100001;

-- drop index first_name on Author;
--explain format=json select * from Author where first_name='Elle%' and last_name='A%';

-- partitioning



-- ALTER TABLE Author ADD  birth_year INT NULL;
-- UPDATE `Author` SET `birth_year` = YEAR(STR_TO_DATE(SUBSTRING(`birth_date`,1,10), '%Y-%m-%d'));
-- alter table Author drop PRIMARY KEY, add primary key (`id`, `birth_year`);

-- ALTER TABLE Author PARTITION BY RANGE (birth_year) (
--     PARTITION p2011 VALUES LESS THAN (2011),
--     PARTITION p2021 VALUES LESS THAN (2021),
--     PARTITION p9999 VALUES LESS THAN MAXVALUE
-- );

explain partitions select * from Author where first_name like 'Jo%';
explain partitions select * from Author where birth_year<2011;
--ALTER TABLE Author TRUNCATE PARTITION p0,p1,p2,p3,p4;
--ALTER TABLE log DROP PARTITION p0;
