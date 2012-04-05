/*
$("#loginBtn").bind("click", function(){
        var name = $.trim($("#username").val());
        var pwd = $.trim($("#password").val());
        var ct = $.trim($("#csrf_token").val());

        if (name.length==0  && pwd.length==0)
        {
            alert("用xxx为空");
            //$("#EDiv1").show();
            return;
        }

        var d = {username: name, password: pwd, csrf_token: ct};
        $.ajax({
           type:"POST",
           url:"/user/",
           data:d,
           dataType:"json",
           success:function(data, textStatus){
                if (data.message != "ok") {
                    alert(data.message);
                }
                else{
                    document.cookie = 'username'+"=" + escape(name);
                    window.location.href="/user/"+name;
                    // window.history.go(-1);
                    //$.ajax.get("/user/"+name);
                }
           }
        });
    }
);
*/
