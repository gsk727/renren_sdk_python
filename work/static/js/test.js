$("#test2").bind("click", function(event){
    //alert(event);
    var t = $(this);
    var b = t.find("p");
    var a = $(this)[0];
    alert(t.find("p").first().text());
    

    var arr = ["a", "b", "c"];
    arr = jQuery.map(arr, function(v,i){
        v = "a" + i;
        return v;
    });
    
    
    jQuery.each(arr, function(i, n){
        //alert(i + n);
    });
    
     
})

$("#pBtn").bind("mouseover", function(event){
    var a = $(this);
    var $this = $(this);
    if ($("#testDiv").length != 0)
            return
    html="<div id='testDiv'>xxxxx </div>"
    $("body").append(html); 
    $("#testDiv").css({"border-style":"solid",  "border-width":"1", "border-color":"#0000ff"});

});
