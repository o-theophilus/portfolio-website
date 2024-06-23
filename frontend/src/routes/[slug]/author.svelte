<script>
	import { module, user } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Avatar from '$lib/avatar.svelte';
	import Link from '$lib/button/link.svelte';
	import Form from './author_form.svelte';

	export let post;
	export let edit_mode;
	let name = '';
	let photo = '';
	let loading = true;

	const update = async (data) => {
		post = data;
		await refresh();
	};

	export const refresh = async () => {
		loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/post/author/${post.author_key}`);
		resp = await resp.json();
		if (resp.status == 200) {
			name = resp.author.name;
			photo = resp.author.photo;
		}
		loading = false;
	};
</script>

{#if !loading}
	<hr />
	<class class="block">
		<Link href="/profile?search={post.author_key}">
			<Avatar {name} {photo} />
		</Link>
		<Link href="/profile?search={post.author_key}">
			{name}
		</Link>
		| Author

		{#if $user.permissions.includes('post:edit_author') && edit_mode}
			<BRound
				icon="edit"
				icon_size={15}
				on:click={() => {
					$module = {
						module: Form,
						post_key: post.key,
						update
					};
				}}
			/>
		{/if}
	</class>
{/if}

<style>
	.block {
		display: flex;
		gap: var(--sp2);
		align-items: center;
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
