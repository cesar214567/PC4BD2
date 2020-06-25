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

function sendfile(url1){
    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);    
    $.ajax({
        url: url1,
        type: 'POST',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            var i=0; 
            response.forEach(element => {
              var linea="<tr><td>ID</td><td><img src=\"static/TEMPLATE\" width=\"300\" height=\"200\">";
              linea+="</td><td>NAME</td></tr>";
              linea.replace("ID",response[i].id);
              linea.replace("TEMPLATE",response[i].name);
              linea.replace("NAME",response[i].name);
              i++;
              $("#"+url1).append(linea );
              
                
            });
        }
    });
}