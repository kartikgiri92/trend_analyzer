// URLS
var pathname = window.location.pathname;
if(pathname.length == 1) var window_location_pathname = "";
else var window_location_pathname = pathname.slice(1, -1);
var window_location_origin = window.location.origin

var fetch_active_trend_url = window_location_origin + "/api/prime/get-active-trend/";
var fetch_trend_by_id_url = window_location_origin + "/api/prime/get-trend/";


// Trend Info Section Variables
var trend_information_section = document.querySelector("#trend-information-section")
var trend_information_not_available_tag = document.querySelector("#trend-information-not-available-tag")

// Trend Info Section Functions

function display_trend_information_data_unavailability_tag(){
    trend_information_not_available_tag.style.display = "block";
    trend_information_section.style.display = "none";
}

function hide_trend_information_data_unavailability_tag(){
    trend_information_not_available_tag.style.display = "none";
    trend_information_section.style.display = "block";
}

function fill_trend_information(json_obj_data){
    let trend_information_elements = document.querySelectorAll(".trend-information")

    // Trend Name
    trend_information_elements[0].style.color = "blue";
    trend_information_elements[0].innerHTML = '#' + json_obj_data.name;

    // Trend TOTAL TWEETS
    trend_information_elements[1].style.color = "blue";
    if(json_obj_data.total_tweet_volume == "0"){
        trend_information_elements[1].innerHTML = "No Data";
    }
    else{
        trend_information_elements[1].innerHTML = json_obj_data.total_tweet_volume;
    }

    // Trend TOP TRENDING
    if(json_obj_data.is_top_trending){
        trend_information_elements[2].style.color = "#118a2c";
        trend_information_elements[2].innerHTML = "True"
    }
    else{
        trend_information_elements[2].style.color = "red";
        trend_information_elements[2].innerHTML = "False"
    }

    // Trend ANALYSIS TWEET QUANTITY
    trend_information_elements[3].style.color = "blue";
    trend_information_elements[3].innerHTML = json_obj_data.num_positive + json_obj_data.num_neutral +  json_obj_data.num_negative;

    // Trend Positive Percentage
    trend_information_elements[4].style.color = "#118a2c";
    trend_information_elements[4].innerHTML = Math.round( json_obj_data.positive_percentage * 100 ) / 100;

    // Trend Neutral Percentage
    trend_information_elements[5].style.color = "blue";
    trend_information_elements[5].innerHTML = Math.round( json_obj_data.neutral_percentage * 100 ) / 100;

    // Trend Negative Percentage
    trend_information_elements[6].style.color = "red";
    trend_information_elements[6].innerHTML = Math.round( json_obj_data.negative_percentage * 100 ) / 100;

    // Pie Chart
    var generated_chart = Highcharts.chart('chartContainer', {
        chart: {
            type: 'pie',
        },
        title: {
            text: "Sentiment Analysis over " + (json_obj_data.num_positive + json_obj_data.num_neutral +  json_obj_data.num_negative) + " tweets"
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },
        series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'Neutral',
                color:'blue',
                y: json_obj_data.neutral_percentage,
            }, {
                name: 'Positive',
                color:'rgb(17, 138, 44)',
                y: json_obj_data.positive_percentage
            }, {
                name: 'Negative',
                color:'red',
                y: json_obj_data.negative_percentage
            }]
        }]
    });

    // Remove previous embed tweets
    let positive_sentiment_card_body = document.querySelector("#positive-sentiment-card-body")
    let negative_sentiment_card_body = document.querySelector("#negative-sentiment-card-body")
    let neutral_sentiment_card_body = document.querySelector("#neutral-sentiment-card-body")
    positive_sentiment_card_body.innerHTML = "";
    negative_sentiment_card_body.innerHTML = "";
    neutral_sentiment_card_body.innerHTML = "";

    // embed new tweets
    if(json_obj_data.positive_tweets.length){
        json_obj_data.positive_tweets.forEach(function(tweet_id){
            let created_ele = document.createElement("div");
            created_ele.classList.add("col");
            created_ele.classList.add("col-md-auto");
            created_ele.classList.add("mb-2");
            positive_sentiment_card_body.append(created_ele);
            twttr.widgets.createTweet(
                tweet_id,
                created_ele,
                {})
                .then(function (el){
            });
        });
    }
    else{
        positive_sentiment_card_body.innerHTML = "No Data";
    }

    if(json_obj_data.neutral_tweets.length){
        json_obj_data.neutral_tweets.forEach(function(tweet_id){
            let created_ele = document.createElement("div");
            created_ele.classList.add("col");
            created_ele.classList.add("col-md-auto");
            created_ele.classList.add("mb-2");
            neutral_sentiment_card_body.append(created_ele);
            twttr.widgets.createTweet(
                tweet_id,
                created_ele,
                {})
                .then(function (el){
            });
        });
    }
    else{
        neutral_sentiment_card_body.innerHTML = "No Data";
    }

    if(json_obj_data.negative_tweets.length){
        json_obj_data.negative_tweets.forEach(function(tweet_id){
            let created_ele = document.createElement("div");
            created_ele.classList.add("col");
            created_ele.classList.add("col-md-auto");
            created_ele.classList.add("mb-2");
            negative_sentiment_card_body.append(created_ele);
            twttr.widgets.createTweet(
                tweet_id,
                created_ele,
                {})
                .then(function (el){
            });
        });
    }
    else{
        negative_sentiment_card_body.innerHTML = "No Data";
    }
}

const fetch_trend = async (temp_pathname) => {
    let temp_url = fetch_trend_by_id_url + temp_pathname + '/';
    let response = await fetch(temp_url, {
        method: "GET",
    });
    if(response.ok){
        let json_obj = await response.json();
        if(json_obj.status){
            hide_trend_information_data_unavailability_tag();
            fill_trend_information(json_obj.data);
        }
        else{
            display_trend_information_data_unavailability_tag();
        }
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
            fetch_trend(item.id);
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
        else{
            display_active_trend_data_unavailability_tag();
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