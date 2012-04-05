$("#dir li").bind("click", function(event){
    $(".active").attr("class", "");
    $(this).attr("class", "active");
});


$(".active").live("click", function(event){
        var tag = $(this).find("a").text();
        if (tag == "个人信息") {
            $.get("/user/show", function(data){
                $("#show").html("<h1>" + data + "</h1>");
            });
        } else if (tag == "任务信息") {
             url = $(".active a").attr("href");
             $.get(url, function(data){
                 $("#show").html(data);
             });
             return false;
         }
});
