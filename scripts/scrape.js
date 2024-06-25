// Create blob object with file content
var blob = new Blob(["This is a sample file content."], {
    type: "text/plain;charset=utf-8",
 });
 
 
 (function(console){
 
 console.save = function(data, filename){
 
     if(!data) {
         console.error('Console.save: No data')
         return;
     }
 
     if(!filename) filename = 'console.json'
 
     if(typeof data === "object"){
         data = JSON.stringify(data, undefined, 4)
     }
 
     var blob = new Blob([data], {type: 'text/json'}),
         e    = document.createEvent('MouseEvents'),
         a    = document.createElement('a')
 
     a.download = filename
     a.href = window.URL.createObjectURL(blob)
     a.dataset.downloadurl =  ['text/json', a.download, a.href].join(':')
     e.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
     a.dispatchEvent(e)
  }
 })(console)

 var button = document.getElementsByClassName( "next")[0];
 var links = [];
 for (let j = 0 ; j < 1029; j++) {
    let list = document.getElementsByClassName( "title");
    
    for(let i = 0 ; i < list.length ; i++) {
        links.push(list[i].href.substring(34) + " ");
        // console.log(list[i].href.substring(34));
        console.log('ok');
    }
    if (links % 20 == 0) {
        button.click();
    }
    console.log(links)
    
    // Create and save the file using the FileWriter library
    // saveAs(links, "sample.txt");
}


function downloadBlob(blob, name = 'file.txt') {
    // Convert your blob into a Blob URL (a special url that points to an object in the browser's memory)
    const blobUrl = URL.createObjectURL(blob);
  
    // Create a link element
    const link = document.createElement("a");
  
    // Set link's href to point to the Blob URL
    link.href = blobUrl;
    link.download = name;
  
    // Append link to the body
    document.body.appendChild(link);
  
    // Dispatch click event on the link
    // This is necessary as link.click() does not work on the latest firefox
    link.dispatchEvent(
      new MouseEvent('click', { 
        bubbles: true, 
        cancelable: true, 
        view: window 
      })
    );
  
    // Remove link from body
    document.body.removeChild(link);
  }

var blob = new Blob(links, {
    type: "text/plain;charset=utf-8",
});
downloadBlob(blob, 'doi.txt');