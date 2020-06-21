// Html components
var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");
var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");

var resultTable = document.getElementById("result-table");
var classification = document.getElementById("classification");
var covidProb = document.getElementById("covid-probability");
var pneumoniaProb = document.getElementById("pneumonia-probability");
var healthyProb = document.getElementById("healthy-probability");

// Listens for file drag events
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  e.preventDefault();
  e.stopPropagation();
  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

function predictImage() {
  console.log("predicting...");

  imageDisplay.classList.add("loading");
  predImage(imageDisplay.src);
}

//when the clear button gets pushed
function clearImage() {
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(resultTable);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}

//shows the image in the imageviewer
function previewFile(file) {
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}

//Posts image to backend, gets prediction result
function predImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
 	console.log("result determined");
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("you have an error: ", err.message);
    });
}

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

//TODO: This is obviously ugly, format this in a future merge request..
//Displays the class and probabilities
function displayResult(data) {
  classification.innerHTML = data.resultClass;
  covidProb.innerHTML = data.covid;
  pneumoniaProb.innerHTML = data.pneumonia;
  healthyProb.innerHTML = data.healthy
  show(resultTable);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}
