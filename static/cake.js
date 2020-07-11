const BASE_URL = "http://localhost:5000/api";

/* Handle form submission from index.html */
$('#new-cupcake-form').on("submit", async function(event){
    event.preventDefault();
    let flavor = $('#form-flavor').val();
    let size = $('#form-size').val();
    let rating = $('#form-rating').val();
    let image = $('#form-image').val();

const resp = await axios.post(`${BASE_URL}/cupcakes`, {flavor,size,rating,image});
let newCupcake = $(generateHTML(resp.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
})

/* generate template */
function generateHTML(cupcake){
    return `
    <div data-cupcake-id =${cupcake.id}
    <li>${cupcake.flavor} / ${cupcake.size} / Rating : ${cupcake.rating}
    <button class="delete_btn"> X </button> 
    </li>
    <img class="Cupcake-img" src="${cupcake.image}" alt="${cupcake.image}">
    </div>`;
    }

/* show initial cupcakes in page */
async function loadInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
  
    for (let cupcakeData of response.data.cupcakes) {
      let newCupcake = $(generateHTML(cupcakeData));
      $("#cupcakes-list").append(newCupcake);
    }
  }

/* Handle delete button */

$("#cupcakes-list").on("click", ".delete_btn", async function(event){
    event.preventDefault();
    let $cupcake = $(event.target).closest("div");
    let cakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cakeId}`);
    $cupcake.remove();
});


$(loadInitialCupcakes);