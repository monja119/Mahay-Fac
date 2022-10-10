var section = document.getElementById('section');
var number = document.getElementById('number')
var count = 1

function add(){
    count += 1;
    number.value = count
    var field = `
            <br>
            <label for="item`+ count+`"> Objet :</label>
            <input type="text" name="item`+ count+`">
            <br>
            <label for="quantity`+ count+`"> Quantité :</label>
            <input type="number" name="quantity`+ count+`">
            <br>
            <label for="unitePrice`+ count+`"> Prix unitaire :</label>
            <input type="number" name="unitePrice`+ count+`">
            <br>
    `;

    section.innerHTML += field;
}