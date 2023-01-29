import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export const setCookie = (name, value, exdays) => {
	let date = new Date();
	date.setTime(date.getTime() + exdays * 24 * 60 * 60 * 1000);
	if (browser) {
		document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
	}
};

export const getCookie = (name) => {
	if (browser) {
		let cookies = document.cookie.split(';');
		for (let i in cookies) {
			let temp = cookies[i].split('=');
			if (temp[0].trim() === name) {
				return temp[1];
			}
		}
	}
	return '';
};

export let token = writable(getCookie('token'), () => {
	const unsubscribe = token.subscribe((value) => {
		let day = value ? 1 : -10000;
		setCookie('token', value, day);
	});
	return unsubscribe;
});
