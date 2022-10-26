//test onclick() event in JavaScript

function callClick(){
    alert("You will now be directly taken to a call with QuickHelp staff!");
}

function getQuotes(){
  fetch("https://type.fit/api/quotes")
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    console.log(data);
    //now return a random quote using Math.random()
    const i = Math.floor(Math.random() * (data.length - 1)) + 1;
    document.getElementById("quotestext").innerHTML = JSON.stringify(data[i]["author"]).replace(/^["'](.+(?=["']$))["']$/, '$1') + ": " + JSON.stringify(data[i]["text"]);
    
  });
    
}
