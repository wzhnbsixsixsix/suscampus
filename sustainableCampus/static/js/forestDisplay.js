const forestView = document.getElementById("forest-grid");

function onCellClick(cell) {
    console.log(cell.id + " clicked");
    let occupiedPopup = document.getElementById("occupied-popup");
    let emptyPopup = document.getElementById("empty-popup");

    if (cell.plantid == 0) { //if cell is empty
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
    popup.style.animation = "popup-enter 0.5s"
}

function closePopup(popup) {
    popup.style.animation = "popup-exit 0.5s"
    setTimeout(function () { popup.style.display = "none"; }, 480);
}

// generate user's forest grid 
function generateGrid(rows, cols) {
    forestView.style.setProperty('--forest-rows', rows);
    forestView.style.setProperty('--forest-cols', cols);
    // iterates for each cell that will be in the grid
    for (let i = 0; i < (rows * cols); i++) {
        let gridCell = document.createElement("div");
        console.log("Creating forest-cell-" + i);
        const addedCell = forestView.appendChild(gridCell);
        addedCell.className = "grid-item";
        addedCell.id = "forest-cell-" + i;
        console.log("Adding event listener for click");
        addedCell.addEventListener("click", function () { onCellClick(addedCell); })
        //if cell contains plant
        // set cell to plant details
        // else
        addedCell.plantid = i
        addedCell.plantGrowthStage = 0
        addedCell.plantRequirement = 0 //0 if no requirement, 1 for fertiliser, etc

    }
}

generateGrid(4, 4);

document.getElementById("customise-button").addEventListener("click", customiseClick);
document.getElementById("sell-button").addEventListener("click", sellClick);
document.getElementById("recycling-button").addEventListener("click", recyclingClick);
document.getElementById("close-recycling-popup").addEventListener("click", function () { closePopup(document.getElementById("recycling-popup")) });
document.getElementById("close-occupied-popup").addEventListener("click", function () { closePopup(document.getElementById("occupied-popup")) });
document.getElementById("close-empty-popup").addEventListener("click", function () { closePopup(document.getElementById("empty-popup")) });
document.getElementById("close-customise-popup").addEventListener("click", function () { closePopup(document.getElementById("customise-popup")) });
document.getElementById("close-sell-popup").addEventListener("click", function () { closePopup(document.getElementById("sell-popup")) });
