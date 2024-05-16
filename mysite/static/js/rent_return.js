let userId = 0;

$(document).ready(() => {
    fetchAllMovies();
});

const fetchAllMovies = () => {
    $.get("/dbMovie/")
        .done((data) => {
            const availableMovies = data.filter(movie => movie.stock >= 1);
            $("#all-movies-table-body").html(renderMoviesTable(availableMovies));
        })
        .fail((response) => {
            $("#error-message").text(response.responseJSON.error);
            $("#all-movies-table-body").html(renderMoviesTable([]));
        });
};

const fetchMember = () => {
    const email = $('#member-email').val().trim();
    if (email) {
        $.get("/dbUser/", { email: email })
            .done((data) => {
                $('#member-info').html(`Member: ${data.first_name} ${data.last_name}`);
                userId = data.user_id;
                fetchCheckedOutMovies(userId);
            })
            .fail((response) => {
                $('#error-message').text(response.responseJSON.error);
                $('#member-info').html('');
                userId = 0;
                $("#checked-out-container").html('');
            });
    } else {
        $('#error-message').text('Please enter a valid email.');
        $('#member-info').html('');
        userId = 0;
        $("#checked-out-container").html('');
    }
};

const fetchCheckedOutMovies = userId => {
    $.get("/dbRent/", { user_id: userId })
        .done((data) => {
            $("#checked-out-container").html(renderCheckedOutTable(data));
        })
        .fail((response) => {
            $("#error-message").text(response.responseJSON.error);
            $("#checked-out-container").html('');
        });
};

const renderCheckedOutTable = movies => {
    return `
        <h2>Checked Out Movies</h2>
        <table id="checked-out-table">
            <thead>
                <tr>
                    <th>Title</th>
                </tr>
            </thead>
            <tbody>${renderMoviesTable(movies, false)}</tbody>
        </table>`;
};

const renderMoviesTable = (movies, checkOut = true) => {
    return movies.map(movie => renderMovieRow(movie, checkOut)).join('');
};

const renderMovieRow = (movie, checkOut) => {
    return `
        <tr>
            <td class='rent-return-item' onclick="toggleMovieCheckout('${movie.movie_id}', '${checkOut ? "rent" : "return"}')">${movie.title}</td>
        </tr>`;
};

const toggleMovieCheckout = (movieId, action) => {
    $.post("/dbRent/", { action: action, user_id: userId, movie_id: movieId })
        .done(() => {
            fetchAllMovies();
            fetchCheckedOutMovies(userId);
            $("#error-message").text("");
        })
        .fail((response) => {
            $("#error-message").text(response.responseJSON.error);
        });
};
