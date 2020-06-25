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

function sendfile(){
    var fd = new FormData();
    var files = $('#file')[0].files[0];
    fd.append('file',files);    
    $.ajax({
        url: 'upload',
        type: 'POST',
        data: fd,
        contentType: false,
        processData: false,
        success: function(response){
            if(response != 0){
                //$('#img').attr('src',response);
                //$('.preview  img').show();
                alert(response);
            }   
            else{
                alert('File not uploaded');
            }        
        }
    });
}