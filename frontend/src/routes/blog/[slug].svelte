<script context="module">
	import { posts, _posts } from '$lib/db.js';
	let temp = [...posts, ..._posts];

	export async function load({ params }) {
		let { slug } = params;
		let post;
		for (let i = 0; i < temp.length; i++) {
			if (temp[i].slug === slug) {
				post = temp[i];
				break;
			}
		}
		if (post) {
			return { props: { post } };
		}
	}
</script>

<script>
	import Content from '$lib/pageContent.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';

	export let post;
</script>

<Meta title={post.title} description={post.summary} image={post.image} />

<Content noMargin>
	<img src="/images/{post.image}" alt={post.title} />
	<h2>
		<p>{post.title}</p>
	</h2>
	<p>{post.tags}</p>
	<p class="date">{post.date}</p>
	<br />
	{#if post.type === 'md'}
		<Marked md={post.content} />
	{:else}
		{@html post.content}
	{/if}
</Content>
