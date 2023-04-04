<html>
<body>
    
<?php

$python = 'C:/Users/Nathan/anaconda3/python.exe'; //path to python executable
$pyscript = '';
$hello = '';
function generate($url_){
    global $python;
    global $pyscript;
    $pyscript = '../generate.py';
    $site = $url_;

    return shell_exec("$python $pyscript $site");
}
?>
<link rel="stylesheet" href="style.css">

Your url is: <br></br>
<?php global $URL; $URL = $_GET["url"]; echo $URL?><br></br>
The formatted citation is: <br></br>
<?php echo "<p id=\"formatted\">" . generate($URL) . "</p>";?><br>

<button onclick = "window.location.href='test.php';">Return to home</button>

</body>
</html>
