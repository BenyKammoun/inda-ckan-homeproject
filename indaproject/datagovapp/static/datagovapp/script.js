$(document).ready(function() {
    function enableButtons() {
        $("#showQueryButton").prop('disabled', false);
        $("#downloadDataButton").prop('disabled', false);
    }


    $('#tagSelector').on('change', function() {
      const tag = $(this).val();
      $.ajax({
        url: '/datagov/get_datasets/',
        data: {
          'tag': tag
        },
        success: function(response) {
          var datasets = response.datasets;
          var html = '';
          for (var i = 0; i < datasets.length; i++) {
            html += '<option value="' + datasets[i].id + '">' + datasets[i].title + '</option>';
          }
          $('#datasetSelector').html(html);
          $('#datasetSelector').prop('disabled', false);
        }
      });
    });

    $('#datasetSelector').on('change', function() {
      alert($(this).val());
      const dataset_id = $(this).val();
      $.ajax({
        url: '/datagov/get_dataset_fields/',
        data: {
          'dataset_id': dataset_id
        },
        success: function(response) {
          var fields = response.fields;
          var html = '';
          for (var i = 0; i < fields.length; i++) {
            html += '<option>' + fields[i].id + '</option>';
            $('#fieldsSelector').html(html);
            $('#fieldsSelector').prop('disabled', false);
            enableButtons();
          }
        }
      });
    });
  });

  $("#mainForm").submit(function(event) {
    event.preventDefault(); // prevent the form from submitting via HTTP

    const formData = $(this).serialize();

    $.ajax({
      type: "POST",
      url: "/datagov/get_dataset_records/",
      data: formData,
      success: function(response) {
        // handle the response from the server
        $("#datasetRecordsContainer").html(response.html)
        console.log(response);
      },
      error: function(xhr, status, error) {
        // handle errors
        console.log(error);
      }
    });
  });

  $('#showQueryButton').on('click', function(event) {
    event.preventDefault(); // prevent the form from submitting via HTTP

    const selected_dataset = $('#datasetSelector').val();
    const selected_fields = $('#fieldsSelector').val();

    $.ajax({
      url: '/datagov/get_query_string/',
      method: 'GET',
      data: {
        'selected_fields': selected_fields,
        'selected_dataset': selected_dataset
      },
      success: function(response) {
        console.log(response);
        $("#queryStringElement").html(response);
        $("#queryStringElement").prop('href', response);
      },
      error: function(xhr, status, error) {
        // handle errors
        console.log(error);
      }
    });

    $('#downloadDataButton').on('click', function(event) {
        event.preventDefault(); // prevent the form from submitting via HTTP
        alert("downloadDataButton clicked");
        
        const selected_dataset = $('#datasetSelector').val();
        const selected_fields = $('#fieldsSelector').val();
        const file_format = $('#fileFomat').val();

        $.get('/datagov/download/', );

        $.ajax({
            url: "/datagov/download/",
            method: "GET",
            data: {
                selected_dataset: selected_dataset,
                selected_fields: selected_fields,
                file_format: file_format
            },
            success: function() {},
            error: function() {}
        });
    });
  });