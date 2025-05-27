load "empleados.csv";
filter column "salario" between 3400 and 3600;
aggregate count column "id_empleado";
print;