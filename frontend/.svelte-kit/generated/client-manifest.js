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
	() => import('./nodes/9')];

export const server_loads = [];

export const dictionary = {
	"/": [3],
	"/admin9049": [8],
	"/(blog_project)/blog": [~4,[2]],
	"/(blog_project)/blog/[slug]": [~5,[2]],
	"/(blog_project)/project": [~6,[2]],
	"/(blog_project)/project/[slug]": [~7,[2]],
	"/test": [9]
};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
};