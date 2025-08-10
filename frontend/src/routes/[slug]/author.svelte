<script>
	import { module, app } from '$lib/store.svelte.js';

	import { Button, Link } from '$lib/button';
	import { Icon, Avatar, Spinner } from '$lib/macro';
	import { Row } from '$lib/layout';
	import Form from './author.edit.svelte';

	let { post, edit_mode } = $props();
	let author = $state({});
	let loading = $state(true);

	const update = async (data) => {
		post = data;
		await refresh();
	};

	export const reset = () => {
		loading = true;
	};

	export const refresh = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/author/${post.key}`);
		resp = await resp.json();
		loading = false;
		if (resp.status == 200) {
			author = resp.user;
		}
	};
</script>

{#if loading || author.key}
	<hr />
	{#if app.user.access.includes('post:edit_author') && edit_mode}
		<Button size="small" onclick={() => module.open(Form, { post_key: post.key, update })}>
			<Icon icon="edit" size="1.4" />
			Edit Author
		</Button>
	{/if}

	<Row>
		{#if !loading}
			<Link href="/profile?search={author.key}">
				<Avatar name={author.name} photo={author.photo} --avatar-border-radius="100%" />
			</Link>
			<Link href="/profile?search={author.key}" --link-font-size="0.8rem">
				<div class="name">
					{author.name}
				</div>
			</Link>
		{/if}
		<Spinner active={loading} size="20" />

		<span class="author"> | </span>
		<span class="author"> Author </span>
	</Row>
{/if}

<style>
	hr {
		margin: var(--sp2) 0;
	}

	.author {
		font-size: 0.8rem;
	}
</style>
