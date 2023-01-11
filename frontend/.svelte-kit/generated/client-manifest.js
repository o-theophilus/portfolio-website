export { matchers } from './client-matchers.js';

export const nodes = [() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11')];

export const server_loads = [];

export const dictionary = {
	"/": [3],
	"/(p)/admin9049": [4,[2]],
	"/(p)/blog": [5,[2]],
	"/(p)/blog/[slug]": [6,[2]],
	"/(p)/project": [7,[2]],
	"/(p)/project/[slug]": [8,[2]],
	"/(p)/tag": [9,[2]],
	"/(p)/tag/[slug]": [10,[2]],
	"/(p)/test": [11,[2]]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};