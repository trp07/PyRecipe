/* Helper functions to be used by the app */

/***********************  INPUT FORMS *************************/

/* recipe/shared/recipe_ingredients.html:: add an "ingredient" table/input row */
$(document).ready(function() {
    var table_class = $(".recipe-ingredients"); // ingredient table class
    var table_row = $(".new-ingredient");
    var add_button = $(".add-ingredient"); // Add row when button pressed

    var row_to_add = '<tr>\n';
    row_to_add += table_row.html();
    row_to_add += '<td><button class="btn btn-danger" type="button">X</button></td>';
    row_to_add += '</tr>\n';

    $(add_button).click(function(e){ //on click, add row
        e.preventDefault();
        $(table_class).append(row_to_add);
    });

    $(table_class).on("click",".btn", function(e){ //on click, delete row
        e.preventDefault();
        $(this).parents('tr').remove();
    });
});
