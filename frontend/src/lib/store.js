import { writable } from 'svelte/store';

export const showHeader = writable(true);
export const openMobileMenu = writable(false);
export const isMobile = writable(true);

// tools
export const scroll = (query) => {
	const scrollMobile = () => {
		let e = document.querySelector(query);
		e.scrollIntoView({ behavior: 'smooth' });
	};

	const scrollDesktop = () => {
		let e = document.querySelector(query);
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
	// $isMobile ? scrollMobile() : scrollDesktop();

	const unsubscribe = isMobile.subscribe((value) => {
		value ? scrollMobile() : scrollDesktop();
	});
	return unsubscribe;
};
