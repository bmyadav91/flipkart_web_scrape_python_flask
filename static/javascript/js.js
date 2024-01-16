// mobile nav hide show 
const humburg_icon = document.querySelector(".humburg_icon i");
const mobile_nav_container = document.querySelector(".mobile_navbar_container");
humburg_icon.addEventListener("click", function () {
    mobile_nav_container.classList.toggle("active");
});

// search frorm 
$(".search_container #searchForm").on("submit", function(event){
    event.preventDefault();
    search_val = $("#search_query").val();
    document.querySelector(".search_query_dyn").innerText = search_val;

    // ajax request 
    $.ajax({
        url: '/s',
        method: 'post',
        data: {
            query_is: search_val
        },
        beforeSend: function () {
            $(".search_container button").attr("disabled", true);
        },
        success: function (data) {
            $(".product_container .product_parent").html(data);
        },
        complete: function(){
            $(".search_container button").attr("disabled", false);
        }
    });
    
});