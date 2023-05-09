function updateInput()
{
    document.getElementById('search-btn').addEventListener('click', updateResults)
}

function Open(url) {
    window.open(url, "_blank");
}

function setUpTable()
{
    const buttons = $(".match-btn");

    //for everything in the table essentially
    function clickCallback() {
        var id = $(this).parent("td").parent("tr").children(".song-id").text();
        Open("/song-description/" + id)
    }

    buttons.on("click", clickCallback);
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
            setUpTable();
        }
    });
}

function setup()
{
    updateInput();
}


$(document).ready(setup);