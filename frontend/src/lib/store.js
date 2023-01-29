import { writable } from 'svelte/store';

export const api_url = import.meta.env.VITE_API_URL;

// app variables
export const _user = writable();

// variables
export const module = writable();
export const loading = writable(false);

export const _tick = writable("");
export const tick = (data) => {
	_tick.set(data);
}


// tools
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

// temp fix
export const theme = writable("dark");