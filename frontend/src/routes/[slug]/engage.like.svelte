<script>
	import { user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Icon from '$lib/icon.svelte';
	import { createEventDispatcher } from 'svelte';

	export let name;
	export let entity = {};
	export let search = {};
	let error = {};
	let emit = createEventDispatcher();

	const like = async (x = true) => {
		error = {};

		if (x) {
			if (entity.dislike.includes($user.key)) {
				entity.dislike = entity.dislike.filter((e) => e != $user.key);
			}
			if (entity.like.includes($user.key)) {
				entity.like = entity.like.filter((e) => e != $user.key);
			} else {
				entity.like.push($user.key);
			}
		} else {
			if (entity.like.includes($user.key)) {
				entity.like = entity.like.filter((e) => e != $user.key);
			}
			if (entity.dislike.includes($user.key)) {
				entity.dislike = entity.dislike.filter((e) => e != $user.key);
			} else {
				entity.dislike.push($user.key);
			}
		}
		entity = entity;

		let url = `${import.meta.env.VITE_BACKEND}/${name}/like/${entity.key}`;
		if (Object.keys(search).length != 0) {
			url = `${url}?${new URLSearchParams(search).toString()}`;
		}

		let resp = await fetch(url, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ like: x })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			emit('update', resp);
		} else {
			error = resp;
		}
	};
</script>

<div class="line">
	<button
		class="left"
		on:click={() => {
			like();
		}}
	>
		<Icon icon={entity.like.includes($user.key) ? 'thumb_up_fill' : 'thumb_up'} size="1.4" />
		{entity.like.length}
	</button>

	<button
		class="right"
		on:click={() => {
			like(false);
		}}
	>
		<Icon icon={entity.dislike.includes($user.key) ? 'thumb_down_fill' : 'thumb_down'} size="1.4" />
		{entity.dislike.length}
	</button>

	{#if error.error}
		<div class="error">
			{error.error}
		</div>
	{/if}
</div>

<style>
	.line {
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
		font-size: 0.8rem;

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
		color: var(--clb);
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
