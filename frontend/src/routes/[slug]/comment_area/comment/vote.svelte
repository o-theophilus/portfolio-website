<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';
	import { createEventDispatcher } from 'svelte';

	export let comment = {};
	let error = {};
	let emit = createEventDispatcher();

	const vote = async (v) => {
		error = {};

		if (v == 'up') {
			if (comment.downvote.includes($user.key)) {
				comment.downvote = comment.downvote.filter((e) => e != $user.key);
			}
			if (comment.upvote.includes($user.key)) {
				comment.upvote = comment.upvote.filter((e) => e != $user.key);
			} else {
				comment.upvote.push($user.key);
			}
		} else if (v == 'down') {
			if (comment.upvote.includes($user.key)) {
				comment.upvote = comment.upvote.filter((e) => e != $user.key);
			}
			if (comment.downvote.includes($user.key)) {
				comment.downvote = comment.downvote.filter((e) => e != $user.key);
			} else {
				comment.downvote.push($user.key);
			}
		}
		comment = comment;

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/vote/${comment.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ vote: v })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			emit('ok', comment);
		} else {
			error = resp;
		}
	};
</script>

<div class="vote">
	<button
		class="left"
		on:click={() => {
			vote('up');
		}}
	>
		<Icon icon="thumb_up" size="16" />
		|
		{comment.upvote.length}
	</button>

	<button
		class="right"
		on:click={() => {
			vote('down');
		}}
	>
		<Icon icon="thumb_down" size="16" />
		|
		{comment.downvote.length}
	</button>

	{#if error.error}
		<span class="error">
			{error.error}
		</span>
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
</style>
