<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Button, FoldButton } from '$lib/button';
	import { Login } from '$lib/auth';
	import { Icon, Spinner } from '$lib/macro';
	import { Dropdown } from '$lib/input';
	import { PageNote } from '$lib/info';
	import One from './one/index.svelte';
	import Add from './_add.svelte';

	let { post } = $props();
	let comments = $state([]);
	let order_by = $state([]);
	let _status = $state([]);
	let open = $state(true);
	let loading = $state(true);
	let search = {};

	const update = (data) => {
		comments = data;
	};

	export const reset = () => {
		loading = true;
		comments = [];
	};

	export const refresh = async () => {
		let s = {};
		if (search.status) {
			s.status = search.status;
		}
		if (search.order) {
			s.order = search.order;
		}

		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${post.key}?${new URLSearchParams(s).toString()}`,
			{
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			comments = resp.comments;
			order_by = resp.order_by;
			_status = resp._status;
			if (!comments.length) open = false;
		}
		loading = false;
	};
</script>

<hr />

<div class="title">
	<strong class="ititle">
		{#if comments.length > 0}
			{comments.length}
		{/if}
		Comment{#if comments.length > 1}s{/if}
		<Spinner active={loading} size="20" />
	</strong>

	<FoldButton
		{open}
		onclick={() => {
			open = !open;
		}}
	/>
</div>

{#if open}
	<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<div class="line">
			{#if app.user.access.includes('comment:view_deleted')}
				<Dropdown
					list={_status}
					default_value={search.status || 'active'}
					on:change={(e) => {
						search.status = e.target.value;
						refresh();
					}}
				/>
			{/if}
			{#if comments.length > 1}
				<Dropdown
					icon="sort"
					list={order_by}
					default_value={search.order || 'latest'}
					on:change={(e) => {
						search.order = e.target.value;
						refresh();
					}}
				/>
			{/if}
		</div>

		{#each comments as x (x.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				{#if x.path.length == 0}
					<One comment={x} {comments} post_key={post.key} {update} {search} />
				{/if}
			</div>
		{:else}
			<PageNote>No comment</PageNote>
		{/each}
	</div>
{/if}

{#if app.user.login}
	<Button onclick={() => module.open(Add, { post_key: post.key, path: [], update, search })}>
		<Icon icon="add_comment" />
		Add comment
	</Button>
{:else}
	<Button size="small" onclick={() => module.open(Login)}>Login to add comment</Button>
{/if}

<br />

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: var(--sp2);
		margin: var(--sp2) 0;

		font-weight: 800;
		color: var(--ft1);
	}
	.ititle {
		display: flex;
		align-items: center;
		gap: var(--sp2);
	}
	.margin {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
		margin-bottom: var(--sp2);
	}

	hr {
		margin: var(--sp2) 0;
	}
</style>
