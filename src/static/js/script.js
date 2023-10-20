$(document).ready(function(){
    if($('#is_continue_exp').is(":checked") == true) {
        $('#end_year_exp').attr('disabled', 'disabled');
        $('#end_year_exp').attr('required', false);
    } else {
        $('#end_year_exp').removeAttr('disabled');
        $('#end_year_exp').attr('required', true);
    }
    if($('#is_continue_edu').is(":checked") == true) {
        $('#end_year_edu').attr('disabled', 'disabled');
        $('#end_year_edu').attr('required', false);
    } else {
        $('#end_year_edu').removeAttr('disabled');
        $('#end_year_edu').attr('required', true);
    }
    $('#is_continue_exp').click(function() {
        if($('#is_continue_exp').is(":checked") == true) {
            $('#end_year_exp').attr('disabled', 'disabled');
            $('#end_year_exp').attr('required', false);
            $('#end_year_exp').val('')
        } else {
            $('#end_year_exp').removeAttr('disabled');
            $('#end_year_exp').attr('required', true);
        }
    })

    $('#is_continue_edu').click(function() {
        if($('#is_continue_edu').is(":checked") == true) {
            $('#end_year_edu').attr('disabled', 'disabled');
            $('#end_year_edu').attr('required', false);
            $('#end_year_edu').val('')
        } else {
            $('#end_year_edu').removeAttr('disabled');
            $('#end_year_edu').attr('required', true);
        }
    })
    if(!$('#id_country').val()){
        var citySelect = $('#id_city');
        citySelect.empty();
    } else {
        var countryId = $('#id_country').val();
        var url = '/auth/load-cities/?country=' + countryId;
        $.ajax({
            url: url,
            success: function(response) {
                var citySelect = $('#id_city');
                citySelect.empty();
                $.each(response.cities, function(key, value) {
                    console.log(value.id == response.current_city.id)
                    var optionVal = $('<option>').val(value.id).text(value.name).appendTo(citySelect);
                    if (value.id == response.current_city.id) {
                        optionVal.attr('selected', 'selected');
                    }
                });
                // citySelect.text(current_city)
                // $('#id_city').children("option").filter(":selected").val(response.current_city.id).text(response.current_city.name)
            }
        });
    }

    $('#id_country').change(function() {
        var countryId = $(this).val();
        var url = '/auth/load-cities/?country=' + countryId;
        $.ajax({
            url: url,
            success: function(response) {
                var citySelect = $('#id_city');
                citySelect.empty();
                $.each(response.cities, function(key, value) {
                    $('<option>').val(value.id).text(value.name).appendTo(citySelect);
                });
            }
        });
    });
})