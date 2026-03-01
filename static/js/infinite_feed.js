(() => {
    const feed = document.getElementById('feed');
    const loader = document.getElementById('feed-loader');

    if (!feed || !loader) {
        return;
    }

    let nextPage = loader.dataset.nextPage;
    let isLoading = false;

    const query = feed.dataset.query || '';
    const country = feed.dataset.country || '';

    const buildUrl = (page) => {
        const params = new URLSearchParams();
        if (query) {
            params.set('q', query);
        }
        if (country) {
            params.set('country', country);
        }
        params.set('page', page);
        return `/feed/?${params.toString()}`;
    };

    const loadMore = async () => {
        if (!nextPage || isLoading) {
            return;
        }
        isLoading = true;
        loader.style.display = 'inline-flex';

        try {
            const response = await fetch(buildUrl(nextPage), {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            if (!response.ok) {
                return;
            }

            const payload = await response.json();
            if (payload.html) {
                feed.insertAdjacentHTML('beforeend', payload.html);
            }

            if (payload.has_next && payload.next_page) {
                nextPage = payload.next_page;
            } else {
                nextPage = '';
                loader.style.display = 'none';
            }
        } catch (err) {
            // Keep loader visible for retry on scroll.
        } finally {
            isLoading = false;
        }
    };

    const onScroll = () => {
        if (!nextPage || isLoading) {
            return;
        }
        const threshold = 300;
        const scrolled = window.innerHeight + window.scrollY;
        if (scrolled >= document.documentElement.scrollHeight - threshold) {
            loadMore();
        }
    };

    window.addEventListener('scroll', onScroll);
})();
