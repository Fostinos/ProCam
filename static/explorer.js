/********************** ready **************************/
let ID = 1;
let imgID = 0;
let IDMax = 1;
let images;

$( document ).ready(function() {
    $( "#button-prev" ).button( "disable" );
    $( "#button-start" ).button( "disable" );
    $.ajax({
        url: "/api/images",
        type: "POST",
        data: {"ID" : ID},
        datatype: "json",
        success: function(data){
            console.log('ID ' + ID);
            images = data['images'];
            $(".visual-title").text(data['date']);
            $("#image-frame").attr('src', `data:image/png;base64, ${images[imgID]}`);
            IDMax = data['max'];
        },
        error: function(xhr){
            showError(xhr.status);
        },
    }); 
});

$( "#tabs" ).tabs();

$( "#button-icon-live" ).button({
	icon: "ui-icon-bullet",
	showLabel: false
}).click(function(){
    window.location.href = '/';
});

$( "#button-icon-info" ).button({
	icon: "ui-icon-info",
	showLabel: false
}).click(function(){
    window.location.href = '/about';
});


/********************** tabs-1 **************************/

// previous Intruder
$( "#button-start" ).button({
	icon: "ui-icon-seek-first",
	showLabel: false
}).click(function(){
    imgID = 0;
    $( "#button-prev" ).button( "disable" );
    $( "#button-next" ).button( "enable" );
    $( "#button-end" ).button( "enable" );
    if( ID == 1){
        $( "#button-start" ).button( "disable" );
    }else{
        ID = ID - 1;
    }
    $.ajax({
        url: "/api/images",
        type: "POST",
        data: {"ID" : ID},
        datatype: "json",
        success: function(data){
            console.log('ID ' + ID);
            images = data['images'];
            $(".visual-title").text(data['date']);
            $("#image-frame").attr('src', `data:image/png;base64, ${images[imgID]}`);
            IDMax = data['max'];
            if( ID == 1){
                $( "#button-start" ).button( "disable" );
            }
        },
        error: function(xhr){
            showError(xhr.status);
        },
    }); 
});

// next Intruder
$( "#button-end" ).button({
	icon: "ui-icon-seek-end",
	showLabel: false
}).click(function(){
    imgID = 0;
    $( "#button-prev" ).button( "disable" );
    $( "#button-next" ).button( "enable" );
    $( "#button-start" ).button( "enable" );
    if(ID == IDMax){
        $( "#button-end" ).button( "disable" );
    }else{
        ID = ID + 1;
    }
    $.ajax({
        url: "/api/images",
        type: "POST",
        data: {"ID" : ID},
        datatype: "json",
        success: function(data){
            console.log('ID ' + ID);
            images = data['images'];
            $(".visual-title").text(data['date']);
            $("#image-frame").attr('src', `data:image/png;base64, ${images[imgID]}`);
            IDMax = data['max'];
            if( ID == IDMax){
                $( "#button-end" ).button( "disable" );
            }
        },
        error: function(xhr){
            showError(xhr.status);
        },
    }); 
});

// play/stop Image
$( "#button-play" ).button({
	icon: "ui-icon-seek-play",
	showLabel: false
}).click(function(){
    
});

// previous Image
$( "#button-prev" ).button({
	icon: "ui-icon-seek-prev",
	showLabel: false
}).click(function(){
    $( "#button-next" ).button( "enable" );
    imgID = imgID - 1;
    if (imgID == 0){
        $( "#button-prev" ).button( "disable" );
    }
    $("#image-frame").attr('src', `data:image/png;base64, ${images[imgID]}`);
});

// next Image
$( "#button-next" ).button({
	icon: "ui-icon-seek-next",
	showLabel: false
}).click(function(){
    $( "#button-prev" ).button( "enable" );
    imgID = imgID + 1;
    if (imgID == images.length - 1){
        $( "#button-next" ).button( "disable" );
    }
    $("#image-frame").attr('src', `data:image/png;base64, ${images[imgID]}`);
});


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