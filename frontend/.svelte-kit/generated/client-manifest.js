export { matchers } from './client-matchers.js';

export const nodes = [() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8')];

export const server_loads = [];

export const dictionary = {
	"/": [2],
	"/admin9049": [3],
	"/blog": [4],
	"/blog/[slug]": [5],
	"/marked": [6],
	"/project": [~7],
	"/project/[slug]": [~8]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};