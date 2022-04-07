$(function () {
    $('input[name="date_range"]').daterangepicker({
         locale : {
             format: 'YYYY-MM-DD',
             applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
         }
    });


    $('input[name="date_range"]').on('change', function(){
        console.log($(this).val());
    });
});