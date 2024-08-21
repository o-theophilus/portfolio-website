<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Fold from '$lib/button/fold.svelte';
	import Login from '../../account/login.svelte';
	import Icon from '$lib/icon.svelte';
	import Loading from '$lib/loading.svelte';
	import One from './one/index.svelte';
	import Add from './_add.svelte';
	import Drop from '$lib/dropdown.svelte';

	export let post;
	let comments = [];
	let order_by = [];
	let _status = [];
	let open = true;
	let loading = true;
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
					Authorization: $token
				}
			}
		);
		resp = await resp.json();

		if (resp.status == 200) {
			comments = resp.comments;
			order_by = resp.order_by;
			_status = resp._status;
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
		<Loading active={loading} size="20" />
	</strong>

	<Fold
		{open}
		on:click={() => {
			open = !open;
		}}
	/>
</div>

{#if open}
	<div class="margin" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
		<div class="line">
			{#if $user.access.includes('comment:view_deleted')}
				<Drop
					list={_status}
					default_value={search.status || 'active'}
					on:change={(e) => {
						search.status = e.target.value;
						refresh();
					}}
				/>
			{/if}
			{#if comments.length > 1}
				<Drop
					list={order_by}
					icon="sort"
					default_value={search.order || 'sort'}
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
			<div class="margin">No comment</div>
		{/each}
	</div>
{/if}

{#if $user.login}
	<Button
		on:click={() => {
			$module = {
				module: Add,
				post_key: post.key,
				path: [],
				update,
				search
			};
		}}
	>
		<Icon icon="add_comment" />
		Add comment
	</Button>
{:else}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Login
			};
		}}
	>
		Login to add comment
	</Button>
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
