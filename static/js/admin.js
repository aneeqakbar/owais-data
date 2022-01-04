const scrapperChecks = document.querySelectorAll("input[name='scrapper_check']")

scrapperChecks.forEach(check => {
    check.addEventListener('change', ()=>{
        console.log('Toggled')
        toggleScrapper(check)
    })
});

function toggleScrapper(check) {
    const owner = check.getAttribute("data-owner")
    const url = check.getAttribute("data-url")
    const state = check.checked

    var formData = {owner: owner, state: state};

    $.ajax({
        url : url,
        type: "POST",
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        data : formData,
        async : false,
        success: function(response,textStatus,xhr) {
            if (xhr.status == 202){
                popUp("Scrapper Toggled")
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}


function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
