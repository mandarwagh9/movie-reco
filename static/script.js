document.addEventListener('DOMContentLoaded', async () => {
    const genreSelect = document.getElementById('genreSelect');
    const movieContainer = document.getElementById('movieContainer');

    // Fetch genres on page load
    const response = await fetch('/genres');
    const genres = await response.json();

    // Populate genre dropdown
    genres.forEach(genre => {
        const option = document.createElement('option');
        option.value = genre.id;
        option.textContent = genre.name;
        genreSelect.appendChild(option);
    });

    // Fetch movies when a genre is selected
    genreSelect.addEventListener('change', async (event) => {
        const genreId = event.target.value;
        if (genreId) {
            const response = await fetch(`/movies/${genreId}`);
            const movies = await response.json();

            movieContainer.innerHTML = '';
            movies.forEach(movie => {
                const movieElement = document.createElement('div');
                movieElement.classList.add('movie');
                movieElement.innerHTML = `
                    <h3>${movie.title}</h3>
                    <p>${movie.overview}</p>
                    <a href="#" class="details-link" data-id="${movie.id}">More Details</a>
                `;
                movieContainer.appendChild(movieElement);
            });
        } else {
            movieContainer.innerHTML = '';
        }
    });

    // Fetch movie details when "More Details" is clicked
    movieContainer.addEventListener('click', async (event) => {
        if (event.target.classList.contains('details-link')) {
            event.preventDefault();
            const movieId = event.target.getAttribute('data-id');
            const response = await fetch(`/movie/${movieId}`);
            const movieDetails = await response.json();
            alert(`Title: ${movieDetails.title}\nOverview: ${movieDetails.overview}\nRelease Date: ${movieDetails.release_date}`);
        }
    });
});
