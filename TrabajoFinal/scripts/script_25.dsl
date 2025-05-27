load "empleados.csv";
filter column "nombre" contains "Ana";
aggregate count column "id_empleado";
print;