<!DOCTYPE html>

<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
<script>
function show(shown, hidden){
    document.getElementById(shown).style.display='block';
    document.getElementById(hidden).style.display='none';
    return false;
}
</script>

    <link rel="stylesheet" href="style.css">
    <title>Citation Generator</title>
    <h1>Citation Generator</h1>

</head>

<?php

$python = 'C:/Users/Nathan/anaconda3/python.exe'; //path to python executable, set here
$pyscript = '';
$hello = '';

function generate($url_){
    global $python;
    global $pyscript;
    $pyscript = '../generate.py';
    $url = $url_;

    return shell_exec("$python $pyscript $url");
}

?>

<body>
<div id="Page1">
    <p>made by me</p>
    <p>This is a citation generator. Click next, then enter a URL. The page will automatically generate and format a citation based on the information on that site.</p>
    <button onclick="return show('Page2','Page1');">start citing</button>

</div>
<div id="Page2" style="display:none">
    
    <form autocomplete="off" action="citation.php" method="get">
    URL: <input type="text" name="url"><br></br>
    <input type="submit">
    </form>
    <p></p>
    <button onclick="return show('Page1','Page2');">return to home</button>

</div>

<div id="Page3" style="display:none">

</div>
</body>
</html>