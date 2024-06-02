import { page } from '$app/stores';
import { writable, get } from 'svelte/store';
import { invalidate } from '$app/navigation';

export const user = writable();
export const settings = writable({});
export const portal = writable();

export const loading = writable(false);
export const module = writable();
export const notification = writable();

// tools
export const isMobile = writable(false);

export const scroll = (query) => {
	let e = document.querySelector(query);

	const scrollMobile = () => {
		e.scrollIntoView({ behavior: 'smooth' });
	};

	const scrollDesktop = () => {
		const offset = 70;
		const bodyRect = document.body.getBoundingClientRect().top;
		const elementRect = e.getBoundingClientRect().top;
		const elementPosition = elementRect - bodyRect;
		const offsetPosition = elementPosition - offset;

		window.scrollTo({
			top: offsetPosition,
			behavior: 'smooth'
		});
	};

	const unsubscribe = isMobile.subscribe((value) => {
		value ? scrollMobile() : scrollDesktop();
	});
	return unsubscribe;
};


export const timeAgo = (time) => {
	time = new Date(time)
	const now = Date.now();
	const diff = now - time;

	if (diff < 60000) {
		return 'just now';
	} else if (diff < 3600000) {
		const minutes = Math.floor(diff / 60000);
		return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
	} else if (diff < 86400000) {
		const hours = Math.floor(diff / 3600000);
		return `${hours} hour${hours > 1 ? 's' : ''} ago`;
	} else if (diff < 2592000000) {
		const days = Math.floor(diff / 86400000);
		return `${days} day${days > 1 ? 's' : ''} ago`;
	} else {
		const date = new Date(time);
		const year = date.getFullYear();
		const month = date.getMonth() + 1;
		const day = date.getDate();
		return `${day}/${month}/${year}`;
	}
};

export const state = writable([])
export const set_state = (key, value) => {
	let _page = get(page);
	_page.url.searchParams.set(key, value);


	if (value == '') {
		_page.url.searchParams.delete(key);
	}
	if (key != "page_no") {
		_page.url.searchParams.delete("page_no");
	}

	window.history.replaceState(history.state, '', _page.url.href);
	window.scrollTo({ top: 0, behavior: 'smooth' });

	let _state = get(state)
	let i = _state.findIndex(x => x.name == _page.data.page_name)
	_state[i].loaded = false
	_state[i].search = _page.url.search
	state.set(_state)

	loading.set("Loading . . .")
	invalidate(() => true);
};