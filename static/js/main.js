initialize();
let appliedFilters = {
    price: {
        applied: false, value: ''
    },
    query: {
        applied: false, value: ''
    },
}

function initialize() {
    new Waypoint.Infinite({
        // container: document.querySelector('.items-cont'),
        element: document.querySelector('.infinite-container'),
    
        onBeforePageLoad: function (items){
            console.log('triggered')
            try{
                let link_anchor = document.querySelector('.infinite-more-link')
                let url = link_anchor.getAttribute('href');
                let newurl = new URL(`${window.location.origin}${window.location.pathname}${url}`);
    
                Object.entries(appliedFilters).forEach(([key, value]) => {
                    console.log(key, value)
                    if (value.applied){
                        try {
                            newurl.searchParams.get(key)
                            newurl.searchParams.set(key, value.value);
                        } catch (error) {
                            newurl += `&${key}=${value.value}`
                        }
                    }
                    newurl = newurl.toString().replace(`${window.location.origin}${window.location.pathname}`, '')
                    console.log(newurl)
                    link_anchor.setAttribute('href', newurl)
                });
            }catch (er){
                console.log(er)
            }
        },
        offset: function() {
            const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
            return -this.element.clientHeight + vh
        }
    })
}

refreshUrl()
function refreshUrl(){
    console.log('refreshed')
    initialize()
    let urlParams = new URLSearchParams(window.location.search);

    Object.entries(appliedFilters).forEach(([key, value]) => {
        try {
            let value = urlParams.get(key);
            if (value) {
                appliedFilters[`${key}`].applied = true
                appliedFilters[`${key}`].value = value
                if (key == "price") {
                    let btn = document.querySelector(`button[data-value=${value}]`)
                    btn.classList.replace('btn-warning', 'btn-danger')
                }
            }
        } catch (error) {
        }
    });
}

function handleFilters(elem,force_refresh=false){
    const param = elem.getAttribute('data-param')
    let toAppend = elem.getAttribute('data-append') != "false"
    let value = ""
    let isBtn = false
    // console.log(toAppend)
    if (elem.value){
        value = elem.value
    }else if(elem.query){
        value = elem.query.value
    }else{
        value = elem.getAttribute('data-value')
        isBtn = true
    }
    if (value == appliedFilters[`${param}`].value){
        appliedFilters[`${param}`].applied = false
        appliedFilters[`${param}`].value = ''
        popUp("Filter Removed.")
    }
    else{
        appliedFilters[`${param}`].applied = true
        appliedFilters[`${param}`].value = value
        popUp("Filter Applied.")
    }

    if (toAppend){
        toggleActive(true, value, param)
    }

    // popUp("Filter Updated.")

    function toggleActive(isBtn=false,value=null, param=null) {
        if (isBtn){
            elem.parentElement.querySelectorAll('.btn').forEach(btn=>{
                if (btn == elem){
                    if (elem.classList.contains("btn-warning")){
                        btn.classList.replace('btn-warning', 'btn-danger')
                    }else{
                        btn.classList.replace('btn-danger', 'btn-warning')
                    }
                }else{
                    btn.classList.replace('btn-danger', 'btn-warning')
                }
            })
        }
        // appendAppliedFilter(param, value)
    }
    if (force_refresh){
        refreshPage()
    }
}



function refreshPage(elem){
    try{
        let newurl = new URL(`${window.location.origin}${window.location.pathname}`);
        let have_filters = true

        newurl += `?page=1`

        Object.entries(appliedFilters).forEach(([key, value]) => {
            console.log(key, value)
            if (value.applied){
                have_filters = true
                try {
                    newurl.searchParams.get(key)
                    newurl.searchParams.set(key, value.value);
                } catch (error) {
                    newurl += `&${key}=${value.value}`
                }
            }
            //newurl = newurl.toString().replace(`${window.location.origin}${window.location.pathname}`, '')
            console.log(newurl)
            if (have_filters){
                window.location.href = newurl;
            }
        });
    }catch (er){
        console.log(er)
    }
}



// Applied Filters manage

function closeAppliedFilter(elem) {
    let param = elem.parentElement.getAttribute('data-param');
    elem.parentElement.remove()
    if (param){
        appliedFilters[`${param}`].applied = false;
        appliedFilters[`${param}`].value = '';
        refreshPage()
    }
}

function appendAppliedFilter(param, value) {

    let FilterAppliedCont = document.getElementById('filter-applied-cont')
    let filter = FilterAppliedCont.querySelector(`.filter-applied[data-param="${param}"]`);
    if (value == appliedFilters[`${param}`].value){
        if (filter){
            filter.querySelector('span').innerHTML = text ? text : param ;
        }
        else{
            FilterAppliedCont.innerHTML += `
            <div class="col-lg-3 col-md-5 col-sm-12 filter-applied m-1" data-param="${param}">
                <span>${text ? text : param}</span>
                <i class="close-filter ms-auto fas fa-times" onclick="closeAppliedFilter(this)"></i>
            </div>
            `
        }
    }else{
        let filter = FilterAppliedCont.querySelector(`.filter-applied[data-param="${param}"]`);
        filter.remove()
    }
}


document.getElementById('search-form').addEventListener('submit', (event)=>{
    event.preventDefault()
    const query = event.target
    handleFilters(query, true)
})