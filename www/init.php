<?php
echo "<html>\n<body>\n";
require ("clase_mysql.inc.php");
$miconexion = new DB_mysql ;
$miconexion->conectar("rtdb", "localhost", "root", "1admin");
$miconexion->consulta("SELECT parameter.id as id,parameter.name as name,parameter.default as value FROM parameter");
//$miconexion->verconsulta();
 echo "<table border=1>\n";
// mostramos los nombres de los campos
 for ($i = 0; $i < $miconexion->numcampos(); $i++){
  echo "<td><b>".$miconexion->nombrecampo($i)."</b></td>\n";
 }
 echo "</tr>\n";
// mostrarmos los registros
 while ($row = mysql_fetch_row($miconexion->Consulta_ID)) {
  echo "<tr> \n";
   $miconexion->consulta("UPDATE status,parameter SET status.value='".$row('value')."' WHERE parameter.name='".$row('id')."' AND status.id_parameter = parameter.id");
  for ($i = 0; $i < $miconexion->numcampos(); $i++){
   echo "<td>".$row[$i]."</td>\n";
  }
  echo "</tr>\n";
 }
echo "</body>\n</html>\n";
?>

