
function onForestCellClick(cell) {
    console.log(cell.id + " clicked");
    let occupiedPopup = document.getElementById("occupied-popup");
    let emptyPopup = document.getElementById("empty-popup");

    if (cell.plantId == "0") { //if cell is empty
        if (occupiedPopup.style.display == "block") { closePopup(occupiedPopup); }
        //opens popup to plant tree
        openPopup(emptyPopup);
    }
    else {
        if (emptyPopup.style.display == "block") { closePopup(emptyPopup); }
        //opens popup to view tree progress
        openPopup(occupiedPopup);
        //update popup details
        document.getElementById("plant-name").innerText = cell.id; //getPlantName(cell.plantid);
        document.getElementById("selected-plant-image").src = cell.plantImagePath;
        document.getElementById("selected-plant-description").innerText = "Growth stage: " + cell.plantGrowthStage
    }
}

function customiseClick() {
    let customisePopup = document.getElementById("customise-popup");
    let sellPopup = document.getElementById("sell-popup");
    if (customisePopup.style.display == "block") {
        closePopup(customisePopup)
    }
    else {
        if (sellPopup.style.display == "block") {
            closePopup(sellPopup);
        }
        openPopup(customisePopup);
    }
}

function sellClick() {
    let customisePopup = document.getElementById("customise-popup");
    let sellPopup = document.getElementById("sell-popup");
    if (sellPopup.style.display == "block") {
        closePopup(sellPopup)
    }
    else {
        if (customisePopup.style.display == "block") {
            closePopup(customisePopup);
        }
        openPopup(sellPopup);
    }
}

function recyclingClick() {
    let recyclingPopup = document.getElementById("recycling-popup");
    if (recyclingPopup.style.display == "block") {
        recyclingPopup.style.animation = "recycling-exit 0.5s";
        setTimeout(function () { recyclingPopup.style.display = "none"; }, 480);
    }
    else {
        let occupiedPopup = document.getElementById("occupied-popup");
        let emptyPopup = document.getElementById("empty-popup");
        let customisePopup = document.getElementById("customise-popup");
        let sellPopup = document.getElementById("sell-popup");
        if (occupiedPopup.style.display == "block") {
            closePopup(occupiedPopup)
        }
        if (emptyPopup.style.display == "block") {
            closePopup(emptyPopup)
        }
        if (customisePopup.style.display == "block") {
            closePopup(customisePopup)
        }
        if (sellPopup.style.display == "block") {
            closePopup(sellPopup)
        }
        recyclingPopup.style.display = "block";
        recyclingPopup.style.animation = "recycling-enter 0.5s";
    }
}

function openPopup(popup) {
    //check if recycling popup is open
    let recyclingPopup = document.getElementById("recycling-popup");
    if (recyclingPopup.style.display == "block") {
        recyclingPopup.style.animation = "recycling-exit 0.5s";
        setTimeout(function () { recyclingPopup.style.display = "none"; }, 480);
    }
    //open popup
    popup.style.display = "block";
    popup.style.animation = "popup-enter 0.5s";
}

function closePopup(popup) {
    popup.style.animation = "popup-exit 0.5s";
    setTimeout(function () { popup.style.display = "none"; }, 480);
}

function generateCustomiseGrid(rows, cols) {
    const gridContainer = document.getElementById("customise-grid");
    gridContainer.style.setProperty('--grid-rows', rows);
    gridContainer.style.setProperty('--grid-cols', cols);
    for (let i = 0; i < (rows * cols); i++) {
        let gridCell = document.createElement("div");
        const addedCell = gridContainer.appendChild(gridCell);
        addedCell.className = "grid-item";
        addedCell.id = "item-cell-" + i;
        addedCell.addEventListener("click", function () { onCustomiseCellClick(addedCell); });
    }
}

function reloadForest(plantLocation, changedValueIndex, newValue) {
    //TODO refresh retrieved-first-content
    //reading database entry
    const userForest = document.getElementById("retrieved-forest-content").innerHTML.split(";");
    let forestArray = Array(userForest.length);
    let i = 0;
    for (const plant of userForest) {
        forestArray[i] = plant.split(",");
        i += 1;
    }

    //applying changes
    forestArray[plantLocation][changedValueIndex] = newValue;

    //rebuilding database entry
    let forestString = "";
    i = 0;
    for (const plant of forestArray) {
        forestString += plant[0] + "," + plant[1] + "," + plant[2] + ";";
    }
    forestString = forestString.substring(0, forestString.length - 1);
    //save foreststring
}

// generate user's forest grid 
function generateForestGrid(rows, cols) {
    const gridContainer = document.getElementById("forest-grid");
    //splits data into arrays for each plant
    const userForest = document.getElementById("retrieved-forest-content").innerHTML.split(";");
    gridContainer.style.setProperty('--forest-rows', rows);
    gridContainer.style.setProperty('--forest-cols', cols);
    let forestContainer = document.getElementById("forest-images");
    // iterates for each cell that will be in the grid
    for (let i = 0; i < (rows * cols); i++) {
        let gridCell = document.createElement("div");
        console.log("Creating forest-cell-" + i);
        const addedCell = gridContainer.appendChild(gridCell);
        addedCell.className = "grid-item";
        addedCell.id = "forest-cell-" + i;
        console.log("Adding event listener for click");
        addedCell.addEventListener("click", function () { onForestCellClick(addedCell); })

        let currentPlant = userForest[i].split(",");

        //creating each image
        const plantImage = document.createElement("img");
        let addedPlantImage = forestContainer.appendChild(plantImage);

        addedCell.plantId = currentPlant[0]; // id of plant in cell, 0 if none
        addedCell.plantGrowthStage = currentPlant[1]; //0, 1, or 2
        addedCell.plantRequirement = currentPlant[2]; //0 if no requirement, 1 for fertiliser, etc
        //if cell contains plant
        if (currentPlant[0] != 0) {
            //check if plant is first stage
            if (addedCell.plantGrowthStage == 0) {
                addedCell.plantImagePath = media_url + "forest_assets/id0.png";
            }
            else {
                addedCell.plantImagePath = media_url + "forest_assets/id" + addedCell.plantId + "_" + addedCell.plantGrowthStage + ".png";
            }
        }
        else {
            addedCell.plantImagePath = media_url + "forest_assets/empty.png";
        }

        //placing images in correct place
        addedPlantImage.src = addedCell.plantImagePath;
        let cellRect = addedCell.getBoundingClientRect();
        let forestRect = forestContainer.getBoundingClientRect();
        addedPlantImage.style = "height: 50%; width: 20%; position:absolute; top: " + ((100 * ((cellRect.top - forestRect.top) / forestRect.height)) - 35) + "%; left: " + (100 * ((cellRect.left - forestRect.left) / forestRect.width)) + "%;";

    }
}

generateForestGrid(4, 4);
generateCustomiseGrid(4, 4);

document.getElementById("customise-button").addEventListener("click", customiseClick);
document.getElementById("sell-button").addEventListener("click", sellClick);
document.getElementById("recycling-button").addEventListener("click", recyclingClick);
document.getElementById("close-recycling-popup").addEventListener("click", function () { closePopup(document.getElementById("recycling-popup")) });
document.getElementById("close-occupied-popup").addEventListener("click", function () { closePopup(document.getElementById("occupied-popup")) });
document.getElementById("close-empty-popup").addEventListener("click", function () { closePopup(document.getElementById("empty-popup")) });
document.getElementById("close-customise-popup").addEventListener("click", function () { closePopup(document.getElementById("customise-popup")) });
document.getElementById("close-sell-popup").addEventListener("click", function () { closePopup(document.getElementById("sell-popup")) });
