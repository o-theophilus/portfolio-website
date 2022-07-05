export { matchers } from './client-matchers.js';

export const components = [
	() => import("..\\..\\src\\routes\\__layout.svelte"),
	() => import("..\\..\\src\\routes\\__error.svelte"),
	() => import("..\\..\\src\\routes\\blog\\[slug].svelte"),
	() => import("..\\..\\src\\routes\\blog\\index.svelte"),
	() => import("..\\..\\src\\routes\\index.svelte"),
	() => import("..\\..\\src\\routes\\marked.svelte"),
	() => import("..\\..\\src\\routes\\project\\[slug].svelte"),
	() => import("..\\..\\src\\routes\\project\\index.svelte")
];

export const dictionary = {
	"": [[0, 4], [1]],
	"blog": [[0, 3], [1]],
	"marked": [[0, 5], [1]],
	"project": [[0, 7], [1]],
	"blog/[slug]": [[0, 2], [1]],
	"project/[slug]": [[0, 6], [1]]
};