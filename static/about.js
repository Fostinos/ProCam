/********************** ready **************************/

$( document ).ready(function() {
    $.each($('select'), function () {
        $(this).selectmenu({ width : $(this).attr("width")})
    });
    currentMonitor();
});

$('#tabs').tabs({
    create: function( event, ui ) {
        $('#cpu-dynamic').show();
        $('#disk-dynamic').hide();
        $('#ram-dynamic').hide();
    },
    activate: function(event, ui){
        // index 0 equals to CPU Tab
        if(ui.newTab.index() == 0){
            $('#cpu-dynamic').show();
            $('#disk-dynamic').hide();
            $('#ram-dynamic').hide();
        }
        // index 1 equals to DISK Tab
        if(ui.newTab.index() == 1){
            $('#cpu-dynamic').hide();
            $('#disk-dynamic').show();
            $('#ram-dynamic').hide();
        }
        // index 2 equals to RAM Tab
        if(ui.newTab.index() == 2){
            $('#disk-dynamic').hide();
            $('#cpu-dynamic').hide();
            $('#ram-dynamic').show();
        }
    }
});

$( "#button-icon-disk" ).button({
	icon: "ui-icon-disk",
	showLabel: false
}).click(function(){
    window.location.href = '/explorer';
});

$( "#button-icon-live" ).button({
	icon: "ui-icon-bullet",
	showLabel: false
}).click(function(){
    window.location.href = '/';
});

$( ".button-default" ).button({
	icon: "ui-icon-gear",
	showLabel: false
}).click(function(){
    $.ajax({
        url: "/api/telemetry/default",
        type: "POST",
        datatype: "json",
        success: function(data){
            applyTelemetry(data);
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
});


/********************** functions **************************/

// monitoring
function currentMonitor(){
    $.ajax({
        url: "/api/monitoring",
        type: "GET",
        datatype: "json",
        success: function(data){
            applyMonitor(data)
        },
        error: function(xhr){
            showError(xhr.status);
        },
    });
}

// apply monitor
function applyMonitor(data){

    // CPU
    $( "#cpu-min" ).text( data['cpu']['frequency_min'] + ' Hz' );
    $( "#cpu-cores" ).text( data['cpu']['cores'] );
    $( "#cpu-max" ).text( data['cpu']['frequency_max'] + ' Hz' );
    $( "#cpu-usage" ).text( data['cpu']['percent'] + ' %' );
    $( "#cpu-frequency" ).text( data['cpu']['frequency_current'] + ' Hz' );
    $( "#cpu-temperature" ).text( data['cpu']['temperature'] + ' °C' );

    // DISK
    var disk_unit = data['disk']['unit'];
    $( "#disk-total" ).text( data['disk']['total'] + ' ' + disk_unit );
    $( "#disk-usage" ).text( data['disk']['percent'] + ' %' );
    $( "#disk-free" ).text( data['disk']['free'] + ' ' + disk_unit );

    // RAM
    var ram_unit = data['memory']['unit'];
    $( "#ram-total" ).text( data['memory']['total'] + ' ' + ram_unit );
    $( "#ram-usage" ).text( data['memory']['percent'] + ' %' );
    $( "#ram-free" ).text( data['memory']['available'] + ' ' + ram_unit );
    $( "#ram-cached" ).text( data['memory']['cached'] + ' ' + ram_unit );
}

let interval = 2000;

setInterval(currentMonitor, interval);


// alert error
function showError(status){
    var statusErrorMap = {
        '400' : "Bad Request",
        '401' : "Unauthorized",
        '403' : "Forbidden",
        '404' : "Not Found",
        '405' : "Method Not Allowed",
        '408' : "Request Timeout",
        '500' : "Internal Server Error",
        '501' : "Not Implemented",
        '503' : "Service unavailable"
    };
    message =statusErrorMap[status];
    if(!message){
        message="Unknown Error";
    }
    alert(message);
}