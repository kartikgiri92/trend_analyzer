var active_trend_url = window.location.origin + "/api/prime/get-active-trend/";
var fetch_trend_by_id_url = window.location.origin + "/api/prime/get-trend/";

const get_active_trend = async () => {
    let response = await fetch(active_trend_url, {
        method: "GET",
    });
    if (response.ok){
        let json_obj = await response.json();
        // if(json_obj.status){
        //     console.log('Y');
        // }
        // else{
        //     console.log('N');
        // }
        
    }
    else{
        console.log("Error occured, reload the page.");
    }
}

const fetch_trend = async () => {
    let temp_url = fetch_trend_by_id_url + '5/';
    let response = await fetch(temp_url, {
        method: "GET",
    });
    if (response.ok){
        let json_obj = await response.json();
        // console.log(json_obj)
        if(json_obj.status){
            console.log('Y');
        }
        else{
            console.log('N');
        }
        
    }
    else{
        console.log("Error occured, reload the page.");
    }
}

// get_active_trend();
// fetch_trend();