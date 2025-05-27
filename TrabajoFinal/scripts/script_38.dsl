load "empleados.csv";
filter column "fecha_ingreso" == "2019-06-20";
aggregate count column "id_empleado";
print;