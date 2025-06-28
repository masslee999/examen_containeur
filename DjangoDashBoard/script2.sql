-- Sélection de la base de données pour y travailler
USE students;

ALTER TABLE DevStudents MODIFY active VARCHAR(10) DEFAULT 'Active';

ALTER TABLE DevStudents MODIFY creation_date DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6);
