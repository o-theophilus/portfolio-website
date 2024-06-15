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

