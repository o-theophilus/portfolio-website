<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Link from '$lib/button/link.svelte';
	import Form from './author.edit.svelte';
	import Loading from '$lib/loading.svelte';

	export let post;
	export let edit_mode;
	let author = {};
	let loading = true;

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
	{#if $user.access.includes('post:edit_author') && edit_mode}
		<Button
			size="small"
			on:click={() => {
				$module = {
					module: Form,
					post_key: post.key,
					update
				};
			}}
		>
			<Icon icon="edit" size="1.4" />
			Edit Author
		</Button>
	{/if}
	
	<div class="line">
		{#if !loading}
			<Link href="/profile?search={author.key}">
				<Avatar name={author.name} photo={author.photo} />
			</Link>
			<Link href="/profile?search={author.key}">
				<div class="name">
					{author.name}
				</div>
			</Link>
		{/if}
		<Loading active={loading} size="40" />
		| Author
	</div>
{/if}

<style>
	.line {
		display: flex;
		gap: var(--sp2);
		align-items: center;
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}

	.name {
		color: var(--ft1);
	}
</style>
