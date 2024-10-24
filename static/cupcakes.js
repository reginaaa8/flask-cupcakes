const BASE_URL = "http://127.0.0.1:5000/api";


/** generate html with cupcake data */

function generateCupcakeHTML(cupcake) {
  return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-img"
            src="${cupcake.image}"/>
    </div>
  `;
}


/** show existing cupcakes */

async function showInitialCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $("#cupcake-list").append(newCupcake);
  }
}

// handle form submission to add cupcake 

$("#add-cupcake-form").on("submit", async function (e) {
  e.preventDefault()

  let flavor = $("#flavor").val();
  let rating = $("#rating").val();
  let size = $("#size").val();
  let image = $("#image").val();

  const resp = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(generateCupcakeHTML(resp.data.cupcake));
  $("#cupcake-list").append(newCupcake);
  $("#add-cupcake-form").trigger("reset");

  
});

$("#cupcake-list").on("click", ".delete-button", async function(e){
  e.preventDefault();

  let $cupcake = $(e.target).closest("div")
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});




$(showInitialCupcakes); 