function onForestCellClick(cell) {
    console.log(cell.id + " clicked");
    let occupiedPopup = document.getElementById("occupied-popup");
    let emptyPopup = document.getElementById("empty-popup");

    if (cell.plantId == "0") { //if cell is empty
        if (occupiedPopup.style.display == "block") { closePopup(occupiedPopup); }
        emptyPopup.selectedCell = cell;
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

function onCustomiseClick() {
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

function onSellClick() {
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

function onRecyclingClick() {
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

function onPlantCellClick(cell) {
    document.getElementById("selected-plant-name").innerHTML = cell.selectedPlantName;
    let resourceName = "";
    switch (cell.selectedPlantResource){
        case "0":
            resourceName = "Water";
            break;
        case "1":
            resourceName = "Tree Guard";
            break;
        case "2":
            resourceName = "Fertiliser";
            break;
    }
    document.getElementById("selected-plant-resource").innerHTML = resourceName;
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


//drag and drop handlers
function litterDragStart(event) {
    event.dataTransfer.clearData();
    event.dataTransfer.setData('text/plain', event.target.id);

    let litter = event.currentTarget;
    event.currentTarget.style.border = "#1da124";
    //highlighting correct bin
    switch (litter.litterType) {
        case 0:
            document.getElementById("plastic-recycling").style.height = "100%";
            document.getElementById("paper-recycling").style.opacity = "0.4";
            document.getElementById("compost-recycling").style.opacity = "0.4";
            break;
        case 1:
            document.getElementById("plastic-recycling").style.opacity = "0.4";
            document.getElementById("paper-recycling").style.height = "100%";
            document.getElementById("compost-recycling").style.opacity = "0.4";
            break;
        case 2:
            document.getElementById("paper-recycling").style.opacity = "0.4";
            document.getElementById("plastic-recycling").style.opacity = "0.4";
            document.getElementById("compost-recycling").style.height = "100%";
            break;
    }
}

function litterDragEnd(event) {
    let litter = event.currentTarget;
    litter.style.border = "none";

    //resetting bin styles
    document.getElementById("plastic-recycling").style.opacity = "1";
    document.getElementById("paper-recycling").style.opacity = "1";
    document.getElementById("compost-recycling").style.opacity = "1";

    document.getElementById("plastic-recycling").style.height = "90%";
    document.getElementById("paper-recycling").style.height = "90%";
    document.getElementById("compost-recycling").style.height = "90%";
}

function generateRecycling() {
    const litterContainer = document.getElementById("litter-container");
    const user_inv = document.getElementById("retrieved-inventory-content").innerHTML.split(',');
    // populates the container with unrecycled paper
    for (let i = 0; i < user_inv[0]; i++) {
        addRecycleable(i, 0);
    }
    // populates the container with unrecycled plastic
    for (let i = 0; i < user_inv[1]; i++) {
        addRecycleable(i, 1);
    }
    //populates the container with unrecycled compost
    for (let i = 0; i < user_inv[2]; i++) {
        addRecycleable(i, 2);
    }

    function addRecycleable(num, type) {
        let litterImg = document.createElement("img");
        const addedLitter = litterContainer.appendChild(litterImg);
        addedLitter.id = "added-litter-" + type + "-" + num;
        addedLitter.litterType = type
        addedLitter.draggable = "true";
        addedLitter.classList.add("litter");
        // places litter at a random point in the container
        addedLitter.style = "top: " + Math.random() * 60 + "%; left: " + + Math.random() * 90 + "%;";
        switch (addedLitter.litterType) {
            case 0:
                addedLitter.style.backgroundColor = "red";
                break;
            case 1:
                addedLitter.style.backgroundColor = "blue";
                break;
            case 2:
                addedLitter.style.backgroundColor = "green";
                break;
        }
        addedLitter.ondragstart = function () { litterDragStart(event) };
        addedLitter.ondragend = function () { litterDragEnd(event) };
    }
}

function generatePlantSelectionGrid(cols) {
    const userInv = document.getElementById("retrieved-forest-content").innerHTML.split(",");
    const gridContainer = document.getElementById("plant-selection-grid");
    
    let oakCount = userInv[9];
    let birchCOunt = userInv[10];
    let firCount = userInv[11];
    let redCampionCount = userInv[12];
    let poppyCount = userInv[13];
    let cotoneasterCount = userInv[14];

    //skips the first empty array slot
    for (let i = 1; i < (plantArray.length - 1); i++) {  //cut out first empty item
        let gridCell = document.createElement("div");
        const addedCell = gridContainer.appendChild(gridCell);
        addedCell.className = "popup-grid-item";
        addedCell.id = "plant-selection-cell-" + i;
        addedCell.selectedPlantId = plantArray[i][0];
        addedCell.selectedPlantResource = plantArray[i][1];
        addedCell.selectedPlantRarity = plantArray[i][2];
        addedCell.selectedPlantName = plantArray[i][3];
        addedCell.addEventListener("click", function () { onPlantCellClick(addedCell); });

        const cellImage = addedCell.appendChild(document.createElement("img"));
        cellImage.classList = "contained-image";
        cellImage.src =  media_url + "forest_assets/id" + addedCell.selectedPlantId + "_2.png";
    }
}

function generateCustomiseGrid(rows, cols) {
    const gridContainer = document.getElementById("customise-grid");
    gridContainer.style.setProperty('--grid-rows', rows);
    gridContainer.style.setProperty('--grid-cols', cols);
    for (let i = 0; i < (rows * cols); i++) {
        let gridCell = document.createElement("div");
        const addedCell = gridContainer.appendChild(gridCell);
        addedCell.className = "popup-grid-item";
        addedCell.id = "item-cell-" + i;
        addedCell.addEventListener("click", function () { onCustomiseCellClick(addedCell); });
    }
}

function makeForestChanges(plantLocation, changedValueIndex, newValue) {
    ajaxCallUpdateForestData();

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
    ajaxCallSaveForest();

    //save foreststring
    function ajaxCallSaveForest() {
        $.ajax({
            url: "save",
            type: 'POST',
            data: {'user_forest_cells': forestString},
            success: function(response) {
                console.log("sent marker id to view successfully");
                console.log("Response: ", response);
            },
            error: function(error) {
                console.log("encountered error when sending marker id: ", error);
            }
        })
        .done(response => {console.log(response)}) // we don't need to do anything with the response
    }

    function ajaxCallUpdateForestData() {
        $.ajax({
            url: "update_forest_on_page",
            type: 'GET'
        })
            .done(response => {
                document.getElementById("retrieved-forest-content").innerHTML = response.user_forest;
                document.getElementById("sell-value").innerHTML = "Current value of your forest: " + response.forest_value + " tokens."
            })
    }
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
        addedPlantImage.classList.add("plant-image");
        addedPlantImage.src = addedCell.plantImagePath;
        let cellRect = addedCell.getBoundingClientRect();
        let forestRect = forestContainer.getBoundingClientRect();
        addedPlantImage.style = "top: " + ((100 * ((cellRect.top - forestRect.top) / forestRect.height)) - 37) + "%; left: " + ((100 * ((cellRect.left - forestRect.left) / forestRect.width))) + "%;";

    }
}

function addPlant() {

}

function getPlants() {
    let plantList = document.getElementById("retrieved-plant-content").innerHTML.split(";");
    var plantArray = new Array(plantList.length);
    for (let i = 0; i < plantList.length; i++) {    //ignore first item, no plant has id=0
        plantArray[i+1] = plantList[i].split(",");  //creates list where id corresponds to index, [[id, requirement_type, rarity, plant_name]]
    }
    return plantArray;
}

let plantArray = getPlants(); //[[plantid, requirement_type, rarity, plant_name]]
generateForestGrid(4, 4);
generateCustomiseGrid(4, 4);
generatePlantSelectionGrid(2);
generateRecycling();


document.getElementById("customise-button").addEventListener("click", onCustomiseClick);
document.getElementById("sell-button").addEventListener("click", onSellClick);
document.getElementById("recycling-button").addEventListener("click", onRecyclingClick);
document.getElementById("close-recycling-popup").addEventListener("click", function () { closePopup(document.getElementById("recycling-popup")) });
document.getElementById("close-occupied-popup").addEventListener("click", function () { closePopup(document.getElementById("occupied-popup")) });
document.getElementById("close-empty-popup").addEventListener("click", function () { closePopup(document.getElementById("empty-popup")) });
document.getElementById("close-customise-popup").addEventListener("click", function () { closePopup(document.getElementById("customise-popup")) });
document.getElementById("close-sell-popup").addEventListener("click", function () { closePopup(document.getElementById("sell-popup")) });
