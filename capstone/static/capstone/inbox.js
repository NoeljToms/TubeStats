document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn").forEach((element)=>{
      element.addEventListener("click", function () {
        if(element.className === "btn btn-danger" && element.id === "saveChannel"){
          saveChannel(element);
        }else if (element.className === "btn btn-dark" && element.id === "deleteChannel"){
          removeChannel(element);
        }
      });

    });
    
})

function saveChannel(element){
    pfp = document.querySelector("#pfp").src;
    title = document.querySelector("#title").textContent;
    subs = document.querySelector("#subs").textContent;
    views = document.querySelector("#views").textContent;
    vids = document.querySelector("#vids").textContent;
    channel_id = document.querySelector("#channel_id").textContent;
    fetch("/save", {
        method: "POST",
        body: JSON.stringify({
            pfp:pfp,
            title:title,
            subs:subs,
            views:views,
            vids:vids,
            channel_id:channel_id,
        }),
      })
        .then((response) => response.json())
        .then((result) => {
          // Print result
          console.log(result);
          element.className = "btn btn-dark"
          element.textContent = "Remove"
          element.id = "deleteChannel"
        });
}
function removeChannel(element){
  channel_id = document.querySelector("#channel_id").textContent;
  fetch("/remove", {
    method: "POST",
    body: JSON.stringify({
        channel_id:channel_id,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result);
      element.className = "btn btn-danger"
      element.textContent = "Save Channel"
      element.id = "saveChannel"

    });
}