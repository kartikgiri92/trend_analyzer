// URLS
var window_location_origin = window.location.origin
var fetch_all_trends_url = window_location_origin + "/api/prime/get-trend/";

// Page Vars
var loading_div = document.querySelector("#loading-div")
var error_div = document.querySelector("#error-div")
var table_div = document.querySelector("#table-div")
var table_body = document.querySelector("#table-body")

function show_loading_div(){
    loading_div.style.display = "block";
}

function hide_loading_div(){
    loading_div.style.display = "none";
}

function show_error_div(){
    error_div.style.display = "block";
}

function hide_error_div(){
    error_div.style.display = "none";
}

function show_table_div(){
    table_div.style.display = "block";
}

function hide_table_div(){
    table_div.style.display = "none";
}

function get_times(time_str){
    let myDate = new Date(time_str);
    myDate = myDate.toString();
    let temp_index = myDate.search('G');
    return(myDate.slice(0, temp_index));
}

function fill_table(json_obj_data){
    json_obj_data.forEach(function(trend_element){
        let created_ele = document.createElement("tr");
        let temp_element;

        // Trend Name
        let anch_tag = document.createElement("a");
        temp_element = document.createElement("td");
        anch_tag.href = trend_element.url;
        anch_tag.innerHTML = "#" + trend_element.name;
        temp_element.append(anch_tag);
        created_ele.append(temp_element);

        // Trend Total Tweets
        temp_element = document.createElement("td");
        temp_element.innerHTML = trend_element.total_tweet_volume;
        created_ele.append(temp_element);

        // Trend Is Top Trending
        temp_element = document.createElement("td");
        if(trend_element.is_top_trending){
            temp_element.innerHTML = "True";
            temp_element.classList.add("text-success");
        }
        else{
            temp_element.innerHTML = "False";
            temp_element.classList.add("text-danger");
        }
        created_ele.append(temp_element);

        // Trend Last Updated
        temp_element = document.createElement("td");
        temp_element.innerHTML = get_times(trend_element.last_updated);
        created_ele.append(temp_element);

        // Trend Analytics Link
        let btn_tag = document.createElement("a");
        temp_element = document.createElement("td");
        btn_tag.classList.add("btn");
        btn_tag.classList.add("btn-sm");
        btn_tag.classList.add("btn-info");
        btn_tag.href = window_location_origin + "/" + trend_element.id;
        btn_tag.innerHTML = "See Analytics";
        temp_element.append(btn_tag);
        created_ele.append(temp_element);

        table_body.append(created_ele);
    });
}

const fetch_all_trends = async () => {
    let response = await fetch(fetch_all_trends_url, {
        method: "GET",
    });
    if(response.ok){
        let json_obj = await response.json();
        if(json_obj.status && json_obj.data.length){
            hide_loading_div();
            hide_error_div();
            show_table_div();
            fill_table(json_obj.data);
        }
        else{
            hide_loading_div();
            hide_table_div();
            show_error_div();    
        }
    }
    else{
        hide_loading_div();
        hide_table_div();
        show_error_div();
    }
}

// On Page Load
window.addEventListener('load', (event) => {
    hide_table_div();
    hide_error_div();
    fetch_all_trends();
});