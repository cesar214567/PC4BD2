function Parallax(){
    
    $(document).ready(function(){
        $('.parallax').parallax();
      });
      document.addEventListener('DOMContentLoaded', function() {
        var elems = document.querySelectorAll('.parallax');
        var instances = M.Parallax.init(elems, options);
      });
}

function clearInner(node) {
    while (node.hasChildNodes()) {
      clear(node.firstChild);
    }
  }
  
  function clear(node) {
    while (node.hasChildNodes()) {
      clear(node.firstChild);
    }
    node.parentNode.removeChild(node);
}
function cargar(){
  $('.dropdown-trigger').dropdown();

}

function Nombre1(xD){
  document.getElementById("dropdownn1").innerText=xD.toLowerCase();
  document.getElementById("dropdownn1").innerHTML=xD.toLowerCase();
}


function sendfile(url1){
  var elem = document.getElementById('KNN');
  clearInner(elem);
    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);   
    var a =document.getElementById("dropdownn1").innerHTML;
    var b = $('#K').val();
    console.log(b)
    document.getElementById("K").value='';
    $.ajax({
        url: url1+"/"+a+"/"+b,
        type: 'POST',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            console.log(response[0]);
            i=0;
            $.each(response, function(){  
              var linea='<tr><td><img src=\'static/'+response[i].nombre+'\' width=\"300\" height=\"200\"></td><td>'+response[i].nombre+'</td></tr>';
              $("#KNN").append(linea );
              i++;
            });
              
                
        },
        error: function(response){
          console.log("WTF");
        }
    });
}


