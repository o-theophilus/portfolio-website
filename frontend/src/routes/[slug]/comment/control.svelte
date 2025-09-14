<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Datetime, Marked, Avatar, Icon } from '$lib/macro';
	import { Link, RoundButton, Like } from '$lib/button';
	import Add from './_add.svelte';
	import Item from './item.svelte';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';

	let { post, item, update, search } = $props();

	let error = $state({});

	let open_menu = $state(false);
	let self = false;

	const submit_like = async (liked) => {
		error = {};

		let url = `${import.meta.env.VITE_BACKEND}/comment/like/${item.key}`;
		if (Object.keys(search).length != 0) {
			url = `${url}?${new URLSearchParams(search).toString()}`;
		}

		let resp = await fetch(url, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ like: liked })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			item = resp.comment;
		} else {
			error = resp;
		}
	};
</script>

<svelte:window
	onclick={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

{#snippet button(text, icon, onclick)}
	<button class="btn" {onclick}>
		<Icon {icon}></Icon>
		{text}
	</button>
{/snippet}

{#snippet menu()}
	<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if item.user.key == app.user.key}
			{@render button('Delete', 'trash-2', () => module.open(Delete, { item, update, search }))}
		{:else}
			{@render button('Report', 'flag-triangle-right', () => {
				module.open(Report, { item });
			})}
		{/if}
	</div>
{/snippet}

{#if app.login}
	{#if error.error}
		<div class="error" transition:slide>
			{error.error}
		</div>
	{/if}

	<div class="line space control">
		<div class="line">
			<RoundButton icon="reply" onclick={() => module.open(Add, { post, item, update, search })} />

			<Like
				--like-outline-color="var(--cl3)"
				--like-height="32px"
				like={item.likes.length}
				dislike={item.dislikes.length}
				onlike={() => {
					item.dislikes = item.dislikes.filter((e) => e != app.user.key);
					if (item.likes.includes(app.user.key)) {
						item.likes = item.likes.filter((e) => e != app.user.key);
					} else {
						item.likes.push(app.user.key);
					}
					submit_like(true);
				}}
				ondislike={() => {
					item.likes = item.likes.filter((e) => e != app.user.key);
					if (item.dislikes.includes(app.user.key)) {
						item.dislikes = item.dislikes.filter((e) => e != app.user.key);
					} else {
						item.dislikes.push(app.user.key);
					}
					submit_like(false);
				}}
			/>
		</div>

		<div class="menu_area">
			<RoundButton
				icon="ellipsis"
				onclick={() => {
					open_menu = !open_menu;
					self = true;
				}}
			/>

			{#if open_menu}
				{@render menu()}
			{/if}
		</div>
	</div>
{/if}

<style>
	.error {
		color: red;
		font-size: 0.8rem;
		margin: 8px 0;
	}
	.control {
		margin-top: 8px;
	}

	.menu_area {
		position: relative;
	}
	.menu {
		position: absolute;
		bottom: 40px;
		right: 0;

		display: flex;
		flex-direction: column;

		background-color: var(--bg1);
		border-radius: var(--sp0);

		outline: 2px solid var(--bg2);
	}

	.btn {
		all: unset;

		display: flex;
		align-items: center;
		gap: 8px;

		color: var(--ft2);
		font-size: 0.8rem;
		text-align: center;
		padding: 8px;

		border-bottom: 1px solid var(--bg2);

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	.btn:hover {
		background-color: var(--bg2);
		color: var(--ft1);
	}
</style>
