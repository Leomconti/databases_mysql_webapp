-- Table: Pagador (Payer)
CREATE TABLE Pagador (
  pagador_id INT PRIMARY KEY AUTO_INCREMENT,
  nome_completo VARCHAR(255) NOT NULL,
  email_contato VARCHAR(255) NOT NULL,
  num_documento_identificacao VARCHAR(50) NOT NULL,
  telefone_contato VARCHAR(50) NOT NULL
);

-- Table: Unidade (Unit)
CREATE TABLE Unidade (
  unidade_id INT PRIMARY KEY AUTO_INCREMENT,
  numero_identificador VARCHAR(50) NOT NULL,
  localizacao VARCHAR(255) NOT NULL
);

-- Table: Pagamento (Payment)
CREATE TABLE Pagamento (
  payment_id INT PRIMARY KEY AUTO_INCREMENT,
  pagador_id INT NOT NULL,
  data_pagamento DATE NOT NULL,
  comprovante LONGBLOB,
  ano_referencia INT NOT NULL,
  mes_referencia INT NOT NULL,
  unidade_id INT NOT NULL,
  data_registro DATETIME,
  FOREIGN KEY (pagador_id) REFERENCES Pagador(pagador_id),
  FOREIGN KEY (unidade_id) REFERENCES Unidade(unidade_id)
);


DELIMITER //

CREATE PROCEDURE InsertPagamento(
  IN payerId INT,
  IN paymentDate DATE,
  IN receipt LONGBLOB,
  IN referenceYear INT,
  IN referenceMonth INT,
  IN unitId INT
)
BEGIN
  INSERT INTO Pagamento (pagador_id, data_pagamento, comprovante, ano_referencia, mes_referencia, unidade_id, data_registro)
  VALUES (payerId, paymentDate, receipt, referenceYear, referenceMonth, unitId, NOW());
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER RegistroPagamento
BEFORE INSERT ON Pagamento
FOR EACH ROW
BEGIN
  SET NEW.data_registro = NOW();
END //

DELIMITER ;

