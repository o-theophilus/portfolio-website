<script context="module">
	import { api_url } from '$lib/store.js';

	export async function load({ fetch, params }) {
		let { slug } = params;
		const _resp = await fetch(`${api_url}/blog/${slug}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			console.log(resp);

			return {
				props: {
					blog: resp.data.blog
				}
			};
		}
	}
</script>

<script>
	import Page from '$lib/page.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';

	export let blog;
</script>

<Meta title={blog.title} description={blog.summary} image={blog.image} />

<Page>
	<img src="/images/{blog.image}" alt={blog.title} onerror="this.src='/site/error.jpg'" />
	<h2>{blog.title}</h2>
	{#each blog.tags as tag}
		<p>{tag}</p>
	{/each}
	<p class="date">{blog.created_at}</p>

	{#if blog.type_ == 'markdown'}
		<Marked md={blog.content} />
	{:else}
		{@html blog.content}
	{/if}
</Page>

<style>
	h2 {
		text-align: center;
		padding: var(--gap3) 0;
	}

	.date {
		font-size: x-small;
	}
</style>
