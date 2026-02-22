<script>
	import { app, module } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Like, RoundButton } from '$lib/button';
	import { Icon } from '$lib/macro';
	import Add from './_add.svelte';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';

	let { comment, post, search, update } = $props();

	let error = $state({});
	let open_menu = $state(false);
	let self = false;

	let engagement = $derived(comment.engagement);
	let like = $derived.by(() => {
		if (engagement.user_reaction == 'like') return engagement.others_like + 1;
		return engagement.others_like;
	});
	let dislike = $derived.by(() => {
		if (engagement.user_reaction == 'dislike') return engagement.others_dislike + 1;
		return engagement.others_dislike;
	});

	const submit = async (reaction) => {
		if (reaction == engagement.user_reaction) {
			engagement.user_reaction = null;
		} else {
			engagement.user_reaction = reaction;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/comment/like/${comment.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ reaction })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			engagement = {
				others_like: resp.others_like,
				others_dislike: resp.others_dislike,
				user_reaction: resp.user_reaction
			};
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
		{#if comment.user.key == app.user.key}
			{@render button('Delete', 'trash-2', () => module.open(Delete, { comment, update, search }))}
		{:else}
			{@render button('Report', 'flag-triangle-right', () => {
				module.open(Report, { comment });
			})}
		{/if}
	</div>
{/snippet}

<!-- TODO: enforce all app.login in the backend -->
{#if app.login}
	{#if error.error}
		<div class="error" transition:slide>
			{error.error}
		</div>
	{/if}

	<div class="line space control">
		<div class="line">
			<RoundButton
				icon="reply"
				onclick={() => module.open(Add, { comment, post, search, update })}
			/>

			<Like
				--like-height="32px"
				{like}
				{dislike}
				active={engagement.user_reaction}
				onlike={() => submit('like')}
				ondislike={() => submit('dislike')}
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
		margin-top: 16px;
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
		border-radius: 4px;

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
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	.btn:hover {
		background-color: var(--bg2);
		color: var(--ft1);
	}
</style>
