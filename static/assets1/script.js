// Elementos
const toggleThemeBtn = document.querySelector('.header__theme-button');
const storiesContent = document.querySelector('.stories__content');
const storiesLeftButton = document.querySelector('.stories__left-button');
const storiesRightButton = document.querySelector('.stories__right-button');
const posts = document.querySelectorAll('.post');
const postsContent = document.querySelectorAll('.post__content');

// ===================================
//TEMA OSCURO/CLARA
// Establecer tema inicial desde LocalStorage
document.onload = setInitialTheme(localStorage.getItem('theme'));
function setInitialTheme(themeKey) {
    if(themeKey === 'dark') {
        document.documentElement.classList.add('darkTheme');
    }
    else {
        document.documentElement.classList.remove('darkTheme');
    }
}

// Botón para alternar tema
toggleThemeBtn.addEventListener('click', () => {
// Alternar clase raíz
    document.documentElement.classList.toggle('darkTheme');
// Guardando el tema actual en LocalStorage
    if(document.documentElement.classList.contains('darkTheme')) {
        localStorage.setItem('theme', 'dark');
    }
    else {
        localStorage.setItem('theme', 'light');
    }
});

//=====================================
// BOTONES DE DESPLAZAMIENTO DE HISTORIAS
// Desplazamiento del contenido de las historias
storiesLeftButton.addEventListener('click', () => {
    storiesContent.scrollLeft -= 320;
});
storiesRightButton.addEventListener('click', () => {
    storiesContent.scrollLeft += 320;
});

// Comprobando si la pantalla tiene un tamaño mínimo de 1024 px
if(window.matchMedia('(min-width: 1024px)').matches) {
    // Observador para ocultar botones cuando sea necesario
    const storiesObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if(entry.target === document.querySelector('.story:first-child')) {
                storiesLeftButton.style.display = (entry.isIntersecting) ? 'none' : 'unset';
            }
            else if(entry.target === document.querySelector('.story:last-child')) {
                storiesRightButton.style.display = (entry.isIntersecting) ? 'none' : 'unset';
            }
        });
    }, { root: storiesContent, threshold: 1 });

    // Llamar al observador con la primera y la última historia.
    storiesObserver.observe(document.querySelector('.story:first-child'));
    storiesObserver.observe(document.querySelector('.story:last-child'));
}

// =====================================
// PUBLICAR MÚLTIPLES MEDIOS
// Crear botones de desplazamiento e indicadores cuando la publicación tiene más de un medio
posts.forEach(post => {
    if(post.querySelectorAll('.post__media').length > 1) {
        const leftButtonElement = document.createElement('button');
        leftButtonElement.classList.add('post__left-button');
        leftButtonElement.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="var(--primary)" d="M256 504C119 504 8 393 8 256S119 8 256 8s248 111 248 248-111 248-248 248zM142.1 273l135.5 135.5c9.4 9.4 24.6 9.4 33.9 0l17-17c9.4-9.4 9.4-24.6 0-33.9L226.9 256l101.6-101.6c9.4-9.4 9.4-24.6 0-33.9l-17-17c-9.4-9.4-24.6-9.4-33.9 0L142.1 239c-9.4 9.4-9.4 24.6 0 34z"></path>
            </svg>
        `;

        const rightButtonElement = document.createElement('button');
        rightButtonElement.classList.add('post__right-button');
        rightButtonElement.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                <path fill="var(--primary)" d="M256 8c137 0 248 111 248 248S393 504 256 504 8 393 8 256 119 8 256 8zm113.9 231L234.4 103.5c-9.4-9.4-24.6-9.4-33.9 0l-17 17c-9.4 9.4-9.4 24.6 0 33.9L285.1 256 183.5 357.6c-9.4 9.4-9.4 24.6 0 33.9l17 17c9.4 9.4 24.6 9.4 33.9 0L369.9 273c9.4-9.4 9.4-24.6 0-34z"></path>
            </svg>
        `;

        post.querySelector('.post__content').appendChild(leftButtonElement);
        post.querySelector('.post__content').appendChild(rightButtonElement);

        post.querySelectorAll('.post__media').forEach(function() {
            const postMediaIndicatorElement = document.createElement('div');
            postMediaIndicatorElement.classList.add('post__indicator');

            post.querySelector('.post__indicators').appendChild(postMediaIndicatorElement);
        });

        // Observador para cambiar el indicador de medios real
        const postMediasContainer = post.querySelector('.post__medias');
        const postMediaIndicators = post.querySelectorAll('.post__indicator');
        const postIndicatorObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    // Remover los Indicadores
                    postMediaIndicators.forEach(indicator => indicator.classList.remove('post__indicator--active'));
                    // Agregar el indicador que coincide con el medio de la publicación actual
                    postMediaIndicators[Array.from(postMedias).indexOf(entry.target)].classList.add('post__indicator--active');
                }
            });
        }, { root: postMediasContainer, threshold: 0.5 });

        // Llamando al observador para cada publicación multimedia.
        const postMedias = post.querySelectorAll('.post__media');
        postMedias.forEach(media => {
            postIndicatorObserver.observe(media);
        });
    }
});

// Agregar funciones de botones en cada publicación con múltiples medios
postsContent.forEach(post => {
    if(post.querySelectorAll('.post__media').length > 1) {
        const leftButton = post.querySelector('.post__left-button');
        const rightButton = post.querySelector('.post__right-button');
        const postMediasContainer = post.querySelector('.post__medias');

       // Funciones para los botones izquierdo y derecho
        leftButton.addEventListener('click', () => {
            postMediasContainer.scrollLeft -= 400;
        });
        rightButton.addEventListener('click', () => {
            postMediasContainer.scrollLeft += 400;
        });

       // Observador para ocultar el botón si es necesario
        const postButtonObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if(entry.target === post.querySelector('.post__media:first-child')) {
                    leftButton.style.display = (entry.isIntersecting) ? 'none' : 'unset';
                }
                else if(entry.target === post.querySelector('.post__media:last-child')) {
                    rightButton.style.display = (entry.isIntersecting) ? 'none' : 'unset';
                }
            });
        }, { root: postMediasContainer, threshold: 0.5 });

        if(window.matchMedia('(min-width: 1024px)').matches) {
            postButtonObserver.observe(post.querySelector('.post__media:first-child'));
            postButtonObserver.observe(post.querySelector('.post__media:last-child'));
        }
    }
});
