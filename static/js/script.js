function updateInput()
{
    document.getElementById('search-btn').addEventListener('click', updateResults)
}

function updateResults()
{
    let name = $("#name").val();
    let artist = $("#artist").val();
    //encodeURIComponent searchPrefix

    let url = "/search?name=" + name + "&" + "artist=" + artist

    request = $.ajax({
        type: "GET", //get request
        url: url,
        success: (response) => {
            $("#results").html(response); //put the response from the db into the results section of index.html (cause jquery is linked in the index.html file)
        }
    });
}

function setup()
{
    updateInput();
}


$(document).ready(setup);