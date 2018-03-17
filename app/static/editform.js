/**
 * Created by ACER on 12/11/2017.
 */
function AllowEdit(xHow){
        TheForm=document.forms[0].elements;  //get form elements list
    for(i=0;i<TheForm.length;i++){
      if(TheForm[i].name != "EditButton")
      TheForm[i].disabled = xHow;
    }
}

