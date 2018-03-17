function yesnoCheck() {
    if (document.getElementById('yesCheck').checked) {
        document.getElementById('ifYes').style.visibility = 'visible';

         var nature1code = "BC";
    }
    else document.getElementById('ifYes').style.visibility = 'hidden';


    if (document.getElementById('yesCheck1').checked) {
        document.getElementById('ifYes1').style.visibility = 'visible';
        var nature2code = "MC";
    }
    else document.getElementById('ifYes1').style.visibility = 'hidden';

        if (document.getElementById('yesCheck2').checked) {
        document.getElementById('ifYes2').style.visibility = 'visible';
        
        var nature3code = "BP";
    }
    else document.getElementById('ifYes2').style.visibility = 'hidden';

}