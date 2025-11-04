use bluegatefarm;

INSERT INTO crops (name, area_hectares, current_season) VALUES
('Soja', 150.00, 2025),
('Milho', 85.50, 2025),
('Trigo', 60.75, 2024);

INSERT INTO employees (name, cpf, job, base_salary, weekly_hours, hire_date, id_crop_fk) VALUES
('João Silva', 12345678901, 'Gerente Agrícola', 6500.00, 44, '2020-03-15', NULL),
('Maria Oliveira', 98765432109, 'Operador de Máquinas', 3200.50, 40, '2022-08-20', 1), 
('Pedro Souza', 11223344556, 'Técnico Agrônomo', 4800.75, 44, '2021-05-10', 2), 
('Ana Pereira', 44556677889, 'Auxiliar Geral', 2500.00, 40, '2023-01-05', 1); 

INSERT INTO userType (description) VALUES
('Administrador do Sistema'),
('Gerente'),
('Operacional'),
('Visitante');

INSERT INTO users (name, email, password, activity, id_user_type_fk, id_employee_fk) VALUES
('Admin', 'admin@bluegate.com', 'hash_admin_123', TRUE, 1, NULL), 
('joaoSilva', 'joao.silva@bluegate.com', 'hash_joao_456', TRUE, 2, 1), 
('Maria', 'maria.o@bluegate.com', 'hash_maria_789', TRUE, 3, 2); 

INSERT INTO machineryType (name) VALUES
('Trator'),
('Colheitadeira'),
('Pulverizador'),
('Plantadeira');

INSERT INTO machineryBrand (name) VALUES
('John Deere'),
('Case IH'),
('Massey Ferguson'),
('New Holland');

INSERT INTO machinery (model, year, total_worked_hours, total_fuel_consumption, id_machinery_brand_fk, id_machinery_type_fk) VALUES
('JD 7815', 2018, 3500, 15500.50, 1, 1), 
('Axial-Flow 7250', 2020, 1200, 8900.25, 2, 2), 
('MF 4292', 2015, 4200, 18000.00, 3, 1), 
('TL5.80', 2022, 500, 2500.70, 4, 3); 

INSERT INTO machineryUsage (usage_date, hours_usage, fuel_consumed, observation, id_machinery_fk, id_employee_fk) VALUES
('2025-10-25', 8.5, 45.20, 'Preparo de solo para o Milho.', 1, 2), 
('2025-10-26', 10.0, 55.00, 'Plantio de Soja, talhão B.', 1, 2),
('2025-04-15', 7.2, 85.30, 'Colheita de Milho, finalização.', 2, 2); 

INSERT INTO grains (name, type) VALUES
('Soja', 'Oleaginosa'),
('Milho', 'Cereal'),
('Trigo', 'Cereal');

INSERT INTO storageLocations (name) VALUES
('Silo Principal - Leste'),
('Silo Auxiliar - Oeste'),
('Armazém de Bagagem');

INSERT INTO storage (quantity_bags, entry_date, id_grain_fk, id_location_fk) VALUES
(5000, '2025-06-10', 2, 1),
(8000, '2025-05-20', 1, 2),
(1200, '2024-12-01', 3, 3); 

INSERT INTO costTypes (name, cost_value) VALUES
('Fertilizante', 850.00), 
('Semente', 320.00),
('Defensivo', 1200.00),
('Mão de Obra', 10.00); 

INSERT INTO productionCosts (cost_date, description, id_cost_type_fk) VALUES
('2025-09-01', 'Compra de NPK para Soja (150 un)', 1), 
('2025-09-05', 'Compra de semente de Milho Híbrido (85 un)', 2),
('2025-10-20', 'Aplicação de Herbicida no Milho', 3); 

INSERT INTO marketQuotes (price_per_bag, quote_date, observation, id_grain_fk) VALUES
(135.50, '2025-10-30', 'Cotação da bolsa de Chicago, Dólar a 5.10', 1),
(65.20, '2025-10-30', 'Cotação interna, alta demanda', 2), 
(78.90, '2025-10-28', 'Fechamento do dia, mercado estável', 3); 