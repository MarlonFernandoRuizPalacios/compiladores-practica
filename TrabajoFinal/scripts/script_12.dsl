load "empleados.csv";
filter column "departamento" == "Tecnología";
filter column "salario" < 3000;
aggregate count column "id_empleado";
print;