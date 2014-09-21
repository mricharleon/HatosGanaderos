$(document).on('ready', function(){
    $.ajax({
        type:'GET',
        contentType: 'application/json; charset=utf-8',
        dateType:'json',
        url:'/ws/ganados/',
        success:function(response){
            console.log(response);
            for (var i = 0; i < response.length; i++) {
                $('.account_list').append(
                    "<a>"+ 
                        "<div>"+ 
                            "<img src='{{ MEDIA_URL }}"+response[i].fields.imagen +"'>"+
                            "</img>"+
                            "<h4 class='texto_propiedades1'>"+
                                response[i].fields.etapa.nombre+
                            "</h4>"+
                        "</div>"+
                    "</a>"
                    );                    
                
            }
        }
    });
});

// el ultimo archivo
<script type='text/javascript'>

  $(document).ready(function() {

    $( "#busqueda" ).on('keyup', function(tecla) {
      
      var busqueda = $("#busqueda").val()
        $.ajax({
          data: {'search': busqueda},
          type:'GET',
          contentType: 'application/json; charset=utf-8',
          dateType:'json',
          url:'/ws/ganados/',
          success:function(response){
           
            $('.content').empty();
            if(response!=''){
              for (var i = 0; i < response.length; i++) {
                $('.content').append(
                    "<a href=''>"+ 
                          "<div class='searching_cattle'>"+ 
                              "<h5>#" + response[i].fields.rp + "</h5>" +
                              "<h5>(" + response[i].fields.nombre + ")</h5>" +
                          "</div>"+
                      "</a>"
                  ); 
              }
            }else{
              $('.content').html('<h5>No se encuentra "'+busqueda+'"</h5>');
            }
          }
        });
      $( ".close-reveal-modal2" ).click(function() {
        
      });
    });

  }); 

</script>

// el html
<div id="myModal" class="reveal-modal">
         <h2>Buscar RP de la madre </h2>
         {% csrf_token %}
          
          <input type="text" id="busqueda"  placeholder="RP, nombre o año de nacimiento" >

          <div class="content">
          </div>

         <a class="close-reveal-modal">&#215;</a>
    </div>