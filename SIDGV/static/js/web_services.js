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