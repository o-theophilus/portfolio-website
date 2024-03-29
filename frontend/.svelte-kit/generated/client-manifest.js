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
	() => import('./nodes/11'),
	() => import('./nodes/12')];

export const server_loads = [0];

export const dictionary = {
	"/": [3],
	"/(p)/blog": [4,[2]],
	"/(p)/blog/[slug]": [5,[2]],
	"/(p)/login": [6,[2]],
	"/(p)/logout": [7,[2]],
	"/(p)/project": [8,[2]],
	"/(p)/project/[slug]": [9,[2]],
	"/(p)/tags": [10,[2]],
	"/(p)/tags/[slug]": [11,[2]],
	"/(p)/test": [12,[2]]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};