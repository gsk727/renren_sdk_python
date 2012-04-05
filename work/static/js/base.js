var currnet_clicked = "show" // update, add
var checkMap = {
    "stuff" : checkStuff,
    "base" : checkBase,
    "task" : checkTask,
    "airline" : checkAir,
    "device" : checkDevice,
    "content" : checkContent,
};

var options = {
    // target:         '#htmlExampleTarget',    // target element(s) to be updated with server response
    beforeSubmit : showRequest, // pre-submit callback 表单提交前被调用的回调函数
    success : showResponse   // post-submit callback   表单提交成功后被调用的回调函数
    // other available options:
    //url:        url          // override for form's 'action' attribute
    //type:       type         // 'get' or 'post', override for form's 'method' attribute
    //dataType:   null         // 'xml', 'script', or 'json' (expected server response type)
    //clearForm: true         // clear all form fields after successful submit
    //resetForm: true         // reset the form after successful submit
    // $.ajax options can be used here too, for example:
    //timeout:    3000
}

function checkContent(frmName) {
    return true;
}

function checkAir(frmName) {
    return true;
};

function checkDevice(frmName) {
    return true;
};


$("#addBtnOK").live("click", function() {
    var cType = $("#checkType").val();
    cFun = checkMap[cType];
    if(!cFun("#frmAdd"))
        return false;
    // options.target = "\/base\/add";
    $("#frmAdd").ajaxForm(options);

    /*
     var objs = $("#frmAdd input[type!=hidden]");
     var p = {};

     for(var i=0; i < objs.length; ++i)
     {
     p[objs.eq(i).attr("id")] = objs.eq(i).val();
     }

     var sel = $("#frmAdd select option:selected");
     p[sel.parent().attr("id")] = sel.val();
     url = $("#frmAdd").attr("action");
     $.ajax({
     type: "POST",
     url: url,
     data: p,
     dataType: "json",
     success: function(data, textStatus){
     alert(data.message);
     }
     });
     */
});
function handle_addStuff(data, textstatus) {
    m = data.message;
}


$("#frmUpdate #base").bind("GETBASEOK", function(event, selName, index) {
    $(selName + " option:nth-child(" + (index + 1) + ")").attr("selected", true);
    g_cur_base = null;
});


function getBaseNames(callback, url, params, selName) {
    $.ajax({
        type : "GET",
        url : url,
        data : params,
        dataType : "json",
        success : function(data, textStatus) {
            callback(data, textStatus, selName);
        }
    });
};

function addBaseToSel(data, textStatus, selName) {
    var d = $(selName);
    $(selName).empty();
    var dType = $("#checkType").val();

    for(var i = 0; i < data.message.length; ++i) {
        if( typeof g_cur_base != "undefined" && g_cur_base == data.message[i])
            $("<option selected=true>" + data.message[i] + "</option>").appendTo(selName);
        else if( typeof g_cur_airline != "undefined" && g_cur_airline == data.message[i])
            $("<option selected=true>" + data.message[i] + "</option>").appendTo(selName);
        else {
            $("<option>" + data.message[i] + "</option>").appendTo(selName);
        }
    }
    // $(selName).trigger("GETBASEOK", selName, index)
};


$("#addTab").bind("click", function() {
    current_clicked = "add";
    var cType = $("#checkType").val();
    $("div #2")[0].innerHTML = addDivHTML;

    switch(cType) {
        case 'base':
            break;
        case 'device':
            getBaseNames(addBaseToSel, url = "/airline/", {
                dType : "json"
            }, "#frmAdd #airline");
        default:
            getBaseNames(addBaseToSel, "/base/", {
                dataType : "json"
            }, "#frmAdd #base")
    };
});

$("#myTable tbody tr").bind("click", function() {
    g_cur_index = $(this).index();
});


$("#myTable tbody tr").bind("dblclick", function() {
    g_cur_index = $(this).index();
    g_current_selected = $("#myTable tr:nth-child(" + (g_cur_index + 1) + ")");
    t = $("#checkType").val();
    switch(t) {
        case 'base':
            window.location.href = '/'+ t + '/' + $.trim(g_current_selected.children("td:eq(0)").text());
            break;
        case 'task':
            window.location.href = '/' + t + '/' + $("#currentBase").val() + '/' + $.trim(g_current_selected.children("td:eq(0)").text());
        case 'task_show':
            $('#task_show').modal();
            break;
        default:
            break;
    }
});


$("#updateTab").bind("click", function() {
    current_clicked = "update";
    $("div #3")[0].innerHTML = updateDivHTML;
    if( typeof g_cur_index == "undefined")
        return false;
    g_current_selected = $("#myTable tr:nth-child(" + (g_cur_index + 1) + ")");
    var inputID, baseIndex;
    var inputs = $("#frmUpdate >input, #frmUpdate select");
    for(var i = 0; i < inputs.length; ++i) {
        inputID =inputs.eq(i).attr("id");
        if(inputID == "base") {
            baseIndex = i;
            continue;
        }
        $("#frmUpdate #" + inputID).attr("value", $.trim(g_current_selected.children("td:eq(" + i + ")").text()));
    }

    var a =  $.trim(g_current_selected.children("td:eq(0)").text());
    // $("#3 #notify")[0].innerHTML =  "你正在修正的是" + $.trim(g_current_selected.children("td:eq(0)").text());

    g_cur_base = $.trim(g_current_selected.children("td:eq(" + baseIndex + ")").text());
    if($("#checkType").val() == "device")
        g_cur_airline = $("#myTable tr:nth-child(" + (g_cur_index + 1) + ")").children("td:eq(" + i + ")").text();

    var cType = $("#checkType").val();
    switch(cType) {
        case 'base':
            break;
        case 'device':
            getBaseNames(addBaseToSel, url = "/airline/", {
                dType : "json"
            }, "#frmUpdate #airline");
        default:
            getBaseNames(addBaseToSel, "/base/", {
                dataType : "json"
            }, "#frmUpdate #base")
    };
});


function checkTask(frmName) {
    /*
    var start = $.trim($(frmName + " #start").val());
    var end = $.trim($(frmName + " #end").val());
    if(start.length == 0 || end.length == 0) {
        alert("没有制定时间");
        return false;
    }*/

    return true;
}

function checkBase(frmName) {
    var name = $.trim($(frmName + " #name").val());
    if(name.length == 0)
        return alert("名字不能空");
    return true;
};

function checkStuff(frmName) {
    /*
    var name = $.trim($(frmName + " #name").val());
    var role = $.trim($(frmName + " #role").val());
    var begin = $.trim($(frmName + " #begin").val());
    var end = $.trim($(frmName + " #end").val());
    var email = $.trim($(frmName + " #email").val());

    if(email.length == 0)
        return alert("email 不能空");
    else if(name.length == 0)
        return alert("名字不能空");
    else if(begin.length == 0)
        return alert("入职日期不能空");
    */

    return true;
};

/*
 live,  bind的区别见jquery文档
 **/
$("#updateBtnOK").live("click", function() {
    var cType = $("#checkType").val();
    cFun = checkMap[cType];
    if(!cFun("#frmUpdate"))
        return false;
     $("#frmUpdate").ajaxForm(options);
});
// pre-submit callback
function showRequest(formData, jqForm, options) {
    // formData is an array; here we use $.param to convert it to a string to display it
    // but the form plugin does this for you automatically when it submits the data
    var queryString = $.param(formData);
    // jqForm is a jQuery object encapsulating the form element.   To access the
    // DOM element for the form do this:
    // var formElement = jqForm[0];
    // alert('About to submit: \n\n' + queryString);
    // here we could return false to prevent the form from being submitted;
    // returning anything other than false will allow the form submit to continue
    return true;
}

// post-submit callback
function showResponse(responseText, statusText) {
    // for normal html responses, the first argument to the success callback
    // is the XMLHttpRequest object's responseText property
    // if the ajaxSubmit method was passed an Options Object with the dataType
    // property set to 'xml' then the first argument to the success callback
    // is the XMLHttpRequest object's responseXML property
    // if the ajaxSubmit method was passed an Options Object with the dataType
    // property set to 'json' then the first argument to the success callback
    // is the json data object returned by the server
    if(statusText != "success")
    {
        alert( "什么情况出错了啊");
        return; 
    }
    switch(current_clicked) {
        case "add":
            $("#2")[0].innerHTML = responseText;
            break;
        case "update":
            $("#3")[0].innerHTML = responseText;
            break;
        case "show":
            break;
        default:
            break;
    }
}