// URLS
var pathname = window.location.pathname;
if(pathname.length == 1) var window_location_pathname = "";
else var window_location_pathname = pathname.slice(1, -1);
var window_location_origin = window.location.origin

var fetch_active_trend_url = window_location_origin + "/api/prime/get-active-trend/";
var fetch_trend_by_id_url = window_location_origin + "/api/prime/get-trend/";


// Trend Info Section Variables
var active_trend_row = document.querySelector("#active-trend-row")
var active_trend_example_tag = document.querySelector("#active-trend-example-tag")
var active_trend_not_available_tag = document.querySelector("#active-trend-not-available-tag")

// Trend Info Section Functions

const fetch_trend = async (temp_pathname) => {
    let temp_url = fetch_trend_by_id_url + temp_pathname + '/';
    console.log(temp_pathname)
    let response = await fetch(temp_url, {
        method: "GET",
    });
    if(response.ok){
        let json_obj = await response.json();
        console.log(json_obj)
    }
    else{
        console.log("Error occured, reload the page.");
    }
}


// Active Trend Section Variables
var active_trend_row = document.querySelector("#active-trend-row")
var active_trend_example_tag = document.querySelector("#active-trend-example-tag")
var active_trend_not_available_tag = document.querySelector("#active-trend-not-available-tag")

// Active Trend Section Functions
function display_active_trend_data_unavailability_tag(){
    active_trend_not_available_tag.style.display = "block";
}

function hide_active_trend_data_unavailability_tag(){
    active_trend_not_available_tag.style.display = "none";
}

function unactivate_trending_button(){
    let temp_abc = document.querySelectorAll(".active-trend")
    temp_abc.forEach(function(prt_ele){
        prt_ele.children[0].classList.remove("active");
    });
}

function create_and_fill_active_trends(json_obj){
    json_obj.data.forEach(function(item){
        let temp_obj = active_trend_example_tag.cloneNode(deep=true);
        temp_obj.id = item.id;
        temp_obj.style.display = "block";
        temp_obj.children[0].innerHTML = '#' + item.name
        active_trend_row.append(temp_obj);
        temp_obj.addEventListener('click', event => {
            unactivate_trending_button();
            temp_obj.children[0].classList.add('active');
        });
    });
}

const get_active_trend = async () => {
    let response = await fetch(fetch_active_trend_url, {
        method: "GET",
    });
    if(response.ok){
        let json_obj = await response.json();
        if(json_obj.status && json_obj.data.length){
            hide_active_trend_data_unavailability_tag();
            create_and_fill_active_trends(json_obj);
        }
    }
    else{
        console.log("Error occured, reload the page.");
    }
}


// On Page Load
window.addEventListener('load', (event) => {
    get_active_trend();

    if(window_location_pathname)
        fetch_trend(window_location_pathname);
});