document.addEventListener("DOMContentLoaded", function() {
    const addButton1 = document.querySelector("#add-button1");
    const selectHeaders1 = document.getElementById("select-headers1");
    const selectBodies1 = document.getElementById("select-bodies1");
    
    const addButton2 = document.querySelector("#add-button2");
    const selectHeaders2 = document.getElementById("select-headers2");
    const selectBodies2 = document.getElementById("select-bodies2");
  
    addButton1.addEventListener("click", function() {
      addNewColumn(selectHeaders1, selectBodies1);
    });
  
    addButton2.addEventListener("click", function() {
      addNewColumn(selectHeaders2, selectBodies2);
    });
  
    function addNewColumn(selectHeaders, selectBodies) {
      // Create a new select column
      const newSelectHeader = document.createElement("tr");
      newSelectHeader.innerHTML = `
        <div class="Select-container">
          <select class="select-box">
            <option value="">Select Column</option>
            <option value="first">HN</option>
            <option value="second">CID</option>
            <option value="third">ชื่อผู้ป่วย</option>
            <option value="fourth">สัญชาติ</option>
          </select>
        </div>
      `;
      selectHeaders.appendChild(newSelectHeader);
  
      // Create a new empty row in the table body
      const newRow = document.createElement("tr");
      newRow.innerHTML = "<td></td><td></td>";
      selectBodies.appendChild(newRow);
    }
  });
  