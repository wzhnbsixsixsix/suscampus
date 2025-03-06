const forestView = document.getElementById("forest-grid");

function onCellClick(cell) {
    console.log(cell.id +" clicked");
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
    }
}

generateGrid(4, 4);