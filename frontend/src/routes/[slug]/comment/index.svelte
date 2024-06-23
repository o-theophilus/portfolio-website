<script>
	import { slide } from 'svelte/transition';
	import { flip } from 'svelte/animate';
	import { cubicInOut } from 'svelte/easing';
	import { module, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button/button.svelte';
	import Fold from '$lib/button/fold.svelte';
	import Link from '$lib/button/link.svelte';
	import Login from '../../account/login.svelte';
	import Icon from '$lib/icon.svelte';
	import Loading from '$lib/loading_spinner.svelte';
	import One from './one/index.svelte';
	import Add from './_add.svelte';
	import Drop from '$lib/dropdown.svelte';

	export let post;
	let comments = [];
	let order_by = [];
	let _status = [];
	let open = true;

	const update = (data) => {
		comments = data;
	};

	let loading = true;
	let select_status = '';
	let select_order = '';

	export const refresh = async () => {
		let search = {};
		if (select_status) {
			search.status = select_status;
		}
		if (select_order) {
			search.order = select_order;
		}

		loading = true;
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comment/${post.key}?${new URLSearchParams(
				search
			).toString()}`,
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
			{#if $user.permissions.includes('comment:view_deleted')}
				<Drop
					list={_status}
					default_value="active"
					on:change={(e) => {
						select_status = e.target.value;
						refresh();
					}}
				/>
			{/if}
			{#if comments.length > 1}
				<Drop
					list={order_by}
					icon="sort"
					on:change={(e) => {
						select_order = e.target.value;
						refresh();
					}}
				/>
			{/if}
		</div>

		{#each comments as x (x.key)}
			<div animate:flip={{ delay: 0, duration: 250, easing: cubicInOut }}>
				{#if x.path.length == 0}
					<One comment={x} {comments} post_key={post.key} {update} />
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
				path: []
			};
		}}
	>
		<Icon icon="add_comment" />
		Add comment
	</Button>
{:else}
	<Link
		on:click={() => {
			$module = {
				module: Login
			};
		}}
	>
		Login
	</Link> to add comment
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
</style>
