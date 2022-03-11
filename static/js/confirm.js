


function message_error(obj) {
    
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    }
    else{
        html = '<p>'+obj+'</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}



function submit_with_ajax(url,parameters,callback){
    $.confirm({
        theme: 'material',
        title: 'Confirmación',
        icon: 'fas fa-plus',
        content: '¿Estas seguro de realizar esta accion?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        contentType: false,
                        processData: false,
                    }).done(function (data) {
                        console.log(data);
                        
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                        
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert("Hubo un error");
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {
        
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {
                    
                }
            },
        }
    })
}


function alert_action(callback,cancel=null){
    $.confirm({
        theme: 'material',
        title: 'Confirmación',
        icon: 'fas fa-plus',
        content: '¿Estas seguro de realizar esta accion?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    })
}