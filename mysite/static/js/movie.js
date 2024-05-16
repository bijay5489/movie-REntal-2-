function addMovie() {
    var title = $("#new-movie-title").val().trim();
    $.post("/dbMovie/", { "action": "new", "title": title.trim() })
        .done(function (data) {
            fetchAllMovies();
            $("#error-message").text("");
        })
        .fail(function (response) {
            $("#error-message").text(response.responseJSON.error);
        });
}

function updateMovieStock(movieId, action) {
    $.post("/dbMovie/", { "movie_id": movieId, "action": action })
        .done(function (data) {
            fetchAllMovies();
            $("#error-message").text("");
        })
        .fail(function (response) {
            $("#error-message").text(response.responseJSON.error);
        });
}

function renderMoviesTable(movies) {
    var html = movies.map(function (movie) {
        return renderMovieRow(movie);
    }).join('');
    return html;
}

function renderMovieRow(movie) {
    return  `
    <tr id='movie-${movie.movie_id}'>
        <td>${movie.title}</td>
        <td class='stock'>${movie.stock}</td>
        <td class='checkedOut'>${movie.checked_out}</td>
        <td>
            <button class='act-btn' onclick='updateMovieStock(${movie.movie_id}, "add")'>+</button>
            <button class='act-btn' onclick='updateMovieStock(${movie.movie_id}, "remove")'>-</button>
        </td>
    </tr>
    `;
}

function fetchAllMovies() {
    $.get("/dbMovie/")
        .done(function (data) {
            $("#movies-table-body").html(renderMoviesTable(data));  // Render rows inside existing table
        })
        .fail(function (response) {
            $("#error-message").text(response.responseJSON.error);
            $("#movies-table-body").html(renderMoviesTable([]));  // Render empty rows
        });
}

$(document).ready(function () {
    fetchAllMovies();  // Load all movies when the page is loaded
});

