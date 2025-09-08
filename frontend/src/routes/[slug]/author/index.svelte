<script>
	import { module, app } from '$lib/store.svelte.js';

	import { Link } from '$lib/button';
	import Button from '../button.svelte';
	import { Avatar, Spinner } from '$lib/macro';
	import Form from './edit.svelte';

	let { post, edit_mode } = $props();
	let author = $state({});
	let loading = $state(true);

	const update = async (data) => {
		post = data;
	};

	export const load = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/author/${post.key}`);
		resp = await resp.json();
		loading = false;
		if (resp.status == 200) {
			author = resp.user;
		}
	};
</script>

{#if loading || author.username}
	<hr />
	{#if app.user.access.includes('post:edit_author') && edit_mode}
		<Button onclick={() => module.open(Form, { post_key: post.key, update })}>Edit Author</Button>
	{/if}

	<div class="line">
		{#if loading}
			<Spinner active={loading} size="20" />
		{:else}
			<Link href="/@{author.username}">
				<Avatar name={author.name} photo={author.photo} --avatar-border-radius="50%" />
			</Link>
			<Link href="/@{author.username}" --link-font-size="0.8rem">
				<div class="name">
					{author.name}
				</div>
			</Link>
		{/if}

		<span class="author"> | </span>
		<span class="author"> Author </span>
	</div>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}

	.author {
		font-size: 0.8rem;
	}
</style>
