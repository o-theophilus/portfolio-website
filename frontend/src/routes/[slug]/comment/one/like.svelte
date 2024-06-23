<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';
	import { createEventDispatcher } from 'svelte';

	export let comment = {};
	let error = {};
	let emit = createEventDispatcher();

	const like = async (x = true) => {
		error = {};

		if (x) {
			if (comment.dislike.includes($user.key)) {
				comment.dislike = comment.dislike.filter((e) => e != $user.key);
			}
			if (comment.like.includes($user.key)) {
				comment.like = comment.like.filter((e) => e != $user.key);
			} else {
				comment.like.push($user.key);
			}
		} else {
			if (comment.like.includes($user.key)) {
				comment.like = comment.like.filter((e) => e != $user.key);
			}
			if (comment.dislike.includes($user.key)) {
				comment.dislike = comment.dislike.filter((e) => e != $user.key);
			} else {
				comment.dislike.push($user.key);
			}
		}
		comment = comment;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/like/${comment.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ like: x })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			emit('update', comment);
		} else {
			error = resp;
		}
	};
</script>

<div class="vote">
	<button
		class="left"
		on:click={() => {
			like();
		}}
	>
		<Icon icon="thumb_up" size="16" />
		|
		{comment.like.length}
	</button>

	<button
		class="right"
		on:click={() => {
			like(false);
		}}
	>
		<Icon icon="thumb_down" size="16" />
		|
		{comment.dislike.length}
	</button>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
</div>

<style>
	.vote {
		display: flex;
		align-items: center;
		gap: 1px;
	}

	button {
		--height: 28px;
		display: flex;
		align-items: center;
		gap: var(--sp0);

		height: var(--height);
		padding: var(--sp0) var(--sp2);
		font-size: small;

		color: var(--ft2);
		background-color: var(--bg2);
		border: none;
		cursor: pointer;

		transition: background-color var(--trans), color var(--trans);
	}
	.left {
		border-radius: var(--height) 0 0 var(--height);
	}
	.right {
		border-radius: 0 var(--height) var(--height) 0;
	}

	button:hover {
		background-color: var(--cl1);
		color: var(--ft1);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
