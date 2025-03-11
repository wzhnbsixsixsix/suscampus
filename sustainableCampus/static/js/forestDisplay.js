const forestView = document.getElementById("forest-grid");

function onCellClick(cell) {
    console.log(cell.id +" clicked");
    document.getElementById("occupied-popup").style.display = "none";
    document.getElementById("empty-popup").style.display = "none";

    if (cell.plantid == 0){ //if cell is empty
        //opens popup to plant tree
        document.getElementById("empty-popup").style.display = "block";
    }
    else {
        //opens popup to view tree progress
        document.getElementById("occupied-popup").style.display = "block";
        //update popup details
        document.getElementById("plant-name").innerText = cell.id //getPlantName(cell.plantid);
    }

}

function closeForestOccupiedPopup(){
    document.getElementById("occupied-popup").style.display = "none";
}

function closeForestEmptyPopup(){
    document.getElementById("empty-popup").style.display = "none";
}

// generate user's forest grid 
function generateGrid(rows, cols) {
    forestView.style.setProperty('--forest-rows', rows);
    forestView.style.setProperty('--forest-cols', cols);
    // iterates for each cell that will be in the grid
    for (let i = 0; i < (rows*cols); i++) {
        let gridCell = document.createElement("div");
        console.log("Creating forest-cell-" + i);
        const addedCell = forestView.appendChild(gridCell);
        addedCell.className = "grid-item";
        addedCell.id = "forest-cell-" + i;
        console.log("Adding event listener for click");
        addedCell.addEventListener("click", function(){onCellClick(addedCell);})
        //if cell contains plant
        // set cell to plant details
        // else
        addedCell.plantid = i
        addedCell.plantGrowthStage = 0
        addedCell.plantRequirement = 0 //0 if no requirement, 1 for fertiliser, etc

    }
}

generateGrid(4, 4);

document.getElementById("close-occupied-popup").addEventListener("click", closeForestOccupiedPopup);
document.getElementById("close-empty-popup").addEventListener("click", closeForestEmptyPopup);