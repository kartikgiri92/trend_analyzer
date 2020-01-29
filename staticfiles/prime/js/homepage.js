console.log('Hello World');

var active_trend_url = "http://127.0.0.1:8000/api/prime/get-active-trend/";

// let response = await fetch(active_trend_url);

// // if(response.ok){ 
// //   let json = await response.json();
// //   console.log(json);
// //   console.log(response.status);
// // }
// // else{
// //   alert("HTTP-Error: " + response.status);
// // }

const get_active_trends = async () => {
    let response = await fetch(active_trend_url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    });
    if (response.ok){
        let json = await response.json();
        console.log(response);
    }
    else{
        alert("HTTP-Error: ");
    }
}

get_active_trends();