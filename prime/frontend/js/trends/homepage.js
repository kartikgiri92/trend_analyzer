console.log('Hello World')

const userAction = async () => {
  const response = await fetch('http://127.0.0.1:8000/api/prime/get-active-trend/', {
    method: 'GET',
    // body: myBody, // string or object
    // headers: {
      // 'Content-Type': 'application/json'
    // }
  });
  const myJson = await response.json(); //extract JSON from the http response
  console.log(response)
  console.log(myJson)
}