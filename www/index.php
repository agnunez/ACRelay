<?php
echo "<html>\n<body>\n";
require ("clase_mysql.inc.php");
$miconexion = new DB_mysql ;
$miconexion->conectar("rtdb", "localhost", "root", "1admin");
$miconexion->consulta("UPDATE status,parameter SET status.value='OPEN' WHERE parameter.name='S1R1' AND status.id_parameter = parameter.id");
$miconexion->consulta("UPDATE status,parameter SET status.value='OPEN' WHERE parameter.name='S1R2' AND status.id_parameter = parameter.id");
$miconexion->consulta("SELECT parameter.name,status.value FROM status,parameter WHERE status.id_parameter= parameter.id");
$miconexion->verconsulta();
echo "</body>\n</html>\n";
?>

