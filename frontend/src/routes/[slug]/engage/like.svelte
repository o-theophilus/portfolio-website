<script>
	import { app } from '$lib/store.svelte.js';

	import { Icon2 } from '$lib/macro';
	import { createEventDispatcher } from 'svelte';

	let { name, entity = {}, search = {} } = $props();
	let error = $state({});
	let emit = createEventDispatcher();

	const like = async (x = true) => {
		error = {};

		if (x) {
			if (entity.dislike.includes(app.user.key)) {
				entity.dislike = entity.dislike.filter((e) => e != app.user.key);
			}
			if (entity.like.includes(app.user.key)) {
				entity.like = entity.like.filter((e) => e != app.user.key);
			} else {
				entity.like.push(app.user.key);
			}
		} else {
			if (entity.like.includes(app.user.key)) {
				entity.like = entity.like.filter((e) => e != app.user.key);
			}
			if (entity.dislike.includes(app.user.key)) {
				entity.dislike = entity.dislike.filter((e) => e != app.user.key);
			} else {
				entity.dislike.push(app.user.key);
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
				Authorization: app.token
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
		onclick={() => {
			like();
		}}
	>
		<Icon2 icon="thumbs-up" active={entity.like.includes(app.user.key)} />
		{entity.like.length}
	</button>

	<button
		class="right"
		onclick={() => {
			like(false);
		}}
	>
		<Icon2 icon="thumbs-down" active={entity.dislike.includes(app.user.key)} />
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
		display: flex;
		align-items: center;
		gap: var(--sp0);

		height: var(--like-height, 48px);
		padding: var(--sp0) var(--sp2);
		font-size: 0.8rem;

		color: var(--ft2);
		background-color: var(--bg2);
		border: none;
		cursor: pointer;

		transition:
			background-color var(--trans),
			color var(--trans);
	}
	.left {
		border-radius: var(--like-height, 48px) 0 0 var(--like-height, 48px);
	}
	.right {
		border-radius: 0 var(--like-height, 48px) var(--like-height, 48px) 0;
	}

	button:hover {
		background-color: var(--cl1);
		color: white;
	}

	.error {
		margin: var(--sp2) 0;
	}
</style>
