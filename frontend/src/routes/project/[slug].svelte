<script context="module">
	import { projects, _projects } from '$lib/db.js';
	let temp = [...projects, ..._projects];

	export async function load({ params }) {
		let { slug } = params;
		let project;
		for (let i = 0; i < temp.length; i++) {
			if (temp[i].slug === slug) {
				project = temp[i];
				break;
			}
		}
		if (project) {
			return { props: { project } };
		}
	}
</script>

<script>
	import { scroll } from '$lib/store.js';
	import { onMount } from 'svelte';

	import Content from '$lib/pageContent.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';

	export let project;

	onMount(() => {
		var parent = document.querySelector('.pageContent');
		parent.addEventListener(
			'click',
			(e) => {
				if (e.target.matches('span.link')) {
					scroll('footer');
				}
			},
			false
		);
	});
</script>

<Meta title={project.title} description={project.summary} image={project.image} />

<Content noMargin>
	<img src="/images/{project.image}" alt={project.title} />
	<h2>
		<p>{project.title}</p>
	</h2>
	<p>{project.tags}</p>
	<p class="date">{project.date}</p>
	<br />
	{#if project.type === 'md'}
		<Marked md={project.content} />
	{:else}
		{@html project.content}
	{/if}
</Content>
